#!/usr/bin/env python

import grpc
import ships_model_pb2
import ships_model_pb2_grpc
from google.protobuf.json_format import MessageToDict

import argparse
from pydantic import BaseModel, Field, ValidationError

import enum
import sys
import json

import psycopg2
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, create_engine, Table, UniqueConstraint, text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import OperationalError

Base = declarative_base()


class Alignment(enum.IntEnum):
    ALLY = 0
    ENEMY = 1


class ShipClass(enum.IntEnum):
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


class SpaceshipP(BaseModel):
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
            ShipClass.DESTROYER: {'min_length': 800, 'max_length': 2000, 'min_crew': 50, 'max_crew': 80,
                                   'alignment': 'ALLY'},
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

        return cls.validate_constraints(instance)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["alignment"] = self.alignment.name
        data["ship_class"] = self.ship_class.name
        return data


spaceship_officer_association = Table(
    "spaceship_officer",
    Base.metadata,
    Column("spaceship_id", Integer, ForeignKey("spaceships.id"), primary_key=True),
    Column("officer_id", Integer, ForeignKey("officers.id"), primary_key=True),
    UniqueConstraint("spaceship_id", "officer_id", name="unique_spaceship_officer")
)


class SpaceshipDB(Base):
    __tablename__ = "spaceships"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    alignment = Column(Enum(Alignment, name="alignment_enum"), nullable=False)
    ship_class = Column(Enum(ShipClass, name="ship_class_enum"), nullable=False)
    length = Column(Integer, nullable=False)
    crew_size = Column(Integer, nullable=False)
    armed = Column(Boolean, default=False)

    officers = relationship("OfficerDB", secondary=spaceship_officer_association, back_populates="ships")

    def __repr__(self):
        return f"<Spaceship(name={self.name}, alignment={self.alignment.name}, ship_class={self.ship_class.name})>"


class OfficerDB(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    rank = Column(String, nullable=False)

    ships = relationship("SpaceshipDB", secondary=spaceship_officer_association, back_populates="officers")

    def __repr__(self):
        return f"first_name: {self.first_name}, last_name: {self.last_name}, rank: {self.rank}"


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
        ships = []
        for spaceship in response:
            ship = ship_to_dict(spaceship)
            try:
                valid_ship = SpaceshipP.model_validate(ship).model_dump()
                print(json.dumps(valid_ship, indent=2))
                ships.append(valid_ship)
            except ValidationError:
                print(f"Invalid spaceship data")
            except ValueError as e:
                print(e)
    return ships


def spaceship_to_db(session, ship_data):
    ship_data["alignment"] = Alignment[ship_data["alignment"]]
    ship_data["ship_class"] = ShipClass[ship_data["ship_class"]]

    officers_data = ship_data.pop('officers')

    existing_ship = (
        session.query(SpaceshipDB)
        .filter_by(name=ship_data["name"],
                   alignment=ship_data["alignment"],
                   ship_class=ship_data['ship_class'],
                   length=ship_data['length'])
        .first()
    )

    if existing_ship:
        spaceship = existing_ship
    else:
        spaceship = SpaceshipDB(**ship_data)
        session.add(spaceship)
        session.flush()

    for officer_data in officers_data:
        officer = (session.query(OfficerDB).filter_by(
            first_name=officer_data["first_name"],
            last_name=officer_data["last_name"],
            rank=officer_data["rank"]
        )
            .first()
        )

        if not officer:
            officer = OfficerDB(**officer_data)
            session.add(officer)
            session.flush()

        if officer not in spaceship.officers:
            spaceship.officers.append(officer)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def map_ships_to_db(session, ships):
    for ship in ships:
        spaceship_to_db(session, ship)


def create_db():
    db_name = "spaceship_db"
    user = "postgres"
    password = "password"
    host = "localhost"

    engine = create_engine(f"postgresql://{user}:{password}@{host}/postgres")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 FROM pg_database WHERE datname='spaceship_db'"))
        db_exists = result.scalar()
    connection.close()

    if not db_exists:
        try:
            conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
            conn.set_session(autocommit=True)
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE {db_name};')
            conn.close()
        except OperationalError as e:
            print(e)


def mark_traitors(session):
    traitors = (session.query(OfficerDB)
                .join(spaceship_officer_association)
                .join(SpaceshipDB)
                .group_by(OfficerDB.id)
                .having(func.count(SpaceshipDB.alignment.distinct()) > 1)
                .all())

    traitors_list = []
    for officer in traitors:
        officer.traitor = True
        traitors_list.append({
            "first_name": officer.first_name,
            "last_name": officer.last_name,
            "rank": officer.rank
        })
    for traitor in traitors_list:
        print(json.dumps(traitor))


def dump_dbs(session):
    print('Spaceships:----------------------------')
    for i in session.query(SpaceshipDB).all():
        print(i)
    print('Officers:----------------------------')
    for j in session.query(OfficerDB).all():
        print(j)
    print('Relations:-------------------')
    for r in session.execute(spaceship_officer_association.select()).fetchall():
        print(r)


def main():
    parser = argparse.ArgumentParser(description="Spaceship reporting client v3(scan and list traitors")
    subparser = parser.add_subparsers(dest='command', required=True)

    scan_parser = subparser.add_parser('scan', help='Scan a region and store results')
    scan_parser.add_argument('coordinates', nargs='+', help='target location coordinates')

    subparser.add_parser('list_traitors', help='Outputs list of traitors in scanned data')

    args = parser.parse_args()

    create_db()
    engine = create_engine("postgresql://postgres:password@localhost/spaceship_db")
    Base.metadata.create_all(engine)

    session_local = sessionmaker(bind=engine)
    session = session_local()

    if args.command == 'scan':
        ra, dec = parse_coordinates(args.coordinates)
        map_ships_to_db(session, request_ships_in_coordinates(ra, dec))
    elif args.command == 'list_traitors':
        # mark_traitors(session)
        dump_dbs(session)

if __name__ == '__main__':
    main()
