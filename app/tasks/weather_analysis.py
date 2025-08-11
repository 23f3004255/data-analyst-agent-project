import pandas as pd
from matplotlib import pyplot as plt
from app.utils import fig_to_base64,read_csv_files


async def process(qtext, files):
    dfs = await read_csv_files(files)

    if not dfs:
        return {"error": "No CSV files provided"}

    # Only handling first CSV for now
    df = dfs[0]

    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])

    # 1. Average temperature
    average_temp_c = float(df["temperature_c"].mean())

    # 2. Date with the highest precipitation
    max_precip_date = str(df.loc[df["precip_mm"].idxmax(), "date"].strftime("%Y-%m-%d"))

    # 3. Minimum temperature
    min_temp_c = float(df["temperature_c"].min())

    # 4. Correlation between temperature and precipitation
    temp_precip_correlation = float(df["temperature_c"].corr(df["precip_mm"]))

    # 5. Average precipitation
    average_precip_mm = float(df["precip_mm"].mean())

    # 6. Temperature over time (red line)
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["temperature_c"], color="red")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Over Time")
    temp_line_chart = fig_to_base64(fig)

    # 7. Precipitation histogram (orange bars)
    fig, ax = plt.subplots()
    ax.hist(df["precip_mm"], bins=5, color="orange", edgecolor="black")
    ax.set_xlabel("Precipitation (mm)")
    ax.set_ylabel("Frequency")
    ax.set_title("Precipitation Histogram")
    precip_histogram = fig_to_base64(fig)

    return {
        "average_temp_c": round(average_temp_c, 2),
        "max_precip_date": max_precip_date,
        "min_temp_c": min_temp_c,
        "temp_precip_correlation": round(temp_precip_correlation, 4) if pd.notnull(temp_precip_correlation) else None,
        "average_precip_mm": round(average_precip_mm, 2),
        "temp_line_chart": temp_line_chart,
        "precip_histogram": precip_histogram
    }