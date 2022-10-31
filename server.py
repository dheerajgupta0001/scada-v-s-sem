'''
This is the web server that acts as a service that creates scada sem data
'''
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
from flask import Flask, request, jsonify, render_template
import datetime as dt
import pandas as pd
import json
import os
from waitress import serve
from src.config.fileMappings import initConfigs
from src.config.appConfig import getConfig
from src.scadaSemDataFetcher.daywiseScadaSemDataFetcher import fetchScadaSemRawData
from src.repos.insertScadaSemToDb import ScadaSemSummaryRepo
from src.graphDataFetcher.graphPlotDataFetcher import PlotScadaSemData
from src.graphDataFetcher.stateName import stateNameData
from src.routeControllers.scadaSemReData import scadaSemRePage
from src.routeControllers.scadaSemIsgsData import scadaSemIsgsPage
from src.routeControllers.scadaSemReports import scadaSemReportsPage

app = Flask(__name__)

# get application config
appConfig = getConfig()
# get ISGS details config
initConfigs()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# create pmu availability raw data between start and end dates
scadaSemFolderPath = appConfig['scadaSemFolderPath']
scadaFolderPath = appConfig['scadaFolderPath']
semFolderPath = appConfig['semFolderPath']
# print(semFolderPath)
# print(scadaFolderPath)
appDbConnStr = appConfig['appDbConStr']

# get the instance of min_wise demand storage repository
scadaSemRepo= ScadaSemSummaryRepo(appDbConnStr)

@app.route('/')
def hello():
    return render_template('home.html.j2')


@app.route('/createScadaSemData', methods=['GET', 'POST'])
def createScadaSemData():
    # in case of post request, fetch 
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("tsting {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        constituentsName = request.form.getlist('consList')
        # print(constituentsName)

        # testing of multiple div dynamically
        for stateName in constituentsName:
            isRawCreationSuccess= False
            #get the scada sem data of 1st state name for GRAPH PLOTTING
            scadaSemRecord = fetchScadaSemRawData(appDbConnStr, scadaSemFolderPath, scadaFolderPath,
                                                        semFolderPath, startDate, endDate, stateName)
            isRawCreationSuccess = scadaSemRepo.pushScadaSemRecord(scadaSemRecord)
            if isRawCreationSuccess:
                # print("स्काडा सेम संघटक डेटा प्रविष्टि {} के लिए सफल".format(stateName))
                print("Done")
            else:
                print("स्काडा सेम संघटक डेटा प्रविष्टि {} के लिए असफल".format(stateName))
        # print(errorPerc[0])
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        if isRawCreationSuccess:
            x=  {'message': 'Scada Sem Data insertion successful!!!'}
            return render_template('createScadaSemData.html.j2', data= x, startDate= startDate, endDate= endDate)

        return render_template('createScadaSemData.html.j2', startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('createScadaSemData.html.j2')


@app.route('/plotGraph', methods=['GET', 'POST'])
def plotGraph():
    # in case of post request, fetch 
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("tsting {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        constituentsName = request.form.getlist('consList')
        # print(constituentsName)

        # testing of multiple div dynamically
        dfData_g = []
        errorPerc = []
        stateList = []
        divItrs = []
        for cItr, stateName in enumerate(constituentsName):
            #get the instance of scada sem repository for GRAPH PLOTTING
            plotScadaSemDataRepo = PlotScadaSemData(appDbConnStr)

            # fetch scada sem data from db via the repository instance of ith state
            dfData_gInd, errorPercInd = plotScadaSemDataRepo.plotScadaSemData(startDate, endDate, stateName)
            # print(dfData_gInd)
            state= stateNameData(stateName)
            stateList.append(state)
            dfData_g.append(dfData_gInd)
            errorPerc.append(errorPercInd)
            divItrs.append(cItr+1)
            
        # print(errorPerc[0])
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        div_info = zip(constituentsName, errorPerc, divItrs)
        # print(stateList)
        # print(errorPerc)

        return render_template('plot.html.j2', data= dfData_g, div_info= div_info,
                                consName= constituentsName, stateList= stateList,
                                startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('plot.html.j2')

app.register_blueprint(scadaSemRePage, url_prefix='/scadaSemRe')
app.register_blueprint(scadaSemIsgsPage, url_prefix='/scadaSemIsgs')
app.register_blueprint(scadaSemReportsPage, url_prefix='/scadaSemReports')

if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'p':
        app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)
