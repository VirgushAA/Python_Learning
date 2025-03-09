#!/usr/bin/env python

import grpc
import ships_model_pb2
import ships_model_pb2_grpc
from google.protobuf.json_format import MessageToDict
import sys
import json


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


def order_json(ship):
    ship_dict = MessageToDict(
        ship,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
        use_integers_for_enums=False
    )

    ordered_keys = ["name", "alignment", "ship_class", "length", "crew_size", "armed", "officers"]
    ordered_ship_dict = {key: ship_dict[key] for key in ordered_keys if key in ship_dict}
    return json.dumps(ordered_ship_dict, indent=2)


def request_ships_in_coordinates(ra, dec):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ships_model_pb2_grpc.SpaceshipServiceStub(channel)
        request = ships_model_pb2.CoordinateRequest(ra=ra, dec=dec)
        response = stub.GetShips(request)
        for ship in response:
            print(order_json(ship))


def main():
    ra, dec = parse_coordinates(sys.argv[1:])
    request_ships_in_coordinates(ra, dec)


if __name__ == '__main__':
    main()
