# student id: 011028882

# class defining truck objects

import datetime
from package import Package


class Truck:
    def __init__(
        self,
        truck: int,
        driver: str,
        departure_time: datetime.datetime,
    ) -> None:
        self.truck: int = truck
        self.driver: str = driver
        self.package_max_load: int = 16  # max 16 packages per truck
        self.package_list: list[Package] = []
        self.distance_traveled: float = 0.0
        # constant 18 mph used to convert distance legs into time deltas
        self.speed: int = 18
        self.departure_time: datetime.datetime = departure_time
        # current_time starts at departure and advances with each leg during runtime
        self.current_time: datetime.datetime = departure_time
        # ordered list of (timestamp, miles) entries
        # used by mileage_at_time() to answer point-in-time mileage queries
        self.mileage_log: list[tuple[datetime.datetime, float]] = []

    def __str__(self) -> str:
        return (
            f"{self.truck}\n"
            f"{self.driver}\n"
            f"{self.package_max_load}\n"
            f"{self.package_list}\n"
            f"{self.distance_traveled}\n"
            f"{self.speed}\n"
            f"{self.departure_time}\n"
        )
