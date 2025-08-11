import pandas as pd
from fastapi.encoders import jsonable_encoder
from matplotlib import pyplot as plt
from app.utils import fig_to_base64,read_csv_files


async def process(qtext,files):
    dfs = await read_csv_files(files)

    if not dfs:
        return {"error": "No CSV files provided"}

    combined_df = pd.concat(dfs, ignore_index=True)

    # 1. Total sales
    total_sales = combined_df["sales"].sum()

    # 2. Region with the highest total sales
    region_totals = combined_df.groupby("region")["sales"].sum()
    highest_region = region_totals.idxmax()

    # 3. Correlation between day of month and sales
    combined_df["date"] = pd.to_datetime(combined_df["date"])
    combined_df["day"] = combined_df["date"].dt.day
    correlation = combined_df["day"].corr(combined_df["sales"])

    # 4. Bar chart of total sales by region (blue bars)
    fig1, ax1 = plt.subplots()
    region_totals.plot(kind="bar", color="blue", ax=ax1)
    ax1.set_xlabel("Region")
    ax1.set_ylabel("Total Sales")
    ax1.set_title("Total Sales by Region")
    bar_chart_base64 = fig_to_base64(fig1)
    plt.close(fig1)

    # 5. Median sales amount
    median_sales = combined_df["sales"].median()

    # 6. Total sales tax (10%)
    total_tax = total_sales * 0.10

    # 7. Cumulative sales over time (red line)
    combined_df_sorted = combined_df.sort_values("date")
    combined_df_sorted["cumulative_sales"] = combined_df_sorted["sales"].cumsum()
    fig2, ax2 = plt.subplots()
    ax2.plot(combined_df_sorted["date"], combined_df_sorted["cumulative_sales"], color="red")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Cumulative Sales")
    ax2.set_title("Cumulative Sales Over Time")
    line_chart_base64 = fig_to_base64(fig2)
    plt.close(fig2)

    # Prepare JSON-safe response
    result = {
        "total_sales": float(total_sales),
        "top_region": str(highest_region),
        "day_sales_correlation": float(correlation),
        "bar_chart": bar_chart_base64,
        "median_sales": float(median_sales),
        "total_sales_tax": float(total_tax),
        "cumulative_sales_chart": line_chart_base64
    }

    return jsonable_encoder(result)
