from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from wtforms import Form, StringField, validators, DateTimeField, BooleanField
from wtforms.fields.core import SelectMultipleField
from wtforms.fields.simple import MultipleFileField
from wtforms.widgets import TextArea
# from src.appConfig import getConfig
# from src.security.decorators import role_required
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import datetime as dt
from src.config.fileMappings import getReMappings
from src.config.appConfig import getConfig
from src.scadaSemDataFetcher.daywiseScadaSemReDataFetcher import fetchScadaSemReRawData
from src.repos.insertScadaSemReToDb import ScadaSemReSummaryRepo
from src.graphDataFetcher.reDataFetcher.reName import reDisplayNameData
from src.graphDataFetcher.reDataFetcher.reNameFromExcel import reDisplayNameFromExcel
from src.graphDataFetcher.reDataFetcher.graphPlotDataFetcher import PlotScadaSemReData

# get application config
appConfig = getConfig()
scadaReFolderPath = appConfig['scadaReFolderPath']
semReFolderPath = appConfig['semReFolderPath']
appDbConnStr = appConfig['appDbConStr']

scadaSemRePage = Blueprint('scadaSemRe', __name__,
                            template_folder='templates')
# get the instance of min_wise demand storage repository
scadaSemReRepo= ScadaSemReSummaryRepo(appDbConnStr)

class CreateScadSemReForm(Form):
    # my_choices = [('1', _('VEHICLES')), ('2', _('Cars')), ('3', _('Motorcycles'))]
    my_choices = [('Vh', 'Vehicles'), ('Cr', 'Cars'), ('Mr', 'Motorcycles')]
    startDate = DateField("Start Date", default=date.today(), format='%Y-%m-%d', validators=[DataRequired(message="You need to enter the start date")],)
    endDate = DateField("End Date", validators=[DataRequired(message="You need to enter the end date.")], format='%Y-%m-%d')
    reList = SelectMultipleField("Select RE(s)", choices = my_choices, id = "reList")

@scadaSemRePage.route('/create', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def create():
    form = CreateScadSemReForm(request.form)
    if request.method == 'POST' and form.validate():
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        # get file config
        reConfig = getReMappings()
        reList = reConfig['RE'].dropna()
        # reList = ["OS-91", "AM-91", "MA-91", "AR-91", "RE-91", "GI-91", "GI-94", "IX-91", "AG-91", "AF-91", "GH-91",
        #           "EG-91", "GP-91", "TP-91", "AV-91","KR-91", "JM-91", "GS-91", "CR-91", "MJ-91", "GR-91"]
        # testing of multiple div dynamically
        for  reName in reList:
            isRawCreationSuccess= False
            # get the scada sem data of 1st re name for GRAPH PLOTTING
            scadaSemReRecord = fetchScadaSemReRawData(scadaReFolderPath, semReFolderPath,
                                                        startDate, endDate,  reName)
            isRawCreationSuccess = scadaSemReRepo.pushScadaSemReRecord(scadaSemReRecord)
            if isRawCreationSuccess:
                print("{} Data Success".format( reName))
            else:
                print("स्काडा सेम आरई डेटा प्रविष्टि {} के लिए असफल".format( reName))
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        if isRawCreationSuccess:
            x=  {'message': 'Scada Sem RE Data insertion successful!!!'}
            return render_template('scadaSemRe/create.html.j2', data= x, startDate= startDate, endDate= endDate, form=form)

        return render_template('scadaSemRe/create.html.j2', startDate= startDate, endDate= endDate, form=form)
    # in case of get request just return the html template
    return render_template('scadaSemRe/create.html.j2', form=form)

@scadaSemRePage.route('/plot', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def plot():
    # in case of post request, fetch 
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        # reName = request.form.getlist('reList') , "EG-91", "GP-91", "TP-91"
        reConfig = getReMappings()
        reName = reConfig['RE'].dropna()
        reName = reName.to_list()
        # reName = ["OS-91", "AM-91", "MA-91", "AR-91", "RE-91", "GI-91", "GI-94", "IX-91", "AG-91", "AF-91", "GH-91",
        #           "EG-91", "GP-91", "TP-91", "AV-91","KR-91", "JM-91", "GS-91", "CR-91", "MJ-91", "GR-91", "NK-91", "AP-91"]

        # testing of multiple div dynamically
        dfData_g = []
        errorPerc = []
        reDisplayList = []
        divItrs = []
        for cItr,currReName in enumerate(reName):
            #get the instance of scada sem repository for GRAPH PLOTTING
            plotScadaSemReDataRepo = PlotScadaSemReData(appDbConnStr)
            # fetch scada sem data from db via the repository instance of ith state
            dfData_gInd, errorPercInd = plotScadaSemReDataRepo.plotScadaSemReData(startDate, endDate, currReName)
            # re= reDisplayNameData(currReName)
            re= reDisplayNameFromExcel(currReName)
            reDisplayList.append(re)
            dfData_g.append(dfData_gInd)
            errorPerc.append(errorPercInd)
            divItrs.append(cItr+1)
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        div_info = zip(reName, errorPerc, divItrs)

        return render_template('scadaSemRe/plot.html.j2', data= dfData_g, div_info= div_info,
                                reName= reName, reDisplayList= reDisplayList,
                                startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('scadaSemRe/plot.html.j2')
