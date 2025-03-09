#!/usr/bin/env python

import grpc
from concurrent import futures
import random
import ships_model_pb2
import ships_model_pb2_grpc
import sys
import signal

SHIP_NAMES = ["USS Enterprise", "Voyager", "Defiant", "Battlestar Galactica", "Rocinante", 'SSV Normandy']
FIRST_NAMES = ["John", "Jane", "Alex", "Stepan", "Sigizmund"]
LAST_NAMES = ["Doe", "Smith", "Duraleev", "Log", "Ivanov"]
RANKS = ["Ensign", "Lieutenant", "Commander", "Captain", "Admiral"]


class SpaceshipService(ships_model_pb2_grpc.SpaceshipServiceServicer):

    def GetShips(self, request, context):
        for _ in range(10):
            yield self.generate_ship()

    def generate_ship(self):
        ship = ships_model_pb2.Spaceship(
            name=random.choice(SHIP_NAMES),
            alignment=random.choice(list(ships_model_pb2.Alignment.values())),
            ship_class=random.choice(list(ships_model_pb2.ShipClass.values())),
            length=random.randint(80, 20000),
            crew_size=random.randint(4, 500),
            armed=random.choice([True, False]),
        )
        for _ in range(random.randint(1, 3)):
            officer = ships_model_pb2.Officer(
                first_name=random.choice(FIRST_NAMES),
                last_name=random.choice(LAST_NAMES),
                rank=random.choice(RANKS)
            )
            ship.officers.append(officer)
        return ship


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ships_model_pb2_grpc.add_SpaceshipServiceServicer_to_server(SpaceshipService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server Started on port 50051")

    def shutdown_server(sig, frame):
        print("\nShutting down gRPC server...")
        server.stop(0)
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    server.wait_for_termination()


def main():
    serve()


if __name__ == '__main__':
    main()
