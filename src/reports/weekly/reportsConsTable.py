import datetime as dt
import pandas as pd
from src.graphDataFetcher.graphPlotDataFetcher import PlotScadaSemData
from src.graphDataFetcher.stateName import stateNameData


# get application config
def fetchConsErrorReportData(endDate, appDbConnStr: str):
    endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
    startDate = endDate - dt.timedelta(days=6)
    endDate1 = endDate - dt.timedelta(days=7)
    startDate1 = endDate1 - dt.timedelta(days=6)
    endDate2 = endDate - dt.timedelta(days=14)
    startDate2 = endDate2 - dt.timedelta(days=6)
    endDate3 = endDate - dt.timedelta(days=21)
    startDate3 = endDate3 - dt.timedelta(days=6)
    # reName = request.form.getlist('reList')
    # print(reportList)
    reportList = ["constituents", "re", "isgs"]
    for reportType in reportList:
        if reportType == "constituents":
            constituentsName = ["BR1", "CS1", "TD1", "GO1",
                                "GU2", "HZ1", "MH2", "MP2", "ER1", "NR1", "SR1"]
            # print(constituentsName)

            # testing of multiple div dynamically
            dfData_g = []
            errorPerc1 = []
            errorPerc2 = []
            errorPerc3 = []
            errorPerc4 = []
            stateList = []
            columnNameList = []
            columnNameList.append("States")
            for stateName in constituentsName:
                # get the instance of scada sem repository for GRAPH PLOTTING
                plotScadaSemDataRepo = PlotScadaSemData(appDbConnStr)

                # fetch scada sem data from db via the repository instance of ith state
                dfData_gInd, errorPercWeek4 = plotScadaSemDataRepo.plotScadaSemData(
                    startDate3, endDate3, stateName)

                dfData_gInd, errorPercWeek3 = plotScadaSemDataRepo.plotScadaSemData(
                    startDate2, endDate2, stateName)

                dfData_gInd, errorPercWeek2 = plotScadaSemDataRepo.plotScadaSemData(
                    startDate1, endDate1, stateName)

                dfData_gInd, errorPercWeek1 = plotScadaSemDataRepo.plotScadaSemData(
                    startDate, endDate, stateName)

                state = stateNameData(stateName)
                stateList.append(state)
                dfData_g.append(dfData_gInd)
                errorPerc1.append(errorPercWeek1)
                errorPerc2.append(errorPercWeek2)
                errorPerc3.append(errorPercWeek3)
                errorPerc4.append(errorPercWeek4)
            endDate = dt.datetime.strftime(endDate, '%d-%m-%Y')
            endDate1 = dt.datetime.strftime(endDate1, '%d-%m-%Y')
            endDate2 = dt.datetime.strftime(endDate2, '%d-%m-%Y')
            endDate3 = dt.datetime.strftime(endDate3, '%d-%m-%Y')
            startDate = dt.datetime.strftime(startDate, '%d-%m-%Y')
            startDate1 = dt.datetime.strftime(startDate1, '%d-%m-%Y')
            startDate2 = dt.datetime.strftime(startDate2, '%d-%m-%Y')
            startDate3 = dt.datetime.strftime(startDate3, '%d-%m-%Y')
            week4 = str(startDate3) + " " + str(endDate3)
            week3 = str(startDate2) + " " + str(endDate2)
            week2 = str(startDate1) + " " + str(endDate1)
            week1 = str(startDate) + " " + str(endDate)
            columnNameList.append(week4)
            columnNameList.append(week3)
            columnNameList.append(week2)
            columnNameList.append(week1)

            constituentsTableError = pd.DataFrame(
                {'states': stateList,
                    'week1': errorPerc4,
                    'week2': errorPerc3,
                    'week3': errorPerc2,
                    'week4': errorPerc1
                    })
            constituentsTableError = constituentsTableError.to_records(
                index=False)
            constituentsTableError = list(constituentsTableError)

    return constituentsTableError, columnNameList
