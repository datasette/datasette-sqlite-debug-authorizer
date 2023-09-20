from datasette import hookimpl
import sqlite3
import sys

CONSTANTS = {
    getattr(sqlite3, c): c
    for c in dir(sqlite3)
    if c.startswith("SQLITE_") and isinstance(getattr(sqlite3, c), int)
}


def print_authorizer(action, table, column, db_name, trigger_name):
    bits = ["{}: ".format(CONSTANTS.get(action, action))]
    if table:
        bits.append('table="{}"'.format(table))
    if column:
        bits.append('column="{}"'.format(column))
    if db_name:
        bits.append("db_name={}".format(db_name))
    if trigger_name:
        bits.append('trigger_name="{}"'.format(trigger_name))
    print(" ".join(bits), file=sys.stderr)
    return sqlite3.SQLITE_OK


@hookimpl
def prepare_connection(conn):
    conn.set_authorizer(print_authorizer)
