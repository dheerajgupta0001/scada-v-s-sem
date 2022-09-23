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
from src.config.appConfig import getConfig
from src.scadaSemDataFetcher.daywiseScadaSemIsgsDataFetcher import fetchScadaSemIsgsRawData
from src.repos.insertScadaSemIsgsToDb import ScadaSemIsgsSummaryRepo
from src.graphDataFetcher.isgsDataFetcher.isgsName import isgsDisplayNameData
from src.graphDataFetcher.isgsDataFetcher.graphPlotDataFetcher import PlotScadaSemIsgsData

# get application config
appConfig = getConfig()
scadaIsgsFolderPath = appConfig['scadaIsgsFolderPath']
semIsgsFolderPath = appConfig['semIsgsFolderPath']
appDbConnStr = appConfig['appDbConStr']

scadaSemIsgsPage = Blueprint('scadaSemIsgs', __name__,
                             template_folder='templates')
# get the instance of min_wise demand storage repository
scadaSemIsgsRepo = ScadaSemIsgsSummaryRepo(appDbConnStr)


class CreateScadSemIsgsForm(Form):
    # my_choices = [('1', _('VEHICLES')), ('2', _('Cars')), ('3', _('Motorcycles'))]
    my_choices = [('Vh', 'Vehicles'), ('Cr', 'Cars'), ('Mr', 'Motorcycles')]
    startDate = DateField("Start Date", default=date.today(), format='%Y-%m-%d',
                          validators=[DataRequired(message="You need to enter the start date")],)
    endDate = DateField("End Date", validators=[DataRequired(
        message="You need to enter the end date.")], format='%Y-%m-%d')
    isgsList = SelectMultipleField(
        "Select ISGS(s)", choices=my_choices, id="isgsList")


@scadaSemIsgsPage.route('/create', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def create():
    form = CreateScadSemIsgsForm(request.form)
    if request.method == 'POST' and form.validate():
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("tsting {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        # isgsName = request.form.getlist('isgsList')
        isgsList = ["AC-91", "BL-91", "CG-91", "DB-91", "DC-91", "DG-91", "DW-91", "EM-91", "GA-91",
                    "GM-91", "JD-96", "JD-97", "JH-91", "JY-91", "KA-91", "KB-91", "KO-97", "KO-98",
                    "KS-91", "KW-91", "LK-91", "MB-91", "MD-96", "MD-97", "MN-91", "NS-91", "RG-91",
                    "RK-91", "SA-91", "SK-91", "SS-91", "TA-91", "TA-94", "TR-91", "VI-96",
                    "VI-97", "VI-99", "VI-V4", "VI-V5", "SO-91", "LA-91", "GD-91", "KH-91"]
        # print(isgsList)
        # isgsList = ["SK-91"]

        # testing of multiple div dynamically
        for isgsName in isgsList:
            isRawCreationSuccess = False
            # get the scada sem data of 1st re name for GRAPH PLOTTING
            scadaSemIsgsRecord = fetchScadaSemIsgsRawData(scadaIsgsFolderPath, semIsgsFolderPath,
                                                          startDate, endDate,  isgsName)
            isRawCreationSuccess = scadaSemIsgsRepo.pushScadaSemIsgsRecord(
                scadaSemIsgsRecord)
            if isRawCreationSuccess:
                # print("स्काडा सेम आईएसजीएस डेटा प्रविष्टि {} के लिए सफल".format(isgsName))
                print("{} ISGS Done".format(isgsName))
            else:
                print("स्काडा सेम आईएसजीएस डेटा प्रविष्टि {} के लिए असफल".format(isgsName))
        # print(errorPerc[0])
        startDate = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strftime(endDate, '%Y-%m-%d')
        if isRawCreationSuccess:
            x = {'message': 'Scada Sem Isgs Data insertion successful!!!'}
            return render_template('scadaSemIsgs/create.html.j2', data=x, startDate=startDate, endDate=endDate, form=form)

        return render_template('scadaSemIsgs/create.html.j2', startDate=startDate, endDate=endDate, form=form)
    # in case of get request just return the html template
    return render_template('scadaSemIsgs/create.html.j2', form=form)


@scadaSemIsgsPage.route('/plot', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def plot():
    # in case of post request, fetch
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("testing {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        # isgsName = request.form.getlist('isgsList')
        isgsName = ["AC-91", "BL-91", "CG-91", "DB-91", "DC-91", "DG-91", "DW-91", "EM-91", "GA-91",
                    "GM-91", "JD-96", "JD-97", "JH-91", "JY-91", "KA-91", "KB-91", "KO-97", "KO-98",
                    "KS-91", "KW-91", "LK-91", "MB-91", "MD-96", "MD-97", "MN-91", "NS-91", "RG-91",
                    "RK-91", "SA-91", "SK-91", "SS-91", "TA-91", "TA-94", "TR-91", "VI-96",
                    "VI-97", "VI-99", "VI-V4", "VI-V5", "SO-91", "LA-91", "GD-91", "KH-91"]
        # print(isgsName)

        # testing of multiple div dynamically
        dfData_g = []
        errorPerc = []
        isgsDisplayList = []
        divItrs = []
        for cItr,currIsgsName in enumerate(isgsName):
            # get the instance of scada sem isgs repository for GRAPH PLOTTING
            plotScadaSemIsgsDataRepo = PlotScadaSemIsgsData(appDbConnStr)

            # fetch scada sem data from db via the repository instance of ith state
            dfData_gInd, errorPercInd = plotScadaSemIsgsDataRepo.plotScadaSemIsgsData(
                startDate, endDate, currIsgsName)
            isgs = isgsDisplayNameData(currIsgsName)
            isgsDisplayList.append(isgs)
            dfData_g.append(dfData_gInd)
            errorPerc.append(errorPercInd)
            divItrs.append(cItr+1)
        # print(errorPerc[0])
        startDate = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strftime(endDate, '%Y-%m-%d')
        div_info = zip(isgsName, errorPerc, divItrs)
        # print(reDisplayList)
        print(errorPerc)

        return render_template('scadaSemIsgs/plot.html.j2', data=dfData_g, div_info=div_info,
                               isgsName=isgsName, isgsDisplayList=isgsDisplayList,
                               startDate=startDate, endDate=endDate)
    # in case of get request just return the html template
    return render_template('scadaSemIsgs/plot.html.j2')
