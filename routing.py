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
DELAYED_IDS: set[int] = {6, 25, 28, 32}
DELAYED_ARRIVAL: datetime.time = datetime.time(9, 5)
PACKAGE9_ID: int = 9
PACKAGE9_CORRECT_ADDRESS: str = "410 S State St"
PACKAGE9_CORRECT_ZIP: int = 84111

# static truck loading assignments
# truck 1: early-deadline packages + central EOD packages
TRUCK1_IDS: set[int] = {1, 2, 4, 7, 8, 10, 29, 30, 33, 40}
# truck 2: truck 2 only + co-delivery group + south/southeast EOD packages
TRUCK2_IDS: set[int] = {3, 5, 11, 13, 14, 15, 16, 18, 19, 20, 21, 34, 36, 37, 38, 39}
# truck 3: delayed packages + wrong-address package 9 + west/south EOD packages
TRUCK3_IDS: set[int] = {6, 9, 12, 17, 22, 23, 24, 25, 26, 27, 28, 31, 32, 35}


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
                zip_code=int(row[4]),
                delivery_deadline=row[5].strip(),
                weight_kg=int(row[6]),
            ),
        )
    return table


def assign_packages(
    package_table: HashTable,
    truck1: Truck,
    truck2: Truck,
    truck3: Truck,
    date: datetime.date,
) -> None:
    delayed_arrival = datetime.datetime.combine(date, DELAYED_ARRIVAL)
    # map each truck to pre-determined package IDs and load them
    for truck, pkg_ids in {
        truck1: TRUCK1_IDS,
        truck2: TRUCK2_IDS,
        truck3: TRUCK3_IDS,
    }.items():
        for pkg_id in pkg_ids:
            pkg = package_table.lookup(pkg_id)
            # stamp truck departure time so status_check knows when package left hub
            # hash table holds reference to the same object, so no re-insert needed
            pkg.truck_number = truck.truck
            pkg.departure_time = truck.departure_time
            if pkg_id in DELAYED_IDS:
                pkg.arrival_time = delayed_arrival
            truck.package_list.append(pkg)


def edf_next_stop(
    remaining: list[Package],
    current_address: str,
    date: datetime.date,
    current_time: datetime.datetime,
    correction_time: datetime.datetime,
) -> Package:
    # exclude package 9 while address is wrong; fall back to all remaining if needed
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
    # compute leg distance and advance truck clock and odometer accordingly
    distance = get_distance(current_address, destination)
    truck.current_time += datetime.timedelta(hours=distance / truck.speed)
    truck.distance_traveled += distance
    # record (timestamp, miles) snapshot for point-in-time mileage queries
    truck.mileage_log.append((truck.current_time, truck.distance_traveled))
    # return destination so caller can update current_address in one assignment
    return destination


def simulate_truck(
    truck: Truck,
    date: datetime.date,
    correction_time: datetime.datetime,
) -> None:
    truck.current_time = truck.departure_time
    current_address = HUB
    # copy package list to remove entries as packages are delivered
    # without modifying truck original list, which CLI reads later
    remaining = list(truck.package_list)
    # flag prevents re-scanning for package 9 after address corrected
    pkg9_corrected = False
    while remaining:
        # apply package 9 address correction once correction time reached
        if not pkg9_corrected and truck.current_time >= correction_time:
            for pkg in remaining:
                if pkg.package_id == PACKAGE9_ID:
                    pkg.pre_correction_address = pkg.address
                    pkg.pre_correction_zip = pkg.zip_code
                    pkg.correction_time = correction_time
                    pkg.address = PACKAGE9_CORRECT_ADDRESS
                    pkg.zip_code = PACKAGE9_CORRECT_ZIP
                    pkg9_corrected = True
                    break
        # select next package to deliver using EDF with nearest neighbor tiebreaker
        next_pkg = edf_next_stop(
            remaining, current_address, date, truck.current_time, correction_time
        )
        # drive to package address; truck.current_time is now arrival time
        current_address = travel_to(truck, next_pkg.address, current_address)
        # deliver all packages at this address in one stop
        for pkg in [p for p in remaining if p.address == current_address]:
            pkg.delivery_time = truck.current_time
            remaining.remove(pkg)
    # return to hub after all deliveries are complete
    travel_to(truck, HUB, current_address)


def run_simulation(
    truck1: Truck, truck2: Truck, truck3: Truck, date: datetime.date
) -> None:
    # package 9 correct address becomes known at 10:20 AM
    correction_time = datetime.datetime.combine(date, datetime.time(10, 20))
    simulate_truck(truck1, date, correction_time)
    simulate_truck(truck2, date, correction_time)
    # truck 3 departs once Juan returns to hub
    truck3.departure_time = truck3.current_time = truck1.current_time
    for pkg in truck3.package_list:
        pkg.departure_time = truck1.current_time
    simulate_truck(truck3, date, correction_time)
