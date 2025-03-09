import threading
import random
import time


class Screwdriver(object):
    def __init__(self):
        self.lock = threading.Lock()


class Doctor(threading.Thread):
    def __init__(self, number: int, left_screwdriver, right_screwdriver):
        super().__init__()
        self.name: str = 'Doctor ' + str(number)
        self.left_screwdriver = left_screwdriver
        self.right_screwdriver = right_screwdriver

    def think(self):
        time.sleep(random.uniform(1, 2))

    def blast(self):
        print(f'{self.name}: BLAST!')
        time.sleep(random.uniform(1, 2))

    def take_screwdrivers(self):
        while True:
            left_taken = self.left_screwdriver.lock.acquire(timeout=1)
            if left_taken:
                right_taken = self.right_screwdriver.lock.acquire(timeout=1)
                if right_taken:
                    break
                else:
                    self.left_screwdriver.lock.release()
                    time.sleep(random.uniform(0.1, 1))
            else:
                time.sleep(random.uniform(0.1, 1))

    def give_screwdrivers(self):
        self.left_screwdriver.lock.release()
        self.right_screwdriver.lock.release()

    def run(self):
        # while True: #uncomment to run more iterations
        self.think()
        self.take_screwdrivers()
        self.blast()
        self.give_screwdrivers()


def main():
    number_of_doctors = 5
    screwdrivers = [Screwdriver() for _ in range(number_of_doctors)]
    doctors = []

    for i in range(number_of_doctors):
        left_screwdriver = screwdrivers[i]
        right_screwdriver = screwdrivers[(i + 1) % number_of_doctors]
        doctor = Doctor(9 + i, left_screwdriver=left_screwdriver, right_screwdriver=right_screwdriver)
        doctors.append(doctor)
        doctor.start()

    for doctor in doctors:
        doctor.join()


if __name__ == '__main__':
    main()
