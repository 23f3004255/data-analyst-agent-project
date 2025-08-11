import io
import base64
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def scatter_with_regression_datauri(
    x,
    y,
    xlabel: str = "Rank",
    ylabel: str = "Peak",
    title: str = "Rank vs Peak",
    max_bytes: int = 100_000,
    ) -> Optional[str]:
    """
    Create a scatterplot with a dotted red regression line and return a
    base64-encoded PNG data URI under `max_bytes` (tries compressing/resizing).
    Returns None on failure.
    """
    # ensure numpy arrays
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # drop NaNs (both)
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    if x.size < 2:
        return None

    # fit linear regression (slope, intercept)
    m, b = np.polyfit(x, y, 1)

    # create a small figure (keeps image bytes smaller)
    plt.ioff()
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.scatter(x, y, s=12)
    xs = np.linspace(x.min(), x.max(), 200)
    ax.plot(xs, m * xs + b, linestyle=":", color="red", linewidth=1.6)  # dotted red line
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout(pad=0.6)

    # Save to PNG buffer first
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    png_data = buf.getvalue()

    # If already under target, return it
    if len(png_data) <= max_bytes:
        return "data:image/png;base64," + base64.b64encode(png_data).decode("ascii")

    # Otherwise try compressing / resizing using Pillow
    img = Image.open(io.BytesIO(png_data))

    # Try various strategies: reduce compress_level (for PNG use optimize + compress_level)
    # and progressively downscale image until size is under max_bytes
    scales = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
    compress_levels = list(range(9, -1, -1))  # attempt high compression first (9) down to 0

    for scale in scales:
        new_w = max(64, int(img.width * scale))
        new_h = max(48, int(img.height * scale))
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)

        for comp in compress_levels:
            out = io.BytesIO()
            try:
                # optimize + compress_level may reduce PNG size
                img_resized.save(out, format="PNG", optimize=True, compress_level=comp)
            except OSError:
                # some combinations may fail on some platforms; try without optimize
                out = io.BytesIO()
                img_resized.save(out, format="PNG", compress_level=comp)

            data = out.getvalue()
            if len(data) <= max_bytes:
                return "data:image/png;base64," + base64.b64encode(data).decode("ascii")

    # Final fallback: convert to paletted PNG to reduce size
    try:
        pal = img.convert("P", palette=Image.ADAPTIVE)
        out = io.BytesIO()
        pal.save(out, format="PNG", optimize=True)
        data = out.getvalue()
        if len(data) <= max_bytes:
            return "data:image/png;base64," + base64.b64encode(data).decode("ascii")
    except Exception:
        pass

    # If everything failed, return None (or you can raise)
    return None
