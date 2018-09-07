import numpy as np
import pandas as pd
import psycopg2
from datetime import timedelta, datetime, date, time
from sqlalchemy import create_engine

def table_frame_equivalence(schema_name, table_name, database_dataframe, output_dataframe, psycopg_connection, postgres_column_type):
    '''Enter a postgres schema name and table name followed by a pandas dataframe of the table and output dataframe.
    Additionally, a psycopg2.connect() object needs to be provided and the column type for the postgres database table.
    This will resolve differences between the table and dataframe.'''
    if list(database_dataframe.columns) != list(output_dataframe.columns):
        database_missing = list(output_dataframe.columns.difference(database_dataframe.columns))
        dataframe_missing = list(database_dataframe.columns.difference(output_dataframe.columns))
        with psycopg_connection as conn:
            cur = conn.cursor()
            for column in database_missing:
                cur.execute('ALTER TABLE %s.%s ADD COLUMN %s %s' % (schema_name, table_name, column, postgres_column_type))
            conn.commit()
        final_output_dataframe = pd.concat([output_dataframe, pd.DataFrame(columns=dataframe_missing)], axis=1)
    else
        final_output_dataframe = output_dataframe

    return final_output_dataframe
