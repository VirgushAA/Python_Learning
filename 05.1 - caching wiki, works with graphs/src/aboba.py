import argparse
import requests
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


parser = argparse.ArgumentParser()
parser.add_argument('product', help='Starting point')
args = parser.parse_args()

wb = 'https://www.wildberrie.ru'
ozon = 'https://www.ozon.ru/highlight/blackfriday/'


def get_page():
    try:
        response = requests.get(wb + args.product)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"{e}, fuck you")
        return None
    pass


def main():

    print(args)
    print(get_page())


if __name__ == '__main__':
    main()