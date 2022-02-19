import datetime as dt
from typing import List
import os
import pandas as pd


def fetchIsgsScadaSummaryForDate( scadaIsgsFolderPath: str, targetDt: dt.datetime, isgsName: str) -> List :
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[IPmuAvailabilitySummary]: list of pmu availability records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'GEN_SCADA_SEM_{0}.csv'.format(fileDateStr)
    targetFilePath = os.path.join( scadaIsgsFolderPath, targetFilename)
    # print(targetFilePath)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("ISGS Scada csv file for date {0} is not present".format(targetDt))
        return []

    # read pmu excel 
    excelDf = pd.read_csv(targetFilePath, skiprows=2, nrows=96)
    # print("scada Data")
    # print(excelDf)
    # print(isgsName)
    
    #  acbil addition with mcpl test starts
    if isgsName == "AC-91":
        excelDf["ACBIL_EXPP"] = excelDf["ACBIL_EXPP"] + excelDf["MCPL_EXPP"] 
        column = "ACBIL_EXPP"
    #  acbil addition with mcpl test ends
    elif isgsName == "BL-91":
        column = "BALCO_EXPP"
    elif isgsName == "CG-91":
        column = "CGPL_EXPP          "
    elif isgsName == "DB-91":
        column = "DBPWR_EXPP"
    elif isgsName == "DC-91":
        column = "JDCPP_JINDL"
    elif isgsName == "DG-91":
        column = "DGEN_EXPP"
    elif isgsName == "DW-91":
        column = "DHRW_EXPP"
    elif isgsName == "EM-91":
        column = "EMCO_EXPP"
    elif isgsName == "GA-91":
        column = "JHNR_EXP"
    elif isgsName == "GM-91":
        column = "GMR_RAI_EXPP"
    elif isgsName == "JD-96":
        column = "JINDAL_EXPP"
    elif isgsName == "JD-97":
        column = "JPLII_EXPP"
    elif isgsName == "JH-91":
        column = "JHABUA_EXPP"
    elif isgsName == "JY-91":
        column = "JPNIG_EXPP"
    elif isgsName == "KA-91":
        column = "KAPS_EXPP                 "
    elif isgsName == "KB-91":
        column = "KWPCL_EXPP"
    elif isgsName == "KO-97":
        column = "KSTPS_I_GROSS"
    elif isgsName == "KO-98":
        column = "KSTP_III_EXPP                 "
    elif isgsName == "KS-91":
        column = "KSK_EXPP"
    elif isgsName == "KW-91":
        column = "KAWAS_EXP"
    elif isgsName == "LK-91":
        column = "LANCO_EXPP"
    elif isgsName == "MB-91":
        column = "MBPWR_EXPP"
    elif isgsName == "MD-96":
        column = "MDA1_EXPP"
    elif isgsName == "MD-97":
        column = "MDA2_EXPP"
    elif isgsName == "MN-91":
        column = "ESRMN_EXPP"
    elif isgsName == "NS-91":
        column = "NSPCL_EXPP"
    elif isgsName == "RG-91":
        column = "RGPPL_EXPP"
    elif isgsName == "RK-91":
        column = "RKM_EXPP"
    elif isgsName == "SA-91":
        column = "SASAN_EXP"
    elif isgsName == "SK-91":
        column = "SKS_EXPP"
    elif isgsName == "SP-91":
        column = "SIPAT_EXPP"
    elif isgsName == "SS-91":
        column = "SSP_EXPP"
    elif isgsName == "TA-91":
        column = "TAPS1_EXPP"
    elif isgsName == "TA-94":
        column = "TAPS2_EXPP"
    elif isgsName == "TR-91":
        column = "TRN_EXPP"
    elif isgsName == "VI-96":
        column = "VIN1_EXPP"
    elif isgsName == "VI-97":
        column = "VIN2_EXPP"
    elif isgsName == "VI-99":
        column = "VIN3_EXPP"
    elif isgsName == "VI-V4":
        column = "VSTPSIV_EXPP"
    elif isgsName == "VI-V5":
        column = "VSTPS5_EXPP"
    elif isgsName == "SO-91":
        column = "SNTPC_EXPP"
    elif isgsName == "LA-91":
        column = "LARA4_EXPP"
    elif isgsName == "GD-91":
        column = "GDRWD_EXPP"
    elif isgsName == "KH-91":
        column = "KHRGN_EXPP"

    excelDf = excelDf.loc[:, ["Timestamp", column]]
    # excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],dayfirst=True)
    excelDf['Timestamp'] = pd.to_datetime(excelDf["Timestamp"],format="%d-%m-%Y %H:%M:S")
    excelDf[column]= excelDf[[column]].div(4, axis=0)

    scadaData = excelDf[column].tolist()
    # timeStamp = list(excelDf.index)
    excelDf['Timestamp'] = pd.to_datetime(excelDf.Timestamp)
    # print(excelDf)
    timeStamp = excelDf["Timestamp"].tolist()
    return scadaData, timeStamp