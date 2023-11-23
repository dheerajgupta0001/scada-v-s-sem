import pandas as pd

def calculateErrorPerc(dataDf: pd.DataFrame, limit):
    errorSum = []
    count = 0
    for i in range(len(dataDf.index)):
        if dataDf['SEM_DATA_ISGS'][i] >=limit or dataDf['SEM_DATA_ISGS'][i] <= -(limit):
            errorSum.append(abs((dataDf['SCADA_DATA_ISGS'][i] - dataDf['SEM_DATA_ISGS'][i]))/dataDf['SEM_DATA_ISGS'][i])
    if len(errorSum) != 0:
        errorSum = sum(errorSum)/len(errorSum)
        errorPerc = round(errorSum*100, 2)
        return errorPerc