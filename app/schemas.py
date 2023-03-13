#import json
from typing import Optional

#from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class TripInput(SQLModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class Trip(TripInput, table=True):
    id:  Optional[int] = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


class CarInput(SQLModel):
    size: str
    fuel: Optional[str] = "electric"
    doors: int
    transmission: Optional[str] = "auto"

    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


class Car(CarInput, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")




# def load_db() -> list[CarOutput]:
#     """Load a list of Car object from a JSON file """
#     with open("cars.json") as f:
#         return [CarOutput.parse_obj(obj) for obj in json.load(f)]
#
#
# def save_db(cars: list[CarOutput]):
#     with open('cars.json', 'w') as f:
#         json.dump([car.dict() for car in cars], f, indent=4)
