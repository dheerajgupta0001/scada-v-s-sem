import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.scadaSemSummary import IScadaSemSummary

class ScadaSemLinesSummaryRepo():
    """Repository class for scada sem data
    """
    """This class pushes Scada-Sem Lines data To "scada_warehouse.SCADA_SEM_Lines" table
    """
    connString: str = ""
    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string

    def pushScadaSemLinesRecord(self, scadaSemLinesRecords: List[IScadaSemSummary]) -> bool:
        """inserts Scada-Sem data To "scada_warehouse.SCADA_SEM_Lines" table
        Args:
            scadaSemLinesRecords (List[IScadaSemSummary]): scada Sem Re Records to be inserted
        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        connection= cx_Oracle.connect(self.connString)
        isInsertSuccess = True
        if len(scadaSemLinesRecords) == 0:
            return isInsertSuccess
        try:
            # keyNames names of the raw data
            keyNames = ['time_stamp', 'SCADA_DATA_Line', 'SEM_DATA_Line', 'Line_NAME']
            colNames = ['TIME_STAMP', 'SCADA_DATA_Line', 'SEM_DATA_Line', 'Line_NAME']
            # get cursor for raw data table
            cursor=connection.cursor()

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(keyNames))])

            # delete the rows which are already present
            existingScadaSemData = [(x['time_stamp'], x['Line_NAME'] )
                                  for x in scadaSemLinesRecords]
            # print("deletion started")
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
            cursor.executemany(
                "delete from scada_warehouse.SCADA_SEM_Line where TIME_STAMP=:1 and Line_NAME=:2", existingScadaSemData)
            # print("deletion is done")
            
            # insert the raw data
            sql_insert = "insert into scada_warehouse.SCADA_SEM_Line({0}) values ({1})".format(
                ','.join(colNames), sqlPlceHldrsTxt)
            
            # cursor.execute("ALTER USER <scada_warehouse> quota unlimited on <SCADA_SEM_RE>;")
            # cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
            cursor.executemany(sql_insert, [tuple(
                [r[col] for col in keyNames]) for r in scadaSemLinesRecords])
            # commit the changes
            connection.commit()
        except Exception as e:
            isInsertSuccess = False
            print('Error while bulk insertion of Scada Sem Lines data into database')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            
        return isInsertSuccess
