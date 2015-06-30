import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='GradingOverview'
    	self.NameSingle='GradingOverview'
        self.Title = 'Grading overview'
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []

    def GenerateOverview(self):

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        Final_Grades = []


        TableData = [
            [
                {'Class' : 'Header', 'Value' : 'Tested modules:'}, {'Class' : 'Value', 'Value' : "%d"%len(ModuleIDsList)}
            ]
        ]
        HTML = self.Table(TableData)

        for ModuleID in ModuleIDsList:

            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''

            ModuleGrades = []

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'm20_1':
                        FTMinus20BTC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'p17_1':
                        FT17 =  RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])


            if len(FTMinus20BTC) > 0 and len(FTMinus20ATC) > 0 and len(FT17) > 0 and len(XrayHR) > 0:
                FinalGrade = 'None'
                if 'C' in ModuleGrades:
                    FinalGrade = 'C'
                elif 'B' in ModuleGrades:
                    FinalGrade = 'B'
                elif 'A' in ModuleGrades:
                    FinalGrade = 'A'
                Final_Grades.append(FinalGrade)

            FTMinus20BTC_Grades.append(FTMinus20BTC)
            FTMinus20ATC_Grades.append(FTMinus20ATC)
            FT17_Grades.append(FT17)
            XrayCal_Grades.append(XrayCal)
            XrayHR_Grades.append(XrayHR)

        TableData = []
        TableData.append(    
            [
                {'Class' : 'Header', 'Value' : 'Grade'}, {'Class' : 'Header', 'Value' : 'A'}, {'Class' : 'Header', 'Value' : 'B'}, {'Class' : 'Header', 'Value' : 'C'}
            ]
        )

        ### Full Qualification
        TableData.append(
            [{'Class' : 'Value', 'Value' : 'T = -20 BTC'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20BTC_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20BTC_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20BTC_Grades if x=='C']) }]
        )
        TableData.append(
            [{'Class' : 'Value', 'Value' : 'T = -20 ATC'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20ATC_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20ATC_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FTMinus20ATC_Grades if x=='C']) }]
        )
        TableData.append(
            [{'Class' : 'Value', 'Value' : 'T = +17 ATC'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FT17_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FT17_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in FT17_Grades if x=='C']) }]
        )

        ### X-ray
        TableData.append(    
            [{'Class' : 'Value', 'Value' : 'High Rate'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in XrayHR_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in XrayHR_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in XrayHR_Grades if x=='C']) }]
        )

        ### Final
        TableData.append(    
            [{'Class' : 'Header', 'Value' : 'Final'}, {'Class' : 'Value', 'Value' : "%d"%len([x for x in Final_Grades if x=='A']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in Final_Grades if x=='B']) }, {'Class' : 'Value', 'Value' : "%d"%len([x for x in Final_Grades if x=='C']) }]
        )

        HTML += self.Table(TableData) + self.BoxFooter("<b>Final</b> only counts modules with all necessary tests done.")

        return self.Boxed(HTML)

