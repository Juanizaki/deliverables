# class for parsing csv files

import csv


class ParseCSV:
    def __init__(self, data=None) -> None:
        self.data = data if data is not None else []

    def __str__(self) -> str:
        return str(self.data)

    @staticmethod
    def parse_csv(csv_file) -> list:
        rows = []
        with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row in reader:
                rows.append(row)
                print(row)
        return rows


# testing
# ParseCSV.parse_csv("data/addresses.csv")
# ParseCSV.parse_csv("data/distances.csv")
# ParseCSV.parse_csv("data/packages.csv")
