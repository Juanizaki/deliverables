# student id: 011028882

# distance utility: loads address index map and distance matrix from csv files

from parse_csv import parse_csv


class DistanceData:
    # groups the address index and distance matrix in one place so both
    # are loaded and accessed together without relying on module-level variables
    def __init__(self) -> None:
        self.address_index: dict[str, int] = {}
        self.matrix: list[list[float]] = []


data = DistanceData()


def load_distance_data(addresses_path: str, distances_path: str) -> None:
    address_rows = parse_csv(addresses_path)
    for row in address_rows:
        address = row[2].strip()
        # address IDs in the csv are 1-based; subtract 1 for the 0-based matrix index
        data.address_index[address] = int(row[0]) - 1
    location_count = len(address_rows)
    # initialize a square matrix filled with zeros; only the lower triangle will be populated
    data.matrix = [[0.0] * location_count for _ in range(location_count)]
    distance_rows = parse_csv(distances_path)
    # skip any completely blank rows that may appear at the end of the csv
    valid_rows = [row for row in distance_rows if any(v.strip() for v in row)]
    for i, row in enumerate(valid_rows):
        for j, value in enumerate(row):
            # the csv is lower-triangular: row i only contains values for columns 0 through i
            if value.strip():
                distance = float(value.strip())
                data.matrix[i][j] = distance


def get_distance(address_a: str, address_b: str) -> float:
    i = data.address_index[address_a]
    j = data.address_index[address_b]
    # the matrix is only filled where i >= j (lower triangle)
    # swap when j > i so we always read from a populated cell regardless of argument order
    if j > i:
        i, j = j, i
    return data.matrix[i][j]
