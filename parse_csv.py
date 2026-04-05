# student id: 011028882

# utility for reading csv files into Python lists

import csv


def parse_csv(csv_file: str) -> list:
    # reads a csv file and returns its rows as a list of string lists
    # utf-8-sig strips the byte-order mark that Excel may prepend to csv files
    # newline="" lets the csv module handle line endings correctly
    with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.reader(file))
