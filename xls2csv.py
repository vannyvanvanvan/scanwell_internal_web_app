import pandas as pd

xlsx_name = "美加航線倉位狀況表20241018.xlsx"
csv_name = "xls2.csv"

# table = pd.read_excel(xlsx_name, keep_default_na=False)
# table.to_csv(csv_name, index=False)


def is_csv_valid(file, extension="csv"):
    try:
        # file not valid if extension incorrect
        if extension not in ["csv", "xlsx"]:
            raise ValueError("File format not recognised")

        # read dataframe from file name based on extension
        df = (
            pd.read_csv(file, keep_default_na=False)
            if extension == "csv"
            else pd.read_excel(file, keep_default_na=False)
        )

        print(df.columns)

        target_columns = [
            "CS",
            "WEEK",
            "CARRIER",
            "SERVICE",
            "M/V",
            "S/O",
            "SIZE",
            "POL",
            "POD",
            "FINAL DEST",
            "ROUTING",
            "CY OPEN",
            "SI CUT OFF",
            "CY/CV CLS",
            "ETD",
            "ETA",
            "Contract/Co-loader",
            "S/",
            "C/",
            "TERM",
            "Saleman",
            "Cost",
            "RATE VALID",
            "S/R",
            "Remark",
        ]

        if not all(column in target_columns for column in df.columns):
            raise ValueError("Incomplete column data")

    except Exception as e:
        print(e)
        return False
    return True


print(is_csv_valid(xlsx_name, "xlsx"))
