import logging

from parser_dentalia import dentalia
from parser_santaelena import santaelena
from parser_yapdomik import yapdomik


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    dentalia()
    yapdomik()
    santaelena()


if __name__ == '__main__':
    main()
