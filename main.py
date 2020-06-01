#!/usr/bin/env python3

import os

from metrika.db.initialization import init_db

DEFAULT_DB_NAME = 'db/data.db'


def main():
    if not os.path.exists(DEFAULT_DB_NAME):
        init_db(db_name=DEFAULT_DB_NAME)
    else:
        # TODO everything else
        pass


if __name__ == '__main__':
    main()
