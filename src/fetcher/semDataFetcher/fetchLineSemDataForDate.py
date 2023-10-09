import datetime as dt
from typing import List
import os
import pandas as pd

from src.config.fileMappings import getLinesMappings


def fetchLineSemSummaryForDate(semLineFolderPath: str, targetDt: dt.datetime, lineName: str) -> List:
    """fetched sem Line availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[]: list of sem data records fetched from the excel data
    """
    # get file config
    linesConfig = getLinesMappings()
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%y')
    # sem column name from mapping file
    semCol = linesConfig.loc[linesConfig['Lines'] == lineName, 'SEM'].iloc[0]
    # file extension (IN6/IN7/....csv type format ) name from isgs Name
    fileNameExtension = linesConfig.loc[linesConfig['Lines']== lineName, 'file'].iloc[0]
    targetFilename = '{0}.{1}.csv'.format(fileDateStr, fileNameExtension)
    targetFilePath = os.path.join(semLineFolderPath, targetFilename)

    # check if csv file is present
    if not os.path.isfile(targetFilePath):
        print("Line Sem file for date {0} is not present for state {1}".format(
            targetDt, lineName))
        return []

    excelDf = pd.read_csv(targetFilePath, skipfooter=1, skiprows=1)

    # excelDf = pd.read_excel(targetFilePath, skiprows=9, skipfooter=3, header=None)
    excelDf = excelDf[[semCol]]
    excelDf.rename(columns={semCol: 'semData'}, inplace=True)

    # convert string typed value '--' column to ZERO
    excelDf.loc[excelDf["semData"] == "--", "semData"] = 0
    # convert string typed column to float
    excelDf['semData'] = excelDf['semData'].astype(float)
    semData = excelDf["semData"].tolist()
    return semData
