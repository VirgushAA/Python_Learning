#!/usr/bin/env python

import grpc
import ships_model_pb2
import ships_model_pb2_grpc
from google.protobuf.json_format import MessageToDict
from enum import IntEnum
from pydantic import BaseModel, Field, ValidationError
import sys
import warnings


class Alignment(IntEnum):
    ALLY = 0
    ENEMY = 1


class ShipClass(IntEnum):
    CORVETTE = 0
    FRIGATE = 1
    CRUISER = 2
    DESTROYER = 3
    CARRIER = 4
    DREADNOUGHT = 5


class Officer(BaseModel):
    first_name: str
    last_name: str
    rank: str


class Spaceship(BaseModel):
    name: str
    alignment: Alignment
    ship_class: ShipClass
    length: int = Field(..., ge=80, le=20000)
    crew_size: int = Field(..., ge=4, le=500)
    armed: bool
    officers: list[Officer]

    @classmethod
    def validate_constraints(cls, values):
        name = values.name
        alignment = values.alignment
        ship_class = values.ship_class
        length = values.length
        crew_size = values.crew_size
        armed = values.armed

        constraints = {
            ShipClass.CORVETTE: {'min_length': 80, 'max_length': 250, 'min_crew': 4, 'max_crew': 10},
            ShipClass.FRIGATE: {'min_length': 300, 'max_length': 600, 'min_crew': 10, 'max_crew': 15},
            ShipClass.CRUISER: {'min_length': 500, 'max_length': 1000, 'min_crew': 15, 'max_crew': 30},
            ShipClass.DESTROYER: {'min_length': 800, 'max_length': 2000, 'min_crew': 50, 'max_crew': 80},
            ShipClass.CARRIER: {'min_length': 1000, 'max_length': 4000, 'min_crew': 120, 'max_crew': 250},
            ShipClass.DREADNOUGHT: {'min_length': 5000, 'max_length': 20000, 'min_crew': 300, 'max_crew': 500}
        }

        if length > constraints[ship_class]['max_length'] or length < constraints[ship_class]['min_length']:
            raise ValueError(f"Invalid length {length} for ship class {ship_class.name}")
        if crew_size > constraints[ship_class]['max_crew'] or crew_size < constraints[ship_class]['min_crew']:
            raise ValueError(f"Invalid cre size {crew_size} for ship class {ship_class.name}")
        if ship_class == ShipClass.CARRIER and armed is True:
            raise ValueError(f"Carriers cant be armed")
        if ship_class == ShipClass.FRIGATE and alignment == Alignment.ENEMY:
            raise ValueError("Enemies have no frigate class ships")
        if ship_class == ShipClass.DESTROYER and alignment == Alignment.ENEMY:
            raise ValueError(f"Enemies have no destroyer class ships")
        if alignment != Alignment.ENEMY and name.lower() == 'unknown':
            raise ValueError("Only enemy ships names can be unknown")

        return values

    @classmethod
    def model_validate(cls, values):

        values["alignment"] = Alignment(values["alignment"]) if isinstance(values["alignment"], int) else Alignment[
            values["alignment"]]
        values["ship_class"] = ShipClass(values["ship_class"]) if isinstance(values["ship_class"], int) else ShipClass[
            values["ship_class"]]

        instance = super().model_validate(values)
        ret = cls.validate_constraints(instance)

        ret.alignment = ret.alignment.name
        ret.ship_class = ret.ship_class.name

        return ret


def normalize_text(text):
    """Normalize text to prevent Unicode formatting issues"""
    text = text.replace("−", "-")  # U+2212 (minus sign)
    text = text.replace(" ", " ")  # U+2009 (thin space)
    text = text.replace("–", "-")  # U+2013 (en dash)
    text = text.replace("—", "-")  # U+2014 (em dash)
    text = text.replace("\u200b", "")  # U+200B (zero width space)
    text = text.replace("\u200c", "")  # U+200C (zero width non-joiner)
    text = text.replace("\u200d", "")  # U+200D (zero width joiner)
    text = text.replace("\ufeff", "")  # BOM (Byte Order Mark)
    return text


def normalize_args(args):
    text: str = ''
    for arg in args:
        text += arg + ' '
    text = normalize_text(text)
    args = text.split()

    return args


def parse_ra(ra_str):
    """Modify radiant ascension into number"""
    hours, minutes, seconds = map(float, ra_str.split(":"))
    return (hours * 15) + (minutes * 15 / 60) + (seconds * 15 / 3600)


def parse_dec(dec_str):
    """Modify declination into number"""
    degrees, minutes, seconds = map(float, dec_str.split(":"))
    return degrees + (minutes / 60) + (seconds / 3600)


def parse_coordinates(args):
    try:
        args = normalize_args(args)
        if len(args) == 2:
            ra_str, dec_str = args[1], args[2]
        elif len(args) == 6:
            ra_str = f"{args[0]}:{args[1]}:{args[2]}"
            dec_str = f"{args[3]}:{args[4]}:{args[5]}"
        else:
            raise ValueError("Invalid number of arguments")

        ra = parse_ra(ra_str)
        dec = parse_dec(dec_str)
        return ra, dec
    except (IndexError, ValueError):
        print("Usage: reporting_client.py HH:MM:SS DD:MM:SS  OR  HH MM SS DD MM SS")
        sys.exit(1)


def ship_to_dict(ship):
    return MessageToDict(
        ship,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
        use_integers_for_enums=False
    )


def request_ships_in_coordinates(ra, dec):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ships_model_pb2_grpc.SpaceshipServiceStub(channel)
        request = ships_model_pb2.CoordinateRequest(ra=ra, dec=dec)
        response = stub.GetShips(request)
        for spaceship in response:
            ship = ship_to_dict(spaceship)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', UserWarning)
                    print(Spaceship.model_validate(ship).model_dump_json(indent=2))
            except ValidationError:
                print(f"Invalid spaceship data")
            except ValueError as e:
                print(e)


def main():
    ra, dec = parse_coordinates(sys.argv[1:])
    request_ships_in_coordinates(ra, dec)


if __name__ == '__main__':
    main()
