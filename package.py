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
        zip: int,
        delivery_deadline: str,
        weight_kg: int,
        delivery_note: str,
    ) -> None:
        # --- fields sourced directly from the csv ---
        self.package_id: int = package_id
        # address is mutable: package 9's address is corrected mid-simulation
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip: int = zip
        self.delivery_deadline: str = delivery_deadline
        self.weight_kg: int = weight_kg
        self.delivery_note: str = delivery_note
        # --- runtime fields stamped during simulation ---
        # departure_time is set by assign_packages when the package is loaded onto a truck
        self.departure_time: datetime.datetime | None = None
        # delivery_time is set by simulate_truck the moment the package is delivered
        self.delivery_time: datetime.datetime | None = None

    def deadline_datetime(self, date: datetime.date) -> datetime.datetime:
        # EOD packages use 10:00 PM so any timed deadline always sorts ahead of them
        if self.delivery_deadline == "EOD":
            return datetime.datetime(date.year, date.month, date.day, 22, 0)
        # parse the "HH:MM AM/PM" string and combine it with the delivery date
        time = datetime.datetime.strptime(self.delivery_deadline, "%I:%M %p")
        return datetime.datetime(
            date.year, date.month, date.day, time.hour, time.minute
        )

    def status_check(self, query_time: datetime.datetime) -> str:
        # package has not left the hub yet at query_time
        if self.departure_time is None or query_time < self.departure_time:
            return "At Hub"
        # package has departed but has not yet arrived at its destination
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
            f"{self.zip}, "
            f"{self.delivery_deadline}, "
            f"{self.weight_kg}, "
            f"{self.delivery_note}, "
            f"{self.departure_time}, "
            f"{self.delivery_time}"
        )
