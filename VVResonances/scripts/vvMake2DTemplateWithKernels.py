#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for x",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-w","--weights",dest="weights",help="additional weights",default='')
parser.add_option("-u","--usegenmass",dest="usegenmass",action="store_true",help="use gen mass for det resolution",default=False)
parser.add_option("-e","--firstEv",dest="firstEv",type=int,help="first event",default=0)
parser.add_option("-E","--lastEv",dest="lastEv",type=int,help="last event",default=-1)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")

def getBinning(binsMVV,minx,maxx,bins):
    l=[]
    if binsMVV=="":
        for i in range(0,bins+1):
            l.append(minx + i* (maxx - minx)/bins)
    else:
        s = binsMVV.split(",")
        for w in s:
            l.append(int(w))
    return l



def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    maxFactor = max(pow(histo.GetXaxis().GetXmax(),power),pow(histo.GetXaxis().GetXmin(),power))
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        for j in range(1,histo.GetNbinsY()+1):
            nominal=histo.GetBinContent(i,j)
            factor = 1+alpha*pow(x,power) 
            newHistoU.SetBinContent(i,j,nominal*factor)
            newHistoD.SetBinContent(i,j,nominal/factor)
    if newHistoU.Integral()>0.0:        
        newHistoU.Scale(1.0/newHistoU.Integral())        
    if newHistoD.Integral()>0.0:        
        newHistoD.Scale(1.0/newHistoD.Integral())        
    return newHistoU,newHistoD 
    
def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
            up=histo.GetBinContent(i,j)/intUp
            nominal=histoNominal.GetBinContent(i,j)/intNominal
            newHisto.SetBinContent(i,j,histoNominal.GetBinContent(i,j)*nominal/up)
    return newHisto       
	
def expandHisto(histo,options):
    histogram=ROOT.TH2F(histo.GetName(),"histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram
      
def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)
            

def smoothTail(hist):
    if hist.Integral() == 0:
        print "histogram has zero integral "+hist.GetName()
        return 0
    hist.Scale(1.0/hist.Integral())
    print "y bins " +str(hist.GetNbinsY())
    print "x bins " +str(hist.GetNbinsX())
    for i in range(1,hist.GetNbinsX()+1):
        print i
        proj=hist.ProjectionY("q",i,i)
#        for j in range(1,proj.GetNbinsX()+1):
#            if proj.GetBinContent(j)/proj.Integral()<0.0005:
#                proj.SetBinError(j,1.8)
        
        beginFit = proj.GetBinLowEdge( proj.GetMaximumBin() )
        beginFitY = beginFit + 1500. * 1/(beginFit/1000.)
        print beginFit
        print beginFitY
        #expo=ROOT.TF1("expo","expo",beginFitX,8000)
        expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",2000,8000) 
        expo.SetParameters(0,16.,2.)
        expo.SetParLimits(2,1.,20.)
        proj.Fit(expo,"LLMR","",beginFitY,8000)
        #proj.Fit(expo,"","",2000,8000)
        c = ROOT.TCanvas("c","c",400,400)
        c.SetLogy()
        proj.Draw("hist")
        proj.Draw("funcsame")
        c.SaveAs(hist.GetName()+"_bin"+str(i)+".pdf")
        beginsmooth = False
        for j in range(1,hist.GetNbinsY()+1):
            y=hist.GetYaxis().GetBinCenter(j)
            if y>beginFitY:
                if beginsmooth==False:
                   if y<3000: 
                       if abs(proj.GetBinContent(j) - expo.Eval(y)) < 0.0000001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                        print beginFitY
                        print "begin smoothing at " +str(y)
                        beginsmooth = True 
                   if abs(proj.GetBinContent(j) - expo.Eval(y)) < 0.00000001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                       print beginFitY
                       print "begin smoothing at " +str(y)
                       beginsmooth = True 
                if beginsmooth:
                    hist.SetBinContent(j,i,expo.Eval(y))



(options,args) = parser.parse_args()

weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')
print "Creating datasets for samples: " ,sampleTypes

dataPlotters=[]
dataPlottersNW=[]

for filename in os.listdir(args[0]):
 for sampleType in sampleTypes:
  if filename.find(sampleType)!=-1:
   fnameParts=filename.split('.')
   fname=fnameParts[0]
   ext=fnameParts[1]
   if ext.find("root") ==-1:
       continue
   dataPlotters.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
   dataPlotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
   dataPlotters[-1].addCorrectionFactor('xsec','tree')
   dataPlotters[-1].addCorrectionFactor('genWeight','tree')
   dataPlotters[-1].addCorrectionFactor('puWeight','tree')
   for w in weights_:
    if w != '': dataPlotters[-1].addCorrectionFactor(w,'branch')
   dataPlotters[-1].filename=fname
   dataPlottersNW.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
   dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
   dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
   for w in weights_: 
    if w != '': dataPlottersNW[-1].addCorrectionFactor(w,'branch')
   dataPlottersNW[-1].filename=fname

data=MergedPlotter(dataPlotters)

fcorr=ROOT.TFile(options.res)
scale_x=fcorr.Get("scaleyHisto")
scale_y=fcorr.Get("scalexHisto")
res_x=fcorr.Get("resyHisto")
res_y=fcorr.Get("resxHisto")

variables=options.vars.split(',')
leg = options.vars.split(',')[0].split('_')[1]



binsx=[]
for i in range(0,options.binsx+1):
    binsx.append(options.minx+i*(options.maxx-options.minx)/options.binsx)


#binsy=[1000+i*100 for i in range(41)]
binsy = getBinning(options.binsMVV,options.miny,options.maxy,options.binsy)
print binsy

scaleUp = ROOT.TH1F(scale_x)
scaleUp.SetName("scaleUp")
scaleDown = ROOT.TH1F(scale_x)
scaleDown.SetName("scaleDown")
for i in range(1,scale_x.GetNbinsX()+1):
    scaleUp.SetBinContent(i,scale_x.GetBinContent(i)+0.09)
    scaleDown.SetBinContent(i,scale_x.GetBinContent(i)-0.09)
    
mjet_mvv_nominal = ROOT.TH2F("mjet_mvv_nominal","mjet_mvv_nominal",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram = ROOT.TH2F("histo_nominal","histo_nominal",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_scale_up = ROOT.TH2F("histo_nominal_ScaleUp","histo_nominal_ScaleUp",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_scale_down = ROOT.TH2F("histo_nominal_ScaleDown","histo_nominal_ScaleDown",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

mjet_mvv_altshapeUp = ROOT.TH2F("mjet_mvv_altshapeUp","mjet_mvv_altshapeUp",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_altshapeUp = ROOT.TH2F("histo_altshapeUp","histo_altshapeUp",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_altshape_scale_up = ROOT.TH2F("histo_altshape_ScaleUp","histo_altshape_ScaleUp",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_altshape_scale_down = ROOT.TH2F("histo_altshape_ScaleDown","histo_altshape_ScaleDown",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

mjet_mvv_altshape2 = ROOT.TH2F("mjet_mvv_altshape2","mjet_mvv_altshape2",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_altshape2 = ROOT.TH2F("histo_altshape2","histo_altshape2",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

mjet_mvv_nominal_3D = ROOT.TH3F("mjet_mvv_nominal_3D","mjet_mvv_nominal_3D",len(binsx)-1,array('f',binsx),len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

#systematics
histograms=[
    histogram,
    #histogram_scale_up,
    #histogram_scale_down,
    #histogram_altshapeUp,
    #histogram_altshape_scale_up,
    #histogram_altshape_scale_down,    
    #histogram_altshape2
]

#ok lets populate!

maxEvents = -1
varsDataSet = 'jj_%s_gen_pt,%s,%s'%(leg,variables[1],variables[0])

for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):
 
 #Nominal histogram Pythia8
 if plotter.filename.find(sampleTypes[0].replace('.root','')) != -1:
  print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
  print "filename: ", plotter.filename, " preparing central values histo"
 
  #histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  #norm=histI.Integral()
  #y:x
  histI2D=plotter.drawTH2Binned("jj_LV_mass:jj_%s_softDrop_mass"%(leg),options.cut,"1",array('f',binsx),array('f',binsy),"Softdrop mass","M_{JJ} mass","GeV","GeV","COLZ" )
  hist3D=plotter.drawTH3Binned("jj_LV_mass:jj_l1_softDrop_mass:jj_l2_softDrop_mass",options.cut,"1",array('f',binsx),array('f',binsx),array('f',binsy),"M_{JJ} mass","GeV","Softdrop mass","GeV","COLZ" )

  print " - Creating dataset - "
  #dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)
  dataset=plotterNW.makeDataSet(varsDataSet,options.cut,options.firstEv,options.lastEv)

  print " - Creating 2D gaussian template - "
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scale_x,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  # histTMP.Scale(histI.Integral()/histTMP.Integral())
  # histogram.Add(histTMP)
  #if histI2D.Integral()>0: 
  # histI2D.Scale(histI.Integral()/histI2D.Integral())
  # mjet_mvv_nominal.Add(histI2D)

  if histTMP.Integral()>0:
   histTMP.Scale(histI2D.Integral()/histTMP.Integral())
   histogram.Add(histTMP)
   mjet_mvv_nominal.Add(histI2D)
   mjet_mvv_nominal_3D.Add(hist3D)
   
  #histI.Delete()  	  
  histTMP.Delete()

  #print " - Creating 2D gaussian template scale up - "
  #histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  #if not(options.usegenmass): 
  # datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scaleUp,scale_y,res_x,res_y,histTMP)
  #else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scaleUp,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  # histTMP.Scale(histI2D.Integral()/histTMP.Integral())
  # histogram_scale_up.Add(histTMP)
    	  
  #histTMP.Delete()

  #print " - Creating 2D gaussian template scale down - "
  #histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  #if not(options.usegenmass): 
  # datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scaleDown,scale_y,res_x,res_y,histTMP)
  #else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scaleDown,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  # histTMP.Scale(histI2D.Integral()/histTMP.Integral())
  # histogram_scale_down.Add(histTMP)
    
  histI2D.Delete()	
  hist3D.Delete()  
  #histTMP.Delete()
    
 if len(sampleTypes)<2: continue 
 elif plotter.filename.find(sampleTypes[1].replace('.root','')) != -1: #alternative shape Herwig
  print "Preparing alternative shapes for sampletype " ,sampleTypes[1]
  print "filename: ", plotter.filename, " preparing alternate shape histo"

  #histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  #norm=histI.Integral()
  histI2D=plotter.drawTH2Binned("jj_LV_mass:jj_%s_softDrop_mass"%(leg),options.cut,"1",array('f',binsx),array('f',binsy),"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )

  print " - Creating dataset - "
  #dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)
  dataset=plotterNW.makeDataSet(varsDataSet,options.cut,options.firstEv,options.lastEv)

  print " - Creating 2D gaussian template - "
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scale_x,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  #  histTMP.Scale(histI.Integral()/histTMP.Integral())
  #  histogram_altshapeUp.Add(histTMP)
  #if histI2D.Integral()>0: 
  #  histI2D.Scale(histI.Integral()/histI2D.Integral())
  #  mjet_mvv_altshapeUp.Add(histI2D)

  if histTMP.Integral()>0:
    histTMP.Scale(histI2D.Integral()/histTMP.Integral())
    histogram_altshapeUp.Add(histTMP)
    mjet_mvv_altshapeUp.Add(histI2D)
   
  #histI.Delete()  
  histTMP.Delete()

  print " - Creating 2D gaussian template scale up - "
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scaleUp,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scaleUp,scale_y,res_x,res_y,histTMP)

  if histTMP.Integral()>0:
    histTMP.Scale(histI2D.Integral()/histTMP.Integral())
    histogram_altshape_scale_up.Add(histTMP)
    
  histTMP.Delete()

  print " - Creating 2D gaussian template scale down - "
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scaleDown,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scaleDown,scale_y,res_x,res_y,histTMP)

  if histTMP.Integral()>0:
    histTMP.Scale(histI2D.Integral()/histTMP.Integral())
    histogram_altshape_scale_down.Add(histTMP)
    
  histI2D.Delete()
  histTMP.Delete()
    
 if len(sampleTypes)<3: continue 
 elif plotter.filename.find(sampleTypes[2].replace('.root','')) != -1: #alternative shape Pythia8+Madgraph (not used for syst but only for cross checks)
  print "Preparing alternative shapes for sampletype " ,sampleTypes[2]
  print "filename: ", plotter.filename, " preparing alternate shape histo"

  #histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  #norm=histI.Integral()

  histI2D=plotter.drawTH2("jj_LV_mass:jj_%s_softDrop_mass"%(leg),options.cut,"1",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy),"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

  print " - Creating dataset - "
  #dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)
  dataset=plotterNW.makeDataSet(varsDataSet,options.cut,options.firstEv,options.lastEv)

  print " - Creating 2D gaussian template - "
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_pt'%(leg),scale_x,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_%s_gen_softDrop_mass'%(leg),scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  #  histTMP.Scale(histI.Integral()/histTMP.Integral())
  #  histogram_altshape2.Add(histTMP)
  #if histI2D.Integral()>0:  
  #  histI2D.Scale(histI.Integral()/histI2D.Integral())
  #  mjet_mvv_altshape2.Add(histI2D)

  if histTMP.Integral()>0:
    histTMP.Scale(histI2D.Integral()/histTMP.Integral())
    histogram_altshape2.Add(histTMP) 
    mjet_mvv_altshape2.Add(histI2D)
    
  #histI.Delete()  
  histI2D.Delete()
  histTMP.Delete()

f=ROOT.TFile(options.output,"RECREATE")
print "Finished producing histograms! Saving to" ,options.output
finalHistograms={}
f.cd()
for hist in histograms:
 print "Working on histogram " ,hist.GetName()
 hist.Write(hist.GetName()+"_coarse")
 #smooth
 #print "Smoothing tail for " ,hist.GetName()
 #smoothTail(hist)
 print "Creating conditional histogram for ",hist.GetName()
 conditional(hist)
 print "Expanding for " ,hist.GetName()
 expanded=expandHisto(hist,options)
 conditional(expanded)
 expanded.Write()
 finalHistograms[hist.GetName()]=expanded

mjet_mvv_nominal.Write()
mjet_mvv_altshapeUp.Write()
mjet_mvv_altshape2.Write()
mjet_mvv_nominal_3D.Write()

# ##Mirror Herwig shape
#histogram_altshapeDown=mirror(finalHistograms['histo_altshapeUp'],finalHistograms['histo_nominal'],"histo_altshapeDown")
#conditional(histogram_altshapeDown)
#histogram_altshapeDown.Write()

alpha=1.5/215.
histogram_pt_down,histogram_pt_up=unequalScale(finalHistograms['histo_nominal'],"histo_nominal_PT",alpha)
conditional(histogram_pt_down)
histogram_pt_down.Write()
conditional(histogram_pt_up)
histogram_pt_up.Write()

alpha=1.5*55.
h1,h2=unequalScale(finalHistograms['histo_nominal'],"histo_nominal_OPT",alpha,-1)
conditional(h1)
h1.Write()
conditional(h2)
h2.Write()
        		
f.Close()




