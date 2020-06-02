import sqlalchemy


def get_table(name: str, metadata: sqlalchemy.MetaData, bind_obj) -> sqlalchemy.Table:
    metadata.reflect(bind=bind_obj)
    return metadata.tables[name]


def get_column(name: str, table: sqlalchemy.Table = None, table_name: str = None,
               metadata: sqlalchemy.MetaData = None, bind_obj=None) -> sqlalchemy.Column:
    if table is not None:
        return table.columns[name]

    if not any(x is None for x in [table_name, metadata, bind_obj]):
        return get_table(table_name, metadata, bind_obj).columns[name]
