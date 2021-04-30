import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import math
import CMS_lumi
import numpy as np
from tools import PostFitTools
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.ProcessLine(".x tdrstyle.cc");

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output folder name",default='')
parser.add_option("-n","--name",dest="name",help="ouptut name",default='PostfitPaper')
parser.add_option("-i","--input",dest="input",help="Input directory",default='postfit_data_blindSR__Run2/')
parser.add_option("-x","--xrange",dest="xrange",help="set range for x bins in projection",default="0,-1")
parser.add_option("-y","--yrange",dest="yrange",help="set range for y bins in projection",default="0,-1")
parser.add_option("-z","--zrange",dest="zrange",help="set range for z bins in projection",default="0,-1")
parser.add_option("-p","--projection",dest="projection",help="choose which projection should be done",default="xyz")
parser.add_option("-d","--data",dest="data",action="store_true",help="make also postfit plots",default=True)
parser.add_option("-l","--label",dest="label",help="add extra label such as pythia or herwig",default="")
parser.add_option("--log",dest="log",help="write fit result to log file",default="fit_results.log")
parser.add_option("--blind",dest="blind",action="store_true",help="Use to blind data in control region",default=False)
parser.add_option("--pdfz",dest="pdfz",help="name of pdfs lie PTZUp etc",default="")
parser.add_option("--pdfx",dest="pdfx",help="name of pdfs lie PTXUp etc",default="")
parser.add_option("--pdfy",dest="pdfy",help="name of pdfs lie PTYUp etc",default="")
parser.add_option("-t","--addTop",dest="addTop",action="store_true",help="Fit top",default=False)
parser.add_option("-M","--mass",dest="signalMass",type=float,help="signal mass",default=1560.)
parser.add_option("--signalScaleF",dest="signalScaleF",type=float,help="scale factor to apply to signal when drawing so its still visible!",default=500.)
parser.add_option("--prelim",dest="prelim",help="add preliminary label",default="Preliminary")
parser.add_option("--channel",dest="channel",help="which category to use? ",default="VV_HPHP")
parser.add_option("--slopes",dest="slopes",action="store_true",help="save ttbar slopes",default=False)
parser.add_option("--pseudo",dest="pseudo",action="store_true",help="write pseudodata in legend",default=False)

(options,args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)

def addPullPlot(hdata,hpostfit,nBins,error_band):
    #print "make pull plots: (data-fit)/sigma_data"                                                                                                                                  
    N = hdata.GetNbinsX()
    gpost = ROOT.TGraphErrors(0)
    gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
    for i in range(1,N+1):
        m = hdata.GetXaxis().GetBinCenter(i)
        #ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/hdata.GetBinErrorUp(i)                                                                                      
        if hpostfit.GetBinContent(i) <= hdata.GetBinContent(i):
            if error_band !=0: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ ROOT.TMath.Abs(hdata.GetBinErrorUp(i))
            else: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ hdata.GetBinErrorUp(i)
        else:
            if error_band!=0: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ ROOT.TMath.Sqrt(ROOT.TMath.Abs( pow(hdata.GetBinErrorUp(i),2) - pow(error_band.GetErrorYlow(i-1),2) ))
            else: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ hdata.GetBinErrorUp(i)
            gpost.SetPoint(i-1,m,ypostfit)
            gt.SetBinContent(i,ypostfit)
            #print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"err data",hdata.GetBinErrorUp(i),"err fit",error_band.GetBinError(i),"pull postfit",ypostfit                                                                                                                                                                               
            #print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"err data",hdata.GetBinErrorUp(i),"err fit",error_band.GetErrorYhigh(i-1),"pull postfit",ypostfit                                                                                                                                                                           

    gpost.SetLineColor(colors[1])
    gpost.SetMarkerColor(colors[1])
    gpost.SetFillColor(ROOT.kGray+3)
    gpost.SetMarkerSize(1)
    gpost.SetMarkerStyle(20)
    gt.SetFillColor(ROOT.kGray+3)
    gt.SetLineColor(ROOT.kGray+3)
    gt.SetTitle("")
    #gt.SetMinimum(0.5);                                                                                                                                                             
    #gt.SetMaximum(1.5);                                                                                                                                                             
    gt.SetMinimum(-3.5);
    #gt.SetMaximum(3.5);                                                                                                                                                             
    gt.SetDirectory(0);
    gt.SetStats(0);
    gt.SetLineStyle(0);
    gt.SetMarkerStyle(20);
    gt.GetXaxis().SetTitle(hpostfit.GetXaxis().GetTitle());
    gt.GetXaxis().SetLabelFont(42);
    gt.GetXaxis().SetLabelOffset(0.02);
    gt.GetXaxis().SetLabelSize(0.17);
    gt.GetXaxis().SetTitleSize(0.15);
    gt.GetXaxis().SetTitleOffset(1.2);
    gt.GetXaxis().SetTitleFont(42);
    gt.GetYaxis().SetTitle("#frac{Data-fit}{#sigma}");
    gt.GetYaxis().CenterTitle(True);
    gt.GetYaxis().SetNdivisions(205);
    gt.GetYaxis().SetLabelFont(42);
    gt.GetYaxis().SetLabelOffset(0.007);
    gt.GetYaxis().SetLabelSize(0.15);
    gt.GetYaxis().SetTitleSize(0.15);
    gt.GetYaxis().SetTitleOffset(0.4);
    gt.GetYaxis().SetTitleFont(42);
    gt.GetXaxis().SetNdivisions(505)
    #gpre.SetHistogram(gt);                                                                                                                                                          
    #gpost.SetHistogram(gt);                                                                                                                                                         
    return [gt]

def get_canvas(cname):
    
    #change the CMS_lumi variables (see CMS_lumi.py)                                                                                                                                 
    CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
    CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
    period = "Run2"
    if options.name.find("2017")!=-1: period = "2017"
    if options.name.find("2018")!=-1: period = "2018"
    if options.name.find("16+17")!=-1: period = "16+17"
    if options.name.find("2016")!=-1: period = "2016"
    if period =="2016":  CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
    if period =="2017":  CMS_lumi.lumi_13TeV = "41.5 fb^{-1}"
    if period =="2018":  CMS_lumi.lumi_13TeV = "59.7 fb^{-1}"
    if period =="16+17":  CMS_lumi.lumi_13TeV = "77.6 fb^{-1}"
    if period =="Run2":  CMS_lumi.lumi_13TeV = "137.2 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.lumi_sqrtS = "13 TeV (2016+2017)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)                                                  
    CMS_lumi.extraText = options.prelim




    H_ref = 600
    W_ref = 600
    W = W_ref
    H  = H_ref
    
    iPeriod = 0
    
    # references for T, B, L, R                                                                                                                                                      
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.15*W_ref #0.12
    R = 0.04*W_ref
    
    canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx()
    canvas.SetTicky()
    
    return canvas

def get_pad(name):
    
    #change the CMS_lumi variables (see CMS_lumi.py)                                                                                                                                 
    CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
    CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
    period = "Run2"
    if options.name.find("2017")!=-1: period = "2017"
    if options.name.find("2018")!=-1: period = "2018"
    if options.name.find("16+17")!=-1: period = "16+17"
    if options.name.find("2016")!=-1: period = "2016"
    if period =="2016":  CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
    if period =="2017":  CMS_lumi.lumi_13TeV = "41.5 fb^{-1}"
    if period =="2018":  CMS_lumi.lumi_13TeV = "59.7 fb^{-1}"
    if period =="16+17":  CMS_lumi.lumi_13TeV = "77.6 fb^{-1}"
    if period =="Run2":  CMS_lumi.lumi_13TeV = "137.2 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.lumi_sqrtS = "13 TeV (2016+2017)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)                                                  
    CMS_lumi.extraText = options.prelim
    
    CMS_lumi.lumiText = "(13 TeV)"
    iPos = 0
    if( iPos==0 ): CMS_lumi.relPosX = 0.014
    CMS_lumi.relPosX=0.05
    H_ref = 600
    W_ref = 600
    W = W_ref
    H  = H_ref
    
    iPeriod = 0
    iPeriod = 4
    
    pad = ROOT.TPad(name, name, 0, 0.3, 1, 1.0)
    pad.SetFillColor(0)
    pad.SetBorderMode(0)
    pad.SetFrameFillStyle(0)
    pad.SetFrameBorderMode(0)
    pad.SetTickx()
    pad.SetTicky()

    pad.SetBottomMargin(0.01)
    pad.SetTopMargin(0.1)

    return pad






def GetHist(infile,histname):
    print " file opened "
    hist = infile.Get(histname)
    print " hist ",hist
    hist.SetDirectory(0)
    return hist





def Plot(categories,histos,axis,signal1=None,signal2=None):
    print histos
    extra1 = ''
    extra2 = ''
    htitle = ''
    xtitle = ''
    ymin = 0
    ymax = 0
    xrange = options.xrange
    yrange = options.yrange
    zrange = options.zrange
    if options.xrange == '0,-1': xrange = '55,215'
    if options.yrange == '0,-1': yrange = '55,215'
    if options.zrange == '0,-1': zrange = '1246,7600' #5500'                                                                                                                    
    xlow = xrange.split(',')[0]
    xhigh = xrange.split(',')[1]
    ylow = yrange.split(',')[0]
    yhigh = yrange.split(',')[1]
    if options.blind == True:
        if len(xrange.split(',')) == 4:
            xlow2 = xrange.split(',')[2]
            xhigh2 = xrange.split(',')[3]
        if len(yrange.split(',')) == 4:
            ylow2 = yrange.split(',')[2]
            yhigh2 = yrange.split(',')[3]

    if axis=='z':
        print "make Z projection"
        htitle = "Z-Proj. x : "+options.xrange+" y : "+options.yrange
        hhtitle = options.channel
        xtitle = "Dijet invariant mass [GeV]"
        ymin = 0.2
        ymax = histos[categories[0]]["Data"].GetMaximum()*5000
        extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
        if options.blind == True and len(xrange.split(',')) == 4:
            extra1 = 'Blind '+xhigh+' < m_{jet1} < '+xlow2+' GeV'        #xlow+' < m_{jet1} < '+xhigh+' & '+xlow2+' < m_{jet1} < '+xhigh2+' GeV'                                     
            extra2 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
        if options.blind == True and len(yrange.split(',')) == 4:
            extra2 = 'Blind '+yhigh+' < m_{jet2} < '+ylow2+' GeV'  #extra2 = ylow+' < m_{jet2} < '+yhigh+' & '+ylow2+' < m_{jet2} < '+yhigh2+' GeV'                                  
    elif axis=='x':
        print "make X projection"
        htitle = "X-Proj. y : "+options.yrange+" z : "+options.zrange
        hhtitle = options.channel
        xtitle = " m_{jet1} [GeV]"
        ymin = 0.02
        ymax = histos[categories[0]]["Data"].GetMaximum()*2#max(hdata.GetMaximum()*1.3,maxY*1.3)                                                                              
        extra1 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
        if options.blind == True and len(yrange.split(',')) == 4:
            extra1 = 'Blind '+yhigh+' < m_{jet2} < '+ylow2+' GeV'  #extra1 = ylow+' < m_{jet2} < '+yhigh+' & '+ylow2+' < m_{jet2} < '+yhigh2+' GeV'                                  
            extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
    elif axis=='y':
        print "make Y projection"
        htitle = "Y-Proj. x : "+options.xrange+" z : "+options.zrange
        hhtitle = options.channel
        xtitle = " m_{jet2} [GeV]"
        ymin = 0.02
        ymax = histos[categories[0]]["Data"].GetMaximum()*2#max(hdata.GetMaximum()*1.3,maxY*1.3)                                                                                
        extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
        if options.blind == True and len(xrange.split(',')) == 4:
            extra1 = 'Blind '+xhigh+' < m_{jet1} < '+xlow2+' GeV'  #extra1 = xlow+' < m_{jet1} < '+xhigh+' & '+xlow2+' < m_{jet1} < '+xhigh2+' GeV'                                  
            extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'

    leg = ROOT.TLegend(0.6,0.6,0.88,0.9)
    leg.SetTextSize(0.04)
    c = get_canvas('c')
    #pad1 = get_pad("pad1") #ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)                                                                                                           
    if axis == 'z': c.SetLogy()
    histos[categories[0]]["Data"].SetLineColor(ROOT.kBlack)
    histos[categories[0]]["Data"].SetLineWidth(2)
    histos[categories[0]]["Data"].SetLineStyle(1)
    histos[categories[0]]["Data"].SetMarkerColor(ROOT.kBlack)
    histos[categories[0]]["Data"].SetMarkerStyle(20)
    leg.AddEntry(histos[categories[0]]["Data"],"Background Fit","l")
    leg.AddEntry(histos[categories[0]]["Data"],"Data","ep")

    #pad1.Draw()
    #pad1.cd()
    leg.SetLineColor(0)

    for cat in categories:
        for sample in histos[cat].keys():
            histos[cat][sample].SetMinimum(ymin)
            histos[cat][sample].SetMaximum(ymax)
            histos[cat][sample].SetTitle(hhtitle)
            histos[cat][sample].SetLineColor(colors[cat])
            histos[cat][sample].SetMarkerColor(colors[cat])
            histos[cat][sample].SetMarkerStyle(markers[cat])

            if "Data" in sample :
                histos[cat][sample].SetMarkerSize(0.7)
                histos[cat][sample].Draw("samePE0")
                #leg.AddEntry(histos[cat][sample],"Data "+cat.replace("_"," "),"ep")
            else:
                histos[cat][sample].SetLineWidth(2)
                histos[cat][sample].SetLineStyle(linestyles[cat])
                histos[cat][sample].Draw('HISTsame')

            histos[cat][sample].GetXaxis().SetTitle(xtitle)
            histos[cat][sample].GetYaxis().SetTitleOffset(1.5)
            binwidth = histos[cat][sample].GetXaxis().GetBinWidth(10)
            if axis == "z": binwidth = 100
            histos[cat][sample].GetYaxis().SetTitle("Events / "+str(binwidth)+" GeV")
            histos[cat][sample].GetYaxis().SetTitleSize(0.05)
            histos[cat][sample].GetYaxis().SetLabelSize(0.05)
            histos[cat][sample].GetXaxis().SetTitleSize(0.05)
            histos[cat][sample].GetXaxis().SetLabelSize(0.05)



            '''
            if errors!=None:
            errors[0].SetFillColor(colors[0])
            errors[0].SetFillStyle(3001)
            errors[0].SetLineColor(colors[0])
            errors[0].SetLineWidth(0)
            errors[0].SetMarkerSize(0)
            '''

            #change this scaling in case you don't just want to plot signal! has to match number of generated signal events
            scaling = options.signalScaleF
            eff = 0.1

            if signal1!= None: # and (options.name.find('sigonly')!=-1  and doFit==0):
                print "print do hsignal1 ", signal1.Integral()
                #if signal1.Integral()!=0.:
                #signal1.Scale(scaling/normsig.getVal())
                signal1.SetLineColor(ROOT.kGreen-6)
                signal1.SetLineStyle(1)
                signal1.Draw("HISTsame")
                leg.AddEntry(siganl1,"G_{bulk} (%i TeV) #rightarrow WW (#times %i)"%(options.signalMass/1000.,scaling) ,"F")

            if signal2!= None: # and (options.name.find('sigonly')!=-1  and doFit==0):
                print "print do hsignal2 ", signal2.Integral()
                #if signal2.Integral()!=0.:
                #signal2.Scale(scaling/normsig.getVal())
                signal2.SetLineColor(ROOT.kViolet)
                signal2.SetLineStyle(2)
                signal2.Draw("HISTsame")
                leg.AddEntry(siganl2,"Z' (%i TeV) #rightarrow ZH (#times %i)"%(options.signalMass/1000.,scaling) ,"F")

            '''     
            if errors!=None:
            if axis=="z":
            errors[0].Draw("2same")
            else:
            errors[0].Draw("3same")
            '''

            '''
            if errors!=None:
                leg.AddEntry(errors[0],"#pm 1#sigma unc.","f")
            
            if (options.signalMass%1000.)==0:
                text = "G_{bulk} (%i TeV) #rightarrow WW (#times %i)"%(options.signalMass/1000.,scaling)

            if signalName.find("ZprimeWW")!=-1:
                text = "Z' (%.1f TeV) #rightarrow WW (#times %i)"%(options.signalMass/1000.,scaling)
            if (options.signalMass%1000.)==0:
                text = "Z' (%i TeV) #rightarrow WW (#times %i)"%(options.signalMass/1000.,scaling)

            if signalName.find("ZprimeZH")!=-1:
                text = "Z' (%.1f TeV) #rightarrow ZH (#times %i)"%(options.signalMass/1000.,scaling)
            if (options.signalMass%1000.)==0:
                text = "Z' (%i TeV) #rightarrow ZH (#times %i)"%(options.signalMass/1000.,scaling)

            if signalName.find("WprimeWZ")!=-1:
            text = "W' (%.1f TeV) #rightarrow WZ (#times %i)"%(options.signalMass/1000.,scaling)
            if (options.signalMass%1000.)==0:
                text = "W' (%i TeV) #rightarrow WZ (#times %i)"%(options.signalMass/1000.,scaling)

            if signalName.find("WprimeWH")!=-1:
            text = "W' (%.1f TeV) #rightarrow WH (#times %i)"%(options.signalMass/1000.,scaling)
            if (options.signalMass%1000.)==0:
                text = "W' (%i TeV) #rightarrow WH (#times %i)"%(options.signalMass/1000.,scaling)
            '''
        #still in the category loop
        leg.AddEntry(histos[cat]["BackgroundFit"],cat.replace("_"," "),"epl")

    leg.Draw("same")

    #errors[0].Draw("E2same")                                                                                                                                                        
    print "projection "+extra1+"  "+extra2+" \n"

 
    pt3 = ROOT.TPaveText(0.18,0.55,0.39,0.68,"NDC")
    pt3.SetTextFont(42)
    pt3.SetTextSize(0.04)
    pt3.SetTextAlign(12)
    pt3.SetFillColor(0)
    pt3.SetBorderSize(0)
    pt3.SetFillStyle(0)
    pt3.AddText(extra1)
    pt3.AddText(extra2)
    pt3.Draw()
    
    CMS_lumi.CMS_lumi(c, 4, 10)
    
    #pad1.Modified()
    #pad1.Update()
    #c.Update()
    #c.cd()
    #pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    #pad2.SetTopMargin(0.01)
    #pad2.SetBottomMargin(0.4)
    #pad2.SetGridy()                                                                                                                                                                 
    #pad2.Draw()
    #pad2.cd()
    
    #for ratio                                                                                                                                                                      
    #graphs = addRatioPlot(hdata,histos[cat][sample],nBins,errors[0])                                                                                                           
    #graphs[1].Draw("AP")                                                                                                                                                           
    #graphs[0].Draw("E3same")                                                                                                                                                       
    #graphs[1].Draw("Psame")                                                                                                                                                        

    #for pulls
    '''
    if errors ==None: errors=[0,0];
    if options.name.find('sigonly')!=-1: graphs = addPullPlot(hdata,hsig,nBins,errors[0])
    else:
    graphs = addPullPlot(hdata,histos[cat][sample],nBins,errors[0])
    # graphs = addRatioPlot(hdata,histos[cat][sample],nBins,errors[0])                                                                                                                         
    graphs[0].Draw("HIST")
    '''
    #pad2.Modified()
    #pad2.Update()
    
    #c.cd()
    c.Update()
    c.Modified()
    c.Update()
    c.cd()
    c.SetSelected(c)
    label = "VVcat"
    if "VH" in categories[0]: label="VHcat"
    elif signal1 != None: label="WithSig"+categpries[0]
    if options.prelim==0:
        outputname= options.output+options.name+label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')
        print "save plot as ", outputname+".pdf"
    else:
        outputname= options.output+options.name+label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+"_prelim"
        print "save plot as ",   outputname+".pdf"
    c.SaveAs(outputname+".png")
    c.SaveAs(outputname+".pdf")
    c.SaveAs(outputname+".C")
    c.SaveAs(outputname+".root")






colors={"VV_HPHP":1,"VH_HPHP":1,"VBF_VV_HPHP":600,"VBF_VH_HPHP":600,"VV_HPLP":619,"VH_HPLP":619,"VBF_VV_HPLP":616,"VBF_VH_HPLP":616,"VH_LPHP":635,"VBF_VH_LPHP":632}
markers={"VV_HPHP":20,"VH_HPHP":20,"VBF_VV_HPHP":24,"VBF_VH_HPHP":24,"VV_HPLP":21,"VH_HPLP":21,"VBF_VV_HPLP":25,"VBF_VH_HPLP":25,"VH_LPHP":22,"VBF_VH_LPHP":26}
linestyles={"VV_HPHP":1,"VH_HPHP":1,"VBF_VV_HPHP":2,"VBF_VH_HPHP":2,"VV_HPLP":3,"VH_HPLP":3,"VBF_VV_HPLP":4,"VBF_VH_HPLP":4,"VH_LPHP":5,"VBF_VH_LPHP":6}
categories_VV=["VV_HPHP","VBF_VV_HPHP","VV_HPLP","VBF_VV_HPLP"]
categories_VH=["VH_HPHP","VBF_VH_HPHP","VH_HPLP","VBF_VH_HPLP","VH_LPHP","VBF_VH_LPHP"]
categories_all=["VV_HPHP","VBF_VV_HPHP","VV_HPLP","VBF_VV_HPLP","VH_HPHP","VBF_VH_HPHP","VH_HPLP","VBF_VH_HPLP","VH_LPHP","VBF_VH_LPHP"]
histnames=["Data","BackgroundFit"]


if __name__ == '__main__':

    for p in options.projection:
        print " doing projection ",p

        if p == "x": 
            htitle = "X-Proj. y : "+options.yrange+" z : "+options.zrange
        elif p == "y":
            htitle = "Y-Proj. x : "+options.xrange+" z : "+options.zrange
        elif p == "z":
            htitle = "Z-Proj. x : "+options.xrange+" y : "+options.yrange
        else:
            print "Error:  unknown proj ",p
            sys.exit()

        hists={}
        for c in categories_all:
            hists[c]={}
            print " getting hists for category ",c

            filename=options.input+"/Histos"+c+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+".root"
            r_file = ROOT.TFile.Open(filename,"READ")
            print " filename ",filename
            for histname in histnames:
                print 
                hists[c][histname]= GetHist(r_file,histname)
                print " hists[c][histname] ",hists[c][histname]

            r_file.Close()
        Plot(categories_VV,hists,p)                
        Plot(categories_VH,hists,p)