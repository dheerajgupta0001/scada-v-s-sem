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
    targetFilename = 'RE_SCADASEM_{0}.csv'.format(fileDateStr)
    targetFilePath = os.path.join( scadaReFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("RE Scada csv file for date {0} is not present".format(targetDt))
        return []

    # read pmu excel 
    excelDf = pd.read_csv(targetFilePath, skiprows=2, nrows=96)
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
    elif reName == "EG-91":
        column = "Engie_Solar"
    elif reName == "GP-91":
        column = "Gipcl_Solar"
    elif reName == "TP-91":
        column = "Tprel_Solar"
    elif reName == "AV-91":
        column = "Avikiran_Solar"
    elif reName == "KR-91":
        column = "KAWAS_Solar "
    elif reName == "GS-91":
        column = "GSECL_Solar "
    elif reName == "JM-91":
        column = "Powerica_Wind"
    excelDf = excelDf.loc[:, ["Timestamp", column]]
    # excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%Y-%m-%d %H:%M:S")
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%d-%m-%Y %H:%M:S")
    
    excelDf[column]= excelDf[[column]].div(4, axis=0)
    scadaData = excelDf[column].tolist()
    # timeStamp = list(excelDf.index)
    excelDf['Timestamp'] = pd.to_datetime(excelDf.Timestamp)
    # print(excelDf)
    timeStamp = excelDf["Timestamp"].tolist()
    return scadaData, timeStamp