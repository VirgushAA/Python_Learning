import random
import time


def emit_gel(step):
    pressure = 21
    direction = 1
    while True:
        value = yield pressure
        if value == 'reverse':
            direction = -direction
        pressure += random.randint(0, step) * direction

        if pressure < 10 or pressure > 90:
            print('invalid pressure, stopping')
            break
        if pressure > 100:
            raise ValueError("Generated value exceeds 100, which is considered an error.")
        elif pressure < 0:
            pressure = 0


def valve(step):
    pipe = emit_gel(step)
    try:
        while True:
            value = pipe.send(None)
            if value <= 20 or value >= 80:
                pipe.send('reverse')
            yield value
    except ValueError as err:
        print(err)


if __name__ == '__main__':
    flow = valve(10)
    for _ in range(50):
        print(next(flow))
        # time.sleep(0.1)
