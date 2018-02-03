"""
Code partially from http://www.sqlitetutorial.net/sqlite-python/create-tables/
"""
import contextlib
import sqlite3


def create_database(path_to_database):
    """ TODO: Implement foreign keys
           log_level_id integer not null,
               foreign key (log_level_id) references log_levels(id)

    :param path_to_database:
    :return:
    """
    sql_to_create_log_entries_table = ("""  create table if not exists log_entries (
                                                id integer primary key,
                                                timestamp text not null,
                                                log_level text not null,
                                                uri text,
                                                uri_pattern text,
                                                request_uuid text,
                                                device_uuid text,
                                                merchant_id text,
                                                version_id text,
                                                request_ip text,
                                                http_method text,
                                                http_status text,
                                                developer_app_id text,
                                                auth_mechanism text,
                                                request_time int,
                                                log_statement text,
                                                logging_class text not null,
                                                unique (timestamp,
                                                       log_level,
                                                       uri,
                                                       uri_pattern,
                                                       request_uuid,
                                                       device_uuid,
                                                       merchant_id,
                                                       version_id,
                                                       request_ip,
                                                       http_method,
                                                       http_status,
                                                       developer_app_id,
                                                       auth_mechanism,
                                                       request_time,
                                                       log_statement,
                                                       logging_class) on conflict replace); """)
    # sql_to_create_log_levels_table = """ create table if not exists log_levels (
    #                                          id integer primary key,
    #                                          value text not null
    #                                      ); """

    # See https://stackoverflow.com/a/19524679/4115031 for the pattern used below to open the db.
    with contextlib.closing(sqlite3.connect(path_to_database)) as con:  # <-- Auto-close the db connection
        with con as session:  # <-- Auto commit or roll back
            _create_table(session, sql_to_create_log_entries_table)
            # _create_table(session, sql_to_create_log_levels_table)


def _create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    c = conn.cursor()
    c.execute(create_table_sql)


def add_log_entry_to_db(path_to_database, timestamp, log_level, logging_class, uri=None, uri_pattern=None,
                        request_uuid=None, device_uuid=None, merchant_id=None, version_id=None, request_ip=None,
                        http_method=None, http_status=None, developer_app_id=None, auth_mechanism=None,
                        request_time=None, log_statement=None):
    """

    :param timestamp:
    :param log_level:
    :return:
    """
    field_names = set(locals().keys())
    assert("path_to_database" in field_names)
    field_names.remove("path_to_database")
    sorted_field_names = sorted(list(field_names))

    parameter_dict = locals()  # Need to do this to get it to work within the list comprehension
    parameter_values = [parameter_dict[key] if key else None for key in sorted_field_names]

    with contextlib.closing(sqlite3.connect(path_to_database)) as con:
        with con as session:
            c = session.cursor()

            sql_string = """insert into log_entries (%s)
                                 values (%s);""" % (", ".join(sorted_field_names), ", ".join(["?" for value in parameter_values]))
            try:
                c.execute(sql_string, parameter_values)
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: log_entries.timestamp" in e.args[0]:
                    print("ERROR:\nTimestamp: %s" % timestamp)
                    raise


if __name__ == '__main__':
    path_to_database = "C:\\sqlite\db\example.sqlite"
    create_database(path_to_database)
