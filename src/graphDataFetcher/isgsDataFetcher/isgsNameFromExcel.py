from src.config.fileMappings import getIsgsMappings

def isgsDisplayNameFromExcel(stateName: str):
    """
    Args:
        stateName (str): sem state code for graph plotting
    Returns:
        Name of the state for graph plotting!!! pd.read_excel(filePath, sheet_name= 'RE')
    """
    isgsDataDf = getIsgsMappings()
    isgsDisplayName = isgsDataDf.loc[isgsDataDf['ISGS'] == stateName, 'Display_Name'].iloc[0]
    
    return isgsDisplayName