import redis
import json
import random
import logging


def create_account_number() -> int:
    first_digit = random.randint(1, 9)  # Ensure the first digit is between 1 and 9
    remaining_digits = [random.randint(0, 9) for _ in range(9)]  # Next 9 digits can be 0-9
    account_number = str(first_digit) + ''.join(map(str, remaining_digits))
    return int(account_number)


def create_amount() -> int:
    amount = random.randrange(1000, 10001, 1000)

    if random.choice([False, False, True, False]):
        amount = -amount

    return amount


def create_message(acc_number1, acc_number2, amount):
    data = {'metadata': {"from": acc_number1, "to": acc_number2},
            "amount": amount}
    json_message = json.dumps(data)
    return json_message


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    r = redis.Redis(host='localhost', port=6379, db=0)
    r.publish('my_chanel', create_message(1111111111, 2222222222, 10000))
    r.publish('my_chanel', create_message(3333333333, 4444444444, -3000))
    r.publish('my_chanel', create_message(2222222222, 5555555555, 5000))
    # iterations = 10
    # while iterations:
    #     message = create_message(create_account_number(), create_account_number(), create_amount())
    #     r.publish('my_chanel', message)
    #     logging.info(f'generated message: {message}')
    #     iterations -= 1
