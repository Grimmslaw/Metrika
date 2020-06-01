from dataclasses import dataclass
from urllib.request import pathname2url

import sqlalchemy as sql
from sqlalchemy import Table


@dataclass
class TypesTables:

    food_t: Table
    rating_t: Table
    time_t: Table
    weight_t: Table


def _init_create_types_tables(engine, metadata: sql.MetaData) -> TypesTables:
    food_type = sql.Table('FOOD_TYPE', metadata,
                          sql.Column('ID', sql.Integer, primary_key=True),
                          sql.Column('NAME', sql.String, nullable=False),)
    rating_type = sql.Table('RATING_TYPE', metadata,
                            sql.Column('ID', sql.Integer, primary_key=True),
                            sql.Column('NAME', sql.String, nullable=False),)
    time_type = sql.Table('TIME_TYPE', metadata,
                          sql.Column('ID', sql.Integer, primary_key=True),
                          sql.Column('NAME', sql.String, nullable=False),)
    weight_type = sql.Table('WEIGHT_TYPE', metadata,
                            sql.Column('ID', sql.Integer, primary_key=True),
                            sql.Column('NAME', sql.String, nullable=False),)
    metadata.create_all(engine)
    return TypesTables(food_type, rating_type, time_type, weight_type)


def _init_insert_into_types_tables(conn, food_types: sql.Table, rating_types: sql.Table,
                                   time_types: sql.Table, weight_types: sql.Table):
    conn.execute(food_types.insert(), [
        {'NAME': 'FULL_MEALS'},
        {'NAME': 'SNACKS'},
        {'NAME': 'SODAS'},
        {'NAME': 'ALCOHOL'},
        {'NAME': 'DESSERTS'},
    ])

    conn.execute(rating_types.insert(), [
        {'NAME': 'MORNING_MOOD'},
        {'NAME': 'NIGHT_MOOD'},
        {'NAME': 'ACTIVITY'},
    ])

    conn.execute(time_types.insert(), [
        {'NAME': 'WAKE'},
        {'NAME': 'BED_OUT'},
        {'NAME': 'BED_IN'},
        {'NAME': 'SLEEP'},
    ])

    conn.execute(weight_types.insert(), [
        {'NAME': 'MORNING_PRE'},
        {'NAME': 'MORNING_POST'},
        {'NAME': 'NIGHT'},
    ])


def _init_entry_tables(engine, metadata: sql.MetaData) -> None:
    day_entry = sql.Table('DAY_ENTRY', metadata,
                          sql.Column('ID', sql.Integer, primary_key=True),
                          sql.Column('DATE_VAL', sql.Integer, nullable=False),)
    food_entry = sql.Table('FOOD_ENTRY', metadata,
                           sql.Column('ID', sql.Integer, primary_key=True),
                           sql.Column('TYPE_ID', sql.Integer, sql.ForeignKey('FOOD_TYPE.ID'), nullable=False),
                           sql.Column('DAY_ID', sql.Integer, sql.ForeignKey('DAY_ENTRY.ID'), nullable=False),
                           sql.Column('MEAL_COUNT', sql.Integer),
                           sql.Column('CALORIES', sql.Numeric),
                           sql.Column('DESCRIPTION', sql.Text),)
    rating_entry = sql.Table('RATING_ENTRY', metadata,
                             sql.Column('ID', sql.Integer, primary_key=True),
                             sql.Column('TYPE_ID', sql.Integer, sql.ForeignKey('RATING_TYPE.ID'), nullable=False),
                             sql.Column('DAY_ID', sql.Integer, sql.ForeignKey('DAY_ENTRY.ID'), nullable=False),
                             sql.Column('RATING', sql.Numeric, nullable=False),)
    time_entry = sql.Table('TIME_ENTRY', metadata,
                           sql.Column('ID', sql.Integer, primary_key=True),
                           sql.Column('TYPE_ID', sql.Integer, sql.ForeignKey('TIME_TYPE.ID'), nullable=False),
                           sql.Column('DAY_ID', sql.Integer, sql.ForeignKey('DAY_ENTRY.ID'), nullable=False),
                           sql.Column('EVENT_TIME', sql.Text, nullable=False),)
    weight_entry = sql.Table('WEIGHT_ENTRY', metadata,
                             sql.Column('ID', sql.Integer, primary_key=True),
                             sql.Column('TYPE_ID', sql.Integer, sql.ForeignKey('WEIGHT_TYPE.ID'), nullable=False),
                             sql.Column('DAY_ID', sql.Integer, sql.ForeignKey('DAY_ENTRY.ID'), nullable=False),
                             sql.Column('WEIGHT', sql.Numeric, nullable=False),)
    metadata.create_all(engine)


def init_db(db_name: str) -> None:
    db_uri = f'sqlite:///{pathname2url(db_name)}'
    with sql.create_engine(db_uri, echo=True) as engine:
        metadata = sql.MetaData()
        types_tables = _init_create_types_tables(engine, metadata)
        _init_insert_into_types_tables(engine.connect(),
                                       types_tables.food_t, types_tables.rating_t,
                                       types_tables.time_t, types_tables.weight_t)
        _init_entry_tables(engine, metadata)
