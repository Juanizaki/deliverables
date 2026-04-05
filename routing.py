# student id: 011028882

# routing module: EDF (Earliest Deadline First) with Nearest Neighbor tiebreaker

import datetime
from hash_table import HashTable
from package import Package
from truck import Truck
from distance import get_distance
from parse_csv import parse_csv

HUB: str = "4001 S 700 E"

# package constraint constants
TRUCK2_ONLY: set[int] = {3, 18, 36, 38}
PACKAGE9_ID: int = 9
PACKAGE9_CORRECT_ADDRESS: str = "410 S State St"
PACKAGE9_CORRECT_ZIP: int = 84111

# static truck loading assignments
# truck 1: early-deadline packages + central/east EOD packages (departs 8:00 AM)
TRUCK1_IDS: set[int] = {1, 2, 4, 5, 8, 10, 26, 29, 30, 33, 37, 40}
# truck 2: truck-2-only + co-delivery group + south/southeast EOD packages (departs 8:00 AM)
TRUCK2_IDS: set[int] = {3, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 34, 36, 38}
# truck 3: delayed packages + wrong-address package 9 + west/south EOD packages (departs 9:05 AM)
TRUCK3_IDS: set[int] = {6, 7, 9, 12, 17, 23, 24, 25, 27, 28, 31, 32, 35, 39}


def load_packages(packages_path: str) -> HashTable:
    table = HashTable()
    # parse each csv row directly into a Package object and insert it by package ID
    for row in parse_csv(packages_path):
        table.insert(
            int(row[0]),
            Package(
                package_id=int(row[0]),
                address=row[1].strip(),
                city=row[2].strip(),
                state=row[3].strip(),
                zip=int(row[4]),
                delivery_deadline=row[5].strip(),
                weight_kg=int(row[6]),
                # guard against rows that are missing the notes column
                delivery_note=row[7].strip() if len(row) > 7 else "",
            ),
        )
    return table


def assign_packages(
    package_table: HashTable,
    truck1: Truck,
    truck2: Truck,
    truck3: Truck,
) -> None:
    # map each truck to its pre-determined set of package IDs and load them
    for truck, pkg_ids in {
        truck1: TRUCK1_IDS,
        truck2: TRUCK2_IDS,
        truck3: TRUCK3_IDS,
    }.items():
        for pkg_id in pkg_ids:
            pkg = package_table.lookup(pkg_id)
            # stamp the truck's departure time so status_check knows when this package left the hub
            # the hash table holds a reference to the same object, so no re-insert is needed
            pkg.departure_time = truck.departure_time
            truck.package_list.append(pkg)


def edf_next_stop(
    remaining: list[Package],
    current_address: str,
    date: datetime.date,
    current_time: datetime.datetime,
    correction_time: datetime.datetime,
) -> Package:
    # exclude package 9 while its address is still wrong; fall back to all remaining if needed
    candidates = [
        p
        for p in remaining
        if not (p.package_id == PACKAGE9_ID and current_time < correction_time)
    ] or remaining
    # tuple key: deadline is primary (EDF), distance is the tiebreaker (nearest neighbor)
    # tuples compared left to right, so distance only matters when deadlines are equal
    return min(
        candidates,
        key=lambda p: (
            p.deadline_datetime(date),
            get_distance(current_address, p.address),
        ),
    )


def travel_to(truck: Truck, destination: str, current_address: str) -> str:
    # compute the leg distance and advance the truck's clock and odometer accordingly
    distance = get_distance(current_address, destination)
    truck.current_time += datetime.timedelta(hours=distance / truck.speed)
    truck.distance_traveled += distance
    # record a (timestamp, cumulative_miles) snapshot for point-in-time mileage queries
    truck.mileage_log.append((truck.current_time, truck.distance_traveled))
    # return destination so the caller can update current_address in one assignment
    return destination


def simulate_truck(
    truck: Truck,
    date: datetime.date,
    correction_time: datetime.datetime,
) -> None:
    truck.current_time = truck.departure_time
    current_address = HUB
    # copy the package list so we can remove entries as packages are delivered
    # without modifying the truck's original list, which the CLI reads later
    remaining = list(truck.package_list)
    # flag prevents re-scanning for package 9 after its address has already been corrected
    pkg9_corrected = False
    while remaining:
        # apply package 9 address correction once the correction time is reached
        if not pkg9_corrected and truck.current_time >= correction_time:
            for pkg in remaining:
                if pkg.package_id == PACKAGE9_ID:
                    pkg.address = PACKAGE9_CORRECT_ADDRESS
                    pkg.zip = PACKAGE9_CORRECT_ZIP
                    pkg9_corrected = True
                    break
        # select the next package to deliver using EDF with nearest neighbor tiebreaker
        next_pkg = edf_next_stop(
            remaining, current_address, date, truck.current_time, correction_time
        )
        # drive to the package's address; truck.current_time is now the arrival time
        current_address = travel_to(truck, next_pkg.address, current_address)
        # stamp the delivery time directly on the package object
        next_pkg.delivery_time = truck.current_time
        remaining.remove(next_pkg)
    # return to hub after all deliveries are complete
    travel_to(truck, HUB, current_address)


def run_simulation(
    truck1: Truck, truck2: Truck, truck3: Truck, date: datetime.date
) -> None:
    # package 9's correct address becomes known at 10:20 AM per the scenario spec
    correction_time = datetime.datetime(date.year, date.month, date.day, 10, 20)
    # simulate each truck sequentially; routes are independent so order does not affect results
    for truck in (truck1, truck2, truck3):
        simulate_truck(truck, date, correction_time)
