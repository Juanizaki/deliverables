# student id: 011028882

import datetime

from distance import load_distance_data
from hash_table import HashTable
from routing import (
    assign_packages,
    load_packages,
    run_simulation,
)
from truck import Truck


def parse_time_input(time: str, date: datetime.date) -> datetime.datetime | None:
    # .upper() normalizes lowercase "am"/"pm" so both "9:00 AM" and "9:00 am" are accepted
    # two formats are tried to handle input with or without a space before AM/PM
    for fmt in ("%I:%M %p", "%I:%M%p"):
        try:
            parsed = datetime.datetime.strptime(time.upper(), fmt)
            # combine the parsed time with today's date to produce a full datetime
            return datetime.datetime.combine(date, parsed.time())
        except ValueError:
            continue
    return None


def mileage_at_time(truck: Truck, query_time: datetime.datetime) -> float:
    # truck has not departed yet or has no recorded legs; nothing to report
    if query_time < truck.departure_time or not truck.mileage_log:
        return 0.0
    # walk the log in reverse so the first match at or before query_time is the correct entry
    for timestamp, cumulative in reversed(truck.mileage_log):
        if timestamp <= query_time:
            return cumulative
    return 0.0


def display_delivery_summary(
    package_table: HashTable,
    truck1: Truck,
    truck2: Truck,
    truck3: Truck,
    query_time: datetime.datetime,
    pkg_id: int | None = None,
) -> None:
    print(f"\nPackage status at {query_time.strftime('%I:%M %p')}:")
    print("-" * 125)
    print(
        f"  {'ID':<4} {'Address':<40} {'City':<18} {'Zip':<7} {'Weight(kg)':<12} {'Deadline':<10} {'Status'}"
    )
    print("-" * 125)
    # when pkg_id is provided show only that package; otherwise iterate all 40
    for pid in ([pkg_id] if pkg_id is not None else range(1, 41)):
        pkg = package_table.lookup(pid)
        if pkg is None:
            print(f"  Package {pid} not found")
            continue
        # status_check derives the current state from the package's recorded timestamps
        print(
            f"  {pid:<4} {pkg.address:<40} {pkg.city:<18} {pkg.zip:<7} {pkg.weight_kg:<12} {pkg.delivery_deadline:<10} {pkg.status_check(query_time)}"
        )
    print("-" * 125)
    # compute per-truck and total mileage at the query time from each truck's mileage log
    miles = [mileage_at_time(t, query_time) for t in (truck1, truck2, truck3)]
    for i, m in enumerate(miles, 1):
        print(f"  Truck {i}: {m:.1f} miles")
    print(
        f"  Total mileage at {query_time.strftime('%I:%M %p')}: {sum(miles):.1f} miles"
    )


def prompt_time(date: datetime.date) -> datetime.datetime | None:
    # wraps parse_time_input with user-facing input and an inline validation message
    query_time = parse_time_input(
        input("\nEnter time (e.g. 9:00 AM, 10:30 AM): ").strip(), date
    )
    if query_time is None:
        print("\nInvalid format. Use HH:MM AM/PM (e.g. 9:00 AM)\n")
    return query_time


def cli_loop(
    package_table: HashTable,
    truck1: Truck,
    truck2: Truck,
    truck3: Truck,
    date: datetime.date,
) -> None:
    print("\n=== WGUPS Package Routing System ===")
    # KeyboardInterrupt (Ctrl+C) is caught so the program exits cleanly
    try:
        while True:
            print(
                "\n  1. View delivery summary for a single package at a specific time"
                "\n  2. View delivery summary at a specific time"
                "\n  3. View final delivery summary"
                "\n  4. Exit"
            )
            choice = input("\nEnter choice: ").strip()
            if choice == "4":
                print("\nExiting...")
                break
            elif choice == "1":
                # prompt for time first, then validate the package ID before displaying
                query_time = prompt_time(date)
                if query_time is None:
                    continue
                try:
                    id_input = int(
                        input("\nEnter package ID to check status (1-40): ").strip()
                    )
                except ValueError:
                    print("\nInvalid package ID\n")
                    continue
                package = package_table.lookup(id_input)
                if package is None:
                    print("\nPackage not found\n")
                    continue
                display_delivery_summary(
                    package_table, truck1, truck2, truck3, query_time, id_input
                )
            elif choice == "2":
                # prompt for time first, then display delivery summary for all packages
                query_time = prompt_time(date)
                if query_time is None:
                    continue
                display_delivery_summary(
                    package_table, truck1, truck2, truck3, query_time
                )
            elif choice == "3":
                # use 10:00 PM as EOD, then display final delivery summary for all packages
                end_of_day = datetime.datetime.combine(date, datetime.time(22, 0))
                display_delivery_summary(
                    package_table, truck1, truck2, truck3, end_of_day
                )
            else:
                print("  Invalid choice. Enter 1, 2, or 3\n")
    except KeyboardInterrupt:
        print("\nExiting...")


def main() -> None:
    # phase 1: load all data and run the full-day simulation
    # run from project root so relative data paths resolve correctly
    load_distance_data("data/addresses.csv", "data/distances.csv")
    package_table = load_packages("data/packages.csv")
    # use today's date so departure times are anchored to a real calendar date
    date = datetime.date.today()
    depart_0800 = datetime.datetime.combine(date, datetime.time(8, 0))
    depart_0905 = datetime.datetime.combine(date, datetime.time(9, 5))
    truck1 = Truck(truck=1, driver="Juan", departure_time=depart_0800)
    truck2 = Truck(truck=2, driver="Tony", departure_time=depart_0800)
    # Juan drives truck 1 first and returns to the hub in time for the 9:05 AM departure for truck 3
    truck3 = Truck(truck=3, driver="Juan", departure_time=depart_0905)
    assign_packages(package_table, truck1, truck2, truck3)
    # simulation must complete before the CLI starts; all delivery times are set here
    run_simulation(truck1, truck2, truck3, date)
    # phase 2: launch the CLI — no further simulation occurs from this point
    cli_loop(package_table, truck1, truck2, truck3, date)


if __name__ == "__main__":
    main()
