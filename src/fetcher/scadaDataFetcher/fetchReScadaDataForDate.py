import datetime as dt
#from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd


def fetchReScadaSummaryForDate( scadaReFolderPath: str, targetDt: dt.datetime, reName: str) -> List :
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[IPmuAvailabilitySummary]: list of pmu availability records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'RE_SCADASEM_{0}.xlsx'.format(fileDateStr)
    targetFilePath = os.path.join( scadaReFolderPath, targetFilename)
    print(targetFilePath)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("RE Scada Excel file for date {0} is not present".format(targetDt))
        return []

    # read pmu excel 
    excelDf = pd.read_excel(targetFilePath, skiprows=2)
    # print("scada Data")
    if reName == "OS-91":
        column = "Ostro_Wind"
    elif reName == "AM-91":
        column = "Acme_Solar"
    elif reName == "MA-91":
        column = "Mahendra_Solar"
    elif reName == "AR-91":
        column = "Arinsun_Solar"
    elif reName == "RE-91":
        column = "Bhuvad_Wind"
    elif reName == "GI-91":
        column = "Vadva_Wind"
    elif reName == "GI-94":
        column = "Naranpar_Wind"
    elif reName == "IX-91":
        column = "Dayapar_Wind"
    elif reName == "AG-91":
        column = "Ratadiya_Wind"
    elif reName == "AF-91":
        column = "Alfanar_Wind"
    elif reName == "GH-91":
        column = "Gadhsisa_Wind"
    excelDf = excelDf.loc[:, ["Timestamp", column]]
    # excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = excelDf['Timestamp'].apply(lambda x: dt.datetime.strftime(x, '%Y-%d-%m %H:%M:%S'))
    # to get month from timestamp
    # month = pd.DatetimeIndex(excelDf['Timestamp']).month
    # excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%Y-%m-%d %H:%M:S")
    excelDf[column]= excelDf[[column]].div(4, axis=0)
    scadaData = excelDf[column].tolist()
    # timeStamp = list(excelDf.index)
    excelDf['Timestamp'] = pd.to_datetime(excelDf.Timestamp)
    # print(excelDf)
    timeStamp = excelDf["Timestamp"].tolist()
    return scadaData, timeStamp