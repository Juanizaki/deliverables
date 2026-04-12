# student id: 011028882

# class defining package objects

import datetime


class Package:

    def __init__(
        self,
        package_id: int,
        address: str,
        city: str,
        state: str,
        zip_code: int,
        delivery_deadline: str,
        weight_kg: int,
    ) -> None:
        # --- fields sourced directly from the csv ---
        self.package_id: int = package_id
        # address is mutable: package 9 address is corrected mid-simulation
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip_code: int = zip_code
        self.delivery_deadline: str = delivery_deadline
        self.weight_kg: int = weight_kg
        # --- runtime fields stamped during simulation ---
        # truck_number set by assign_packages when package is assigned to truck
        self.truck_number: int | None = None
        # arrival_time set for delayed packages not at hub at simulation start
        self.arrival_time: datetime.datetime | None = None
        # departure_time set by assign_packages when package is loaded onto a truck
        self.departure_time: datetime.datetime | None = None
        # delivery_time set by simulate_truck the moment package is delivered
        self.delivery_time: datetime.datetime | None = None
        # set on package 9 before address is corrected mid-simulation
        self.pre_correction_address: str | None = None
        self.pre_correction_zip: int | None = None
        self.correction_time: datetime.datetime | None = None

    def deadline_datetime(self, date: datetime.date) -> datetime.datetime:
        # EOD packages use 10:00 PM so any timed deadline always sorts ahead of them
        if self.delivery_deadline == "EOD":
            return datetime.datetime.combine(date, datetime.time(22, 0))
        # parse "HH:MM AM/PM" string and combine with delivery date
        time = datetime.datetime.strptime(self.delivery_deadline, "%I:%M %p")
        return datetime.datetime.combine(date, datetime.time(time.hour, time.minute))

    def status_check(self, query_time: datetime.datetime) -> str:
        # package delayed in flight and not at hub
        if self.arrival_time is not None and query_time < self.arrival_time:
            return "Delayed"
        # package at hub and has not departed
        if self.departure_time is None or query_time < self.departure_time:
            return "At Hub"
        # package departed but not at destination
        if self.delivery_time is None or query_time < self.delivery_time:
            return "In Transit"
        # package has been delivered; include the exact delivery time
        return f"Delivered at {self.delivery_time.strftime('%I:%M %p')}"

    def __str__(self):
        return (
            f"{self.package_id}, "
            f"{self.address}, "
            f"{self.city}, "
            f"{self.state}, "
            f"{self.zip_code}, "
            f"{self.delivery_deadline}, "
            f"{self.weight_kg}, "
            f"{self.departure_time}, "
            f"{self.delivery_time}"
        )
