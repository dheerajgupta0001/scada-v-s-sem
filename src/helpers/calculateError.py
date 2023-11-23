import pandas as pd

def calculateErrorPerc(dataDf: pd.DataFrame, limit, scada_type, sem_type):
    errorSum = []
    count = 0
    for i in range(len(dataDf.index)):
        if dataDf[sem_type][i] >=limit or dataDf[sem_type][i] <= -(limit):
            errorSum.append(abs((dataDf[scada_type][i] - dataDf[sem_type][i]))/dataDf[sem_type][i])
    if len(errorSum) != 0:
        errorSum = sum(errorSum)/len(errorSum)
        errorPerc = round(errorSum*100, 2)
        return errorPerc