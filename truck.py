# class defining truck objects
from package import Package
from parse_csv import ParseCSV


class Truck:
    available_trucks: list[int] = [1, 2, 3]
    available_drivers: list[str] = ["Juan", "Tony"]

    def __init__(
        self,
        truck: int,
        driver: str,
        package_load: int,
        package_list: list[Package],
        current_location: str,
        distance_traveled: int,
    ) -> None:
        self.truck: int = truck
        self.driver: str = driver
        self.package_max_load: int = 16  # total number of packages a truck can carry
        self.package_load: int = package_load  # number of packages on the truck
        self.package_list: list[Package] = package_list
        self.current_location: str = current_location
        self.next_location = None
        self.distance_traveled: int = distance_traveled
        self.speed: int = 18

    def __str__(self) -> str:
        return (
            f"{self.truck}\n"
            f"{self.driver}\n"
            f"{self.package_max_load}\n"
            f"{self.package_load}\n"
            f"{self.package_list}\n"
            f"{self.current_location}\n"
            f"{self.next_location}\n"
            f"{self.distance_traveled}\n"
            f"{self.speed}\n"
        )

    def __repr__(self) -> str:
        return (
            f"Truck: {self.truck!r}\n"
            f"Driver: {self.driver!r}\n"
            f"Package Max Load: {self.package_max_load!r}\n"
            f"Package Load: {self.package_load!r}\n"
            f"Package List: {self.package_list!r}\n"
            f"Current Location: {self.current_location!r}\n"
            f"Next Location: {self.next_location!r}\n"
            f"Distance Traveled: {self.distance_traveled!r}\n"
            f"Speed: {self.speed!r}\n"
        )


# testing
# truck1 = Truck(
#     truck=Truck.available_trucks[0],
#     driver=Truck.available_drivers[0],
#     package_load=10,
#     package_list=ParseCSV.parse_csv("data/packages.csv"),
#     current_location="Hub",
#     distance_traveled=0,
# )
#
# truck2 = Truck(
#     truck=Truck.available_trucks[1],
#     driver=Truck.available_drivers[1],
#     package_load=8,
#     package_list=[],
#     current_location="Hub",
#     distance_traveled=0,
# )
#
# print(repr(truck1))
# print(truck2)
