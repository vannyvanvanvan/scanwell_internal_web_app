from datetime import datetime
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

        # columns required
        target_columns = {
            "CS": str,
            "WEEK": int,
            "CARRIER": str,
            "SERVICE": str,
            "M/V": str,
            "S/O": str,
            "SIZE": str,
            "POL": str,
            "POD": str,
            "FINAL DEST": str,
            "ROUTING": str,
            "CY OPEN": datetime,
            "SI CUT OFF": datetime,
            "CY/CV CLS": datetime,
            "ETD": datetime,
            "ETA": datetime,
            "Contract/Co-loader": str,
            "S/": str,
            "C/": str,
            "TERM": str,
            "Saleman": str,
            "Cost": float,
            "RATE VALID": datetime,
            "S/R": float,
            "Remark": str,
        }

        # throw error with missing columns
        columns_missing = []
        for target in target_columns.keys():
            if target not in df.columns:
                columns_missing.append(target)
        if len(columns_missing) > 0:
            raise ValueError("Missing columns %s", ", ".join(columns_missing))

        # loop all column data to check data type
        for column in df.columns:
            column_type = target_columns[column]
            column_values = df[column].tolist()

            # check all values of current column
            for value in column_values:
                # if value is not blank and type mismatch, try parsing (i.e. datetime from int)
                if not value == "" and not column_type == type(value):
                    column_type(value)

    except Exception as e:
        print(e)
        return False
    return True


print("Valid" if is_csv_valid(xlsx_name, "xlsx") else "Invalid")
