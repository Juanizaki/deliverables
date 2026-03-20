# class defining package objects


class Package:
    delivery_statuses: list[str] = ["pending", "in progress", "delivered"]
    EOD: str = "10:00 PM"

    def __init__(
        self,
        package_id: int,
        address: str,
        city: str,
        state: str,
        zip_code: int,
        delivery_deadline: str,
        weight_kg: int,
        delivery_status: str,
        delivery_note: str,
    ) -> None:
        self.package_id: int = package_id
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip_code: int = zip_code
        self.delivery_deadline: str = delivery_deadline
        self.weight_kg: int = weight_kg
        self.delivery_status: str = delivery_status
        self.delivery_note: str = delivery_note

    def __str__(self):
        return (
            f"{self.package_id}, "
            f"{self.address}, "
            f"{self.city}, "
            f"{self.state}, "
            f"{self.zip_code}, "
            f"{self.delivery_deadline}, "
            f"{self.weight_kg}, "
            f"{self.delivery_status}, "
            f"{self.delivery_note}"
        )

    def __repr__(self):
        return (
            f"Package ID: {self.package_id!r}, "
            f"Address: {self.address!r}, "
            f"City: {self.city!r}, "
            f"State: {self.state!r}, "
            f"Zip Code: {self.zip_code!r}, "
            f"Delivery Deadline: {self.delivery_deadline!r}, "
            f"Weight (kg): {self.weight_kg!r}, "
            f"Delivery Status: {self.delivery_status!r}, "
            f"Delivery Note: {self.delivery_note!r}"
        )


# testing
# package1: Package = Package(
#     1,
#     "123 Main St",
#     "Salt Lake City",
#     "UT",
#     84115,
#     "10:00 am",
#     10,
#     "pending",
#     "on time",
# )
# package2: Package = Package(
#     2,
#     "321 Third St",
#     "Salt Lake City",
#     "UT",
#     84106,
#     "11:00 am",
#     12,
#     "pending",
#     "delayed",
# )
#
# print(repr(package1))
# print(package2)
