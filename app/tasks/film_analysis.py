import pandas as pd
from app.services.graph_plotter import scatter_with_regression_datauri

async def process(qtext, files):
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_highest-grossing_films")[0]
    # Clean and process data
    df["gross_in_dollars"] = df["Worldwide gross"].str.split("$").str[-1].str.strip().str.replace(",", "").astype("int64")
    df["Peak"] = df["Peak"].str.extract(r"(\d+)").astype(int)
    df = df.drop(columns=["Ref","Worldwide gross"])
    # Calculate answers
    # How many $2 bn movies were released before 2000?
    q1 = len(df[(df["gross_in_dollars"]>=2000000000) & (df["Year"]<2000)])
    # Which is the earliest film that grossed over $1.5 bn?
    q2 = (df[df["gross_in_dollars"] > 1_500_000_000].sort_values("Year", ascending=True).iloc[0])["Title"]
    # What's the correlation between the Rank and Peak?
    q3 = round(df["Rank"].corr(df["Peak"]),6)
    # Generate plot
    q4 = scatter_with_regression_datauri(
        df["Rank"], df["Peak"],
        xlabel="Rank", ylabel="Peak",
        title="Rank vs Peak (with dotted red regression)"
    )
    return [q1,q2,q3,q4]