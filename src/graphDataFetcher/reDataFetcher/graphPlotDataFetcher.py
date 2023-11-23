from typing import List, Tuple, TypedDict
import cx_Oracle
import datetime as dt
import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from src.helpers.calculateError import calculateErrorPerc

class PlotScadaSemReData():
    """Repository class for pmu availability summary data
    """
    connString: str = ""

    def __init__(self, con_string: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.connString = con_string

    def plotScadaSemReData(self, startDate: dt.datetime, endDate: dt.datetime, reName: str):
        """fetchess scada sem data from the app db
        Args:
            appDbConStr (str): application db connection string
            reName (str): List of Scada Sem data for graph plot
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            dictionary of lists of scada sem data!!!
        """
        try:
            # print("cursor created")
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()
            endDate= endDate+dt.timedelta(hours=23, minutes=59, seconds=00)
            sql_fetch = f""" 
                        select TIME_STAMP, scada_data_re, sem_data_re
                        from scada_warehouse.scada_sem_re
                        where
                        TIME_STAMP between to_date(:start_date) and to_date(:end_date)
                        and re_name in ('{reName}')
                        order by TIME_STAMP
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
            # print("cursor executed")
            data = pd.read_sql(sql_fetch, params={
                'start_date': startDate, 'end_date': endDate}, con=connection)
            # print(data)
        except Exception as e:
            print('Error while fetching scada sem re data from db')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            # print('closed db connection after scada sem re data fetching')
        
        # set proper date time format
        times = data['TIME_STAMP']
        dateList = []
        for col in times:
            dateList.append(dt.datetime.strftime(col, '%Y-%m-%d %H:%M:%S'))
        data['TIME_STAMP']= dateList
        # print(data)
        # getting Difference 
        meterDataSum = data['SEM_DATA_RE'].sum()
        errorDiffList = data['SCADA_DATA_RE'] - data['SEM_DATA_RE']
        errorSum = errorDiffList.sum() 
        
        if meterDataSum != 0:
            # errorPerc = round((errorSum/meterDataSum)*100, 2)
            errorPerc = calculateErrorPerc(data, 2, 'SCADA_DATA_RE', 'SEM_DATA_RE')
        else: 
            errorPerc =0
        
        # convert dataframe to list of dictionaries
        resRecords = data.to_dict(orient='list')
        # print(resRecords)

        return resRecords, errorPerc