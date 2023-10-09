from src.config.fileMappings import getLinesMappings

def lineDisplayNameFromExcel(stateName: str):
    """
    Args:
        stateName (str): sem state code for graph plotting
    Returns:
        Name of the state for graph plotting!!! pd.read_excel(filePath, sheet_name= 'Line')
    """
    lineDataDf = getLinesMappings()
    lineDisplayName = lineDataDf.loc[lineDataDf['Lines'] == stateName, 'Display_Name'].iloc[0]
    
    return lineDisplayName