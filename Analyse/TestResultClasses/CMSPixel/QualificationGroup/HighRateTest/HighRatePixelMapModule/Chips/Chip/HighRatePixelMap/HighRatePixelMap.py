import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_Chips_Chip_HighRatePixelMap_TestResult"
        self.NameSingle = "HighRatePixelMap"
        self.Title = "Pixel Map"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePixelMap'

    def OpenFileHandle(self):
        fileHandleName =  self.RawTestSessionDataPath + "/" + self.Attributes["TestResultSubDirectory"] + '/commander_HighRateTest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandleName)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the hitmap from the ROOT file
        histname = "hitmap_C" + str(self.Attributes["ChipNo"])
        hitmap = self.FileHandle.Get(histname).Clone(self.GetUniqueID())
        if not hitmap:
            print "Error: could not find histogram " + histname + "!"
            return
        self.ResultData['Plot']['ROOTObject'] = hitmap
        self.ResultData['Plot']['ROOTObject'].SetTitle("")
        self.ResultData['Plot']['ROOTObject'].SetStats(False)
        self.ResultData['Plot']['ROOTObject'].SetMinimum(0)
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        self.ResultData['Plot']['ROOTObject'].Draw("colz")
        if self.SavePlotFile:
             self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
