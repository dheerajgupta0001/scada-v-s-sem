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
from src.scadaSemDataFetcher.daywiseScadaSemLineDataFetcher import fetchScadaSemLineRawData
from src.repos.insertScadaSemLinesToDb import ScadaSemLinesSummaryRepo
from src.graphDataFetcher.lineDataFetcher.lineNameFromExcel import lineDisplayNameFromExcel
from src.graphDataFetcher.lineDataFetcher.graphPlotDataFetcher import ScadaSemLineDataRepo
from src.config.fileMappings import getLinesMappings

# get application config
appConfig = getConfig()
scadaLineFolderPath = appConfig['scadaLineFolderPath']
semLineFolderPath = appConfig['semLineFolderPath']
appDbConnStr = appConfig['appDbConStr']

scadaSemLinesPage = Blueprint('scadaSemLines', __name__,
                             template_folder='templates')
# get the instance of min_wise demand storage repository
scadaSemLinesRepo = ScadaSemLinesSummaryRepo(appDbConnStr)


class CreateScadSemLinesForm(Form):
    # my_choices = [('1', _('VEHICLES')), ('2', _('Cars')), ('3', _('Motorcycles'))]
    my_choices = [('Vh', 'Vehicles'), ('Cr', 'Cars'), ('Mr', 'Motorcycles')]
    startDate = DateField("Start Date", default=date.today(), format='%Y-%m-%d',
                          validators=[DataRequired(message="You need to enter the start date")],)
    endDate = DateField("End Date", validators=[DataRequired(
        message="You need to enter the end date.")], format='%Y-%m-%d')
    linesList = SelectMultipleField(
        "Select Line(s)", choices=my_choices, id="linesList")


@scadaSemLinesPage.route('/create', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def create():
    form = CreateScadSemLinesForm(request.form)
    if request.method == 'POST' and form.validate():
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        # linesName = request.form.getlist('LinesList')
        # get file config
        linesConfig = getLinesMappings()
        linesList = linesConfig['Lines'].dropna()
        # linesList = ["AC-91", "BL-91", "CG-91", "DB-91", "DC-91", "DG-91", "DW-91", "EM-91", "GA-91",
        #             "GM-91", "JD-96", "JD-97", "JH-91", "JY-91", "KA-91", "KB-91", "KO-97", "KO-98",
        #             "KS-91", "KW-91", "LK-91", "MB-91", "MD-96", "MD-97", "MN-91", "NS-91", "RG-91",
        #             "RK-91", "SA-91", "SK-91", "SS-91", "TA-91", "TA-94", "TR-91", "VI-96",
        #             "VI-97", "VI-99", "VI-V4", "VI-V5", "SO-91", "LA-91", "GD-91", "KH-91"]
        for lineName in linesList:
            isRawCreationSuccess = False
            # get the scada sem data of 1st re name for GRAPH PLOTTING
            try:
                scadaSemLineRecord = fetchScadaSemLineRawData(scadaLineFolderPath, semLineFolderPath,
                                                            startDate, endDate,  lineName)
                isRawCreationSuccess = scadaSemLinesRepo.pushScadaSemLinesRecord(
                    scadaSemLineRecord)
            except:
                print("An exception occured")
            if isRawCreationSuccess:
                # print("स्काडा सेम लाइंस डेटा प्रविष्टि {} के लिए सफल".format(linesName))
                print("{} Line Done".format(lineName))
            else:
                print("स्काडा सेम लाइंस डेटा प्रविष्टि {} के लिए असफल".format(lineName))
        # print(errorPerc[0])
        startDate = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strftime(endDate, '%Y-%m-%d')
        if isRawCreationSuccess:
            x = {'message': 'Scada Sem Lines Data insertion successful!!!'}
            return render_template('scadaSemLines/create.html.j2', data=x, startDate=startDate, endDate=endDate, form=form)

        return render_template('scadaSemLines/create.html.j2', startDate=startDate, endDate=endDate, form=form)
    # in case of get request just return the html template
    return render_template('scadaSemLines/create.html.j2', form=form)


@scadaSemLinesPage.route('/plot', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def plot():
    # in case of post request, fetch
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("testing {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        stationList = request.form.getlist('linesList')
        # get file config
        linesConfig = getLinesMappings()
        # linesName = linesConfig['Lines'].dropna()
        linesName = []
        for currStation in stationList:
            for index, row in linesConfig.iterrows():
                if currStation == row['Display_Name']:
                    linesName.append(linesConfig['Lines'][index])

        # print(linesName)

        # testing of multiple div dynamically
        dfData_g = []
        errorPerc = []
        linesDisplayList = []
        divItrs = []
        linesWithDataList = []
        for cItr,currLinesName in enumerate(linesName):
            # get the instance of scada sem Lines repository for GRAPH PLOTTING
            scadaSemLinesDataRepo = ScadaSemLineDataRepo(appDbConnStr)

            # fetch scada sem data from db via the repository instance of ith state
            dfData_gInd, errorPercInd = scadaSemLinesDataRepo.fetchScadaSemLineData(
                startDate, endDate, currLinesName)
            lines= lineDisplayNameFromExcel(currLinesName)
            # if errorPercInd != 0:
            linesDisplayList.append(lines)
            dfData_g.append(dfData_gInd)
            errorPerc.append(errorPercInd)
            divItrs.append(cItr+1)
            linesWithDataList.append(currLinesName)
        # print(errorPerc[0])
        startDate = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strftime(endDate, '%Y-%m-%d')
        div_info = zip(linesName, errorPerc, divItrs)
        # print(reDisplayList)
        # print(errorPerc)

        return render_template('scadaSemLines/testplot.html.j2', data=dfData_g, div_info=div_info,
                               linesName=linesName, linesDisplayList=linesDisplayList,
                               startDate=startDate, endDate=endDate)
    # in case of get request just return the html template
    return render_template('scadaSemLines/testplot.html.j2')
