import numpy as np
import pandas as pd
import psycopg2
from datetime import timedelta, datetime, date, time
from sqlalchemy import create_engine

def table_frame_equivalence(schema_name, table_name, gospel_dataframe, output_dataframe, postgres_column_type):
    '''Enter a postgres schema name and table name followed by a pandas dataframe of the table and output dataframe.
    This will resolve differences between the table and dataframe.'''
    if list(gospel_dataframe.columns) != list(output_dataframe.columns):
        database_missing = list(output_dataframe.columns.difference(gospel_dataframe.columns))
        dataframe_missing = list(gospel_dataframe.columns.difference(output_dataframe.columns))
        with gospel_rds_ppgconn as conn:
            cur = conn.cursor()
            for column in database_missing:
                cur.execute('ALTER TABLE %s.%s ADD COLUMN %s %s' % (schema_name, table_name, column, postgres_column_type))
                conn.commit()
        final_output_dataframe = pd.concat([output_dataframe, pd.DataFrame(columns=dataframe_missing)], axis=1)

    return final_output_dataframe
