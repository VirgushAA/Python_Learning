import redis
import json
import logging
import argparse

parser = argparse.ArgumentParser(description='idk what description is used for')
parser.add_argument('-e', '--elements', help='list of bad guys numbers')
args = parser.parse_args()
elements = []
if args.elements:
    elements = list(map(int, args.elements.split(',')))


def process_message(msg):
    json_message = msg['data'].decode('utf-8')
    data = json.loads(json_message)
    for baddie in elements:
        if data['metadata']['to'] == baddie and data['amount'] > 0:
            data['metadata']['from'], data['metadata']['to'] = data['metadata']['to'], data['metadata'][
                'from']
    return data


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('my_chanel')

    try:
        for message in pubsub.listen():
            if message['type'] == 'message':
                logging.info(process_message(message))
    except KeyboardInterrupt:
        pubsub.unsubscribe()
        pubsub.close()
