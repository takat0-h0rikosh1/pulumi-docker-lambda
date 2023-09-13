import tempfile
import pandas as pd
from typing import Any

class ExcelExporter:
    @staticmethod
    def save_to_xlsx(df: pd.DataFrame, file_path: str) -> None:
        temp_csv = tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False, encoding='utf-8-sig')
        df.to_csv(temp_csv, index=False)
        temp_csv.close()
        df_from_csv = pd.read_csv(temp_csv.name)
        df_from_csv.to_excel(file_path, index=False)
