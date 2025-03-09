#!/usr/bin/env python

from interface import start_test


def main():
    """
    Starts Voight-Kampff Test.
    :return: None
    """
    try:
        start_test()
    except Exception as e:
        print('Aborting...')
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
