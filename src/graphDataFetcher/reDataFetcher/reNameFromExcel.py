from src.config.fileMappings import getReMappings

def reDisplayNameFromExcel(stateName: str):
    """
    Args:
        stateName (str): sem state code for graph plotting
    Returns:
        Name of the state for graph plotting!!! pd.read_excel(filePath, sheet_name= 'RE')
    """
    reDataDf = getReMappings()
    reDisplayName = reDataDf.loc[reDataDf['RE'] == stateName, 'Display_Name'].iloc[0]
    
    return reDisplayName