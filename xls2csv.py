import pandas as pd

xlsx_name = "美加航線倉位狀況表20241018.xlsx"
csv_name = "xls2.csv"

# table = pd.read_excel(xlsx_name, keep_default_na=False)
# table.to_csv(csv_name, index=False)


def is_csv_valid(file, extension="csv"):
    try:
        df = (
            pd.read_csv(file, keep_default_na=False)
            if extension == "csv"
            else pd.read_excel(file, keep_default_na=False)
        )
    except Exception as e:
        return False
    return True


print(is_csv_valid(xlsx_name, "xlsx"))
