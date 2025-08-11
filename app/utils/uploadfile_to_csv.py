from io import StringIO
from typing import List
import pandas as pd
from fastapi import UploadFile


async def read_csv_files(files: List[UploadFile]) -> List[pd.DataFrame]:
    """
    Reads a list of uploaded CSV files and returns a list of DataFrames.
    """
    dfs = []
    for f in files or []:
        content = await f.read()
        df = pd.read_csv(StringIO(content.decode()))
        dfs.append(df)
    return dfs