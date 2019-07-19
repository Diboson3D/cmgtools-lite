#fit HPLP MC with HPLP kernel
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root 
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample herwig --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root 
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample madgraph --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root 
#merge 1Dx2Dx2D HPLP kernels
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPLP.root --sample pythia --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root --merge
#results validation:
#python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_VV_HPLP.root,nonRes -k save_new_shapes_2016_pythia_VV_HPLP_3D.root,histo -o control-plots-HPLP-pythia
#python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_VV_HPLP_altshapeUp.root,nonRes -k save_new_shapes_2016_pythia_VV_HPLP_3D.root,histo -o control-plots-HPLP-herwig
#python Projections3DHisto.py --mc results_2016/JJ_2016_nonRes_VV_HPLP_altshape2.root,nonRes -k save_new_shapes_2016_pythia_VV_HPLP_3D.root,histo -o control-plots-HPLP-madgraph
#fit HPHP MC with post-fit HPLP kernel
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample pythia --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root 
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample herwig --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root 
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root 
#merge 1Dx2Dx2D HPHP kernels
#python transferKernelNew.py -i results_2016/JJ_2016_nonRes_VV_HPHP.root --sample madgraph --year 2016 -p z --pdfIn results_2016/JJ_2016_nonRes_3D_VV_HPLP.root --merge
#results validation:
#python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_VV_HPHP.root,nonRes -k save_new_shapes_2016_pythia_VV_HPHP_3D.root,histo -o control-plots-HPHP-pythia
#python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_VV_HPHP_altshapeUp.root,nonRes -k save_new_shapes_2016_pythia_VV_HPHP_3D.root,histo -o control-plots-HPHP-herwig
#python Projections3DHisto_HPHP.py --mc results_2016/JJ_2016_nonRes_VV_HPHP_altshape2.root,nonRes -k save_new_shapes_2016_pythia_VV_HPHP_3D.root,histo -o control-plots-HPHP-madgraph
import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.ProcessLine(".x tdrstyle.cc");
import math, copy
from tools.PostFitTools import *
from tools.DatacardTools import *
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output folder name",default='postfit_qcd/')
parser.add_option("-i","--input",dest="input",help="Input nonRes histo with MC data",default='JJ_2016_nonRes_VV_HPLP.root')
parser.add_option("--pdfIn","--pdfIn",dest="pdfIn",help="3D nonRes pdf",default='JJ_2016_nonRes_3D_VV_HPLP.root')
parser.add_option("-x","--xrange",dest="xrange",help="set range for x bins in projection",default="0,-1")
parser.add_option("-y","--yrange",dest="yrange",help="set range for y bins in projection",default="0,-1")
parser.add_option("-z","--zrange",dest="zrange",help="set range for z bins in projection",default="0,-1")
parser.add_option("-p","--projection",dest="projection",help="choose which projection should be done",default="xyz")
parser.add_option("--merge",dest="merge",action="store_true",help="Merge all kernels",default=False)
parser.add_option("--sample",dest="sample",help="pythia, madgraph or herwig",default="pythia")
parser.add_option("--pdfz",dest="pdfz",help="name of pdfs lie PTZUp etc",default="")
parser.add_option("--pdfx",dest="pdfx",help="name of pdfs lie PTXUp etc",default="")
parser.add_option("--pdfy",dest="pdfy",help="name of pdfs lie PTYUp etc",default="")
parser.add_option("--year",dest="year",help="year",default="2017")
(options,args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)

def unequalScale(histo,name,alpha,power=1,dim=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    if dim == 2:
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
    else:
	    for i in range(1,histo.GetNbinsX()+1):
	        x= histo.GetXaxis().GetBinCenter(i)
	        nominal=histo.GetBinContent(i) #ROOT.TMath.Log10(histo.GetBinContent(i))
		factor = 1+alpha*pow(x,power)
	        newHistoU.SetBinContent(i,nominal*factor)
	        if factor != 0: newHistoD.SetBinContent(i,nominal/factor)	
    return newHistoU,newHistoD 
    
def mirror(histo,histoNominal,name,dim=1):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    if dim == 2:
		for i in range(1,histo.GetNbinsX()+1):
			for j in range(1,histo.GetNbinsY()+1):
				up=histo.GetBinContent(i,j)/intUp
				nominal=histoNominal.GetBinContent(i,j)/intNominal
				if up != 0: newHisto.SetBinContent(i,j,histoNominal.GetBinContent(i,j)*nominal/up)
    else:
		for i in range(1,histo.GetNbinsX()+1):
			up=histo.GetBinContent(i)/intUp
			nominal=histoNominal.GetBinContent(i)/intNominal
			newHisto.SetBinContent(i,histoNominal.GetBinContent(i)*nominal/up)	
    return newHisto       

def expandHisto(histo,suffix,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ):
    histogram=ROOT.TH2F(histo.GetName()+suffix,"histo",binsMJ,minMJ,maxMJ,binsMVV,minMVV,maxMVV)
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram

def expandHistoBinned(histo,suffix ,binsx,binsy):
    histogram=ROOT.TH2F(histo.GetName()+suffix,"histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
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


def merge_all():
 fin_herwig_mjj = ROOT.TFile.Open('save_new_shapes_%s_herwig_%s_1D.root'%(options.year,purity),'READ') 
 histo_altshapeUp_mjj = fin_herwig_mjj.histo_nominal
 histo_altshapeUp_mjj.SetName('histo_altshapeUp')
 histo_altshapeUp_mjj.SetTitle('histo_altshapeUp')

 fin_madgraph_mjj = ROOT.TFile.Open('save_new_shapes_%s_madgraph_%s_1D.root'%(options.year,purity),'READ')
 histo_altshape2Up_mjj = fin_madgraph_mjj.histo_nominal
 histo_altshape2Up_mjj.SetName('histo_altshape2Up')
 histo_altshape2Up_mjj.SetTitle('histo_altshape2Up')
 
 fin_pythia_mjj = ROOT.TFile.Open('save_new_shapes_%s_pythia_%s_1D.root'%(options.year,purity),'UPDATE')
 histo_nominal = fin_pythia_mjj.histo_nominal
 histo_altshapeUp_mjj.Write('histo_altshapeUp')
 histo_altshapeDown_mjj = mirror(histo_altshapeUp_mjj,histo_nominal,"histo_altshapeDown")
 histo_altshapeDown_mjj.SetName('histo_altshapeDown')
 histo_altshapeDown_mjj.SetTitle('histo_altshapeDown')
 histo_altshapeDown_mjj.Write('histo_altshapeDown') 
 
 histo_altshape2Up_mjj.Write('histo_altshape2Up')
 histo_altshape2Down_mjj = mirror(histo_altshape2Up_mjj,histo_nominal,"histo_altshape2Down")
 histo_altshape2Down_mjj.SetName('histo_altshape2Down')
 histo_altshape2Down_mjj.SetTitle('histo_altshape2Down')
 histo_altshape2Down_mjj.Write('histo_altshape2Down') 
 
 fin_pythia_mjj.Close()
 fin_madgraph_mjj.Close()
 fin_herwig_mjj.Close()
 
 fin_herwig_l1 = ROOT.TFile.Open('save_new_shapes_%s_herwig_%s_COND2D_l1.root'%(options.year,purity),'READ') 
 histo_altshapeUp_l1 = fin_herwig_l1.histo_nominal
 histo_altshapeUp_l1.SetName('histo_altshapeUp')
 histo_altshapeUp_l1.SetTitle('histo_altshapeUp')
 
 fin_madgraph_l1 = ROOT.TFile.Open('save_new_shapes_%s_madgraph_%s_COND2D_l1.root'%(options.year,purity),'READ')
 histo_altshape2Up_l1 = fin_madgraph_l1.histo_nominal
 histo_altshape2Up_l1.SetName('histo_altshape2Up')
 histo_altshape2Up_l1.SetTitle('histo_altshape2Up')
 
 fin_pythia_l1 = ROOT.TFile.Open('save_new_shapes_%s_pythia_%s_COND2D_l1.root'%(options.year,purity),'UPDATE')
 histo_nominal = fin_pythia_l1.histo_nominal
 histo_altshapeUp_l1.Write('histo_altshapeUp')
 histo_altshapeDown_l1 = mirror(histo_altshapeUp_l1,histo_nominal,"histo_altshapeDown",2)
 conditional(histo_altshapeDown_l1)
 histo_altshapeDown_l1.SetName('histo_altshapeDown')
 histo_altshapeDown_l1.SetTitle('histo_altshapeDown')
 histo_altshapeDown_l1.Write('histo_altshapeDown') 
 
 histo_altshape2Up_l1.Write('histo_altshape2Up')
 histo_altshape2Down_l1 = mirror(histo_altshape2Up_l1,histo_nominal,"histo_altshape2Down",2)
 conditional(histo_altshape2Down_l1)
 histo_altshape2Down_l1.SetName('histo_altshape2Down')
 histo_altshape2Down_l1.SetTitle('histo_altshape2Down')
 histo_altshape2Down_l1.Write('histo_altshape2Down') 
 
 fin_pythia_l1.Close()
 fin_madgraph_l1.Close()
 fin_herwig_l1.Close()
 
 fin_herwig_l2 = ROOT.TFile.Open('save_new_shapes_%s_herwig_%s_COND2D_l2.root'%(options.year,purity),'READ') 
 histo_altshapeUp_l2 = fin_herwig_l2.histo_nominal
 histo_altshapeUp_l2.SetName('histo_altshapeUp')
 histo_altshapeUp_l2.SetTitle('histo_altshapeUp')
 
 fin_madgraph_l2 = ROOT.TFile.Open('save_new_shapes_%s_madgraph_%s_COND2D_l2.root'%(options.year,purity),'READ')
 histo_altshape2Up_l2 = fin_madgraph_l2.histo_nominal
 histo_altshape2Up_l2.SetName('histo_altshape2Up')
 histo_altshape2Up_l2.SetTitle('histo_altshape2Up')
 
 fin_pythia_l2 = ROOT.TFile.Open('save_new_shapes_%s_pythia_%s_COND2D_l2.root'%(options.year,purity),'UPDATE')
 histo_nominal = fin_pythia_l2.histo_nominal
 histo_altshapeUp_l2.Write('histo_altshapeUp')
 histo_altshapeDown_l2 = mirror(histo_altshapeUp_l2,histo_nominal,"histo_altshapeDown",2)
 conditional(histo_altshapeDown_l2)
 histo_altshapeDown_l2.SetName('histo_altshapeDown')
 histo_altshapeDown_l2.SetTitle('histo_altshapeDown')
 histo_altshapeDown_l2.Write('histo_altshapeDown') 
 
 histo_altshape2Up_l2.Write('histo_altshape2Up')
 histo_altshape2Down_l2 = mirror(histo_altshape2Up_l2,histo_nominal,"histo_altshape2Down",2)
 conditional(histo_altshape2Down_l2)
 histo_altshape2Down_l2.SetName('histo_altshape2Down')
 histo_altshape2Down_l2.SetTitle('histo_altshape2Down')
 histo_altshape2Down_l2.Write('histo_altshape2Down') 
 
 fin_pythia_l2.Close()
 fin_madgraph_l2.Close()
 fin_herwig_l2.Close()
 
 inputx=fin_pythia_l1.GetName()
 inputy=fin_pythia_l2.GetName()
 inputz=fin_pythia_mjj.GetName()     
 rootFile="save_new_shapes_%s_pythia_"%options.year+purity+"_3D.root"
   
 print "Reading " ,inputx
 print "Reading " ,inputy
 print "Reading " ,inputz
 print "Saving to ",rootFile 
   
 cmd='vvMergeHistosToPDF3D.py -i "{inputx}" -I "{inputy}" -z "{inputz}" -o "{rootFile}"'.format(rootFile=rootFile,inputx=inputx,inputy=inputy,inputz=inputz)
 print "going to execute "+str(cmd)
 os.system(cmd)
             
def save_shape(final_shape,norm_nonres,sample="pythia"):

    histo = ROOT.TH3F('histo','histo',len(xBinslowedge)-1,xBinslowedge,len(yBinslowedge)-1,yBinslowedge,len(zBinslowedge)-1,zBinslowedge)
    histo_xz = ROOT.TH2F('histo_xz','histo_xz',len(xBinslowedge)-1,xBinslowedge,len(zBinslowedge)-1,zBinslowedge)
    histo_yz = ROOT.TH2F('histo_yz','histo_yz',len(yBinslowedge)-1,yBinslowedge,len(zBinslowedge)-1,zBinslowedge)
    histo_z = ROOT.TH1F('histo_z','histo_z',len(zBinslowedge)-1,zBinslowedge)
    print "Done creating out histos"
    lv = {}
    for xk, xv in xBins.iteritems():
        lv[xv] = {}
        for yk, yv in yBins.iteritems():
          lv[xv][yv] = {}
          for zk,zv in zBins.iteritems():
            lv[xv][yv][zv] = 0

    lv_xz = {}
    lv_yz = {}
    for xk, xv in xBins.iteritems():
        lv_xz[xv] = {}
        lv_yz[xv] = {}
        for zk,zv in zBins.iteritems():
          lv_xz[xv][zv] = 0
          lv_yz[xv][zv] = 0

    lv_z = []
    for zk,zv in zBins.iteritems():
      lv_z.append(0)
                               
    for xk, xv in xBins.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins.iteritems():
                 MJJ.setVal(zv)
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 lv[xv][yv][zv] = final_shape.getVal(argset)*binV
                 lv_xz[xv][zv] += final_shape.getVal(argset)*binV
                 lv_yz[yv][zv] += final_shape.getVal(argset)*binV
                 lv_z[zk-1] += final_shape.getVal(argset)*binV

    for xk, xv in xBins.iteritems():
     for yk, yv in yBins.iteritems():
      for zk,zv in zBins.iteritems():
       histo.Fill(xv,yv,zv,lv[xv][yv][zv]*norm_nonres[0])

    for xk, xv in xBins.iteritems():
      for zk,zv in zBins.iteritems():
       histo_xz.Fill(xv,zv,lv_xz[xv][zv]*norm_nonres[0])
       histo_yz.Fill(xv,zv,lv_yz[xv][zv]*norm_nonres[0])
    
    for zk,zv in zBins.iteritems(): histo_z.Fill(zv,lv_z[zk-1]*norm_nonres[0])    
       
    fout_z = ROOT.TFile.Open('save_new_shapes_%s_%s_%s_1D.root'%(options.year,sample,purity),'RECREATE')
    fout_z.cd()
    histo_z.Scale(1./histo_z.Integral())
    histo_z.SetTitle('histo_nominal')
    histo_z.SetName('histo_nominal')
    histo_z.Write('histo_nominal')

    print "Now PT 1D",zBinslowedge[-1],zBinslowedge[0],xBinslowedge[-1],xBinslowedge[0]
    alpha=1.5/float(zBinslowedge[-1])    
    histogram_pt_up,histogram_pt_down=unequalScale(histo_z,"histo_nominal_PT",alpha,1)
    histogram_pt_down.SetName('histo_nominal_PTDown')
    histogram_pt_down.SetTitle('histo_nominal_PTDown')
    histogram_pt_down.Write('histo_nominal_PTDown')
    histogram_pt_up.SetName('histo_nominal_PTUp')
    histogram_pt_up.SetTitle('histo_nominal_PTUp')
    histogram_pt_up.Write('histo_nominal_PTUp')

    print "Now OPT 1D"
    alpha=1.5*float(zBinslowedge[0])
    histogram_opt_up,histogram_opt_down=unequalScale(histo_z,"histo_nominal_OPT",alpha,-1)
    histogram_opt_down.SetName('histo_nominal_OPTDown')
    histogram_opt_down.SetTitle('histo_nominal_OPTDown')
    histogram_opt_down.Write('histo_nominal_OPTDown')
    histogram_opt_up.SetName('histo_nominal_OPTUp')
    histogram_opt_up.SetTitle('histo_nominal_OPTUp')
    histogram_opt_up.Write('histo_nominal_OPTUp')
        
    fout_z.Close()
    
    fout_xz = ROOT.TFile.Open('save_new_shapes_%s_%s_%s_COND2D_l1.root'%(options.year,sample,purity),'RECREATE')
    fout_xz.cd()  
    conditional(histo_xz)
    histo_xz.SetTitle('histo_nominal')
    histo_xz.SetName('histo_nominal')
    histo_xz.Write('histo_nominal')

    print "Now PT 2D l1"
    alpha=1.5/float(xBinslowedge[-1])
    histogram_pt_up,histogram_pt_down=unequalScale(histo_xz,"histo_nominal_PT",alpha,1,2)
    conditional(histogram_pt_down)
    histogram_pt_down.SetName('histo_nominal_PTDown')
    histogram_pt_down.SetTitle('histo_nominal_PTDown')
    histogram_pt_down.Write('histo_nominal_PTDown')
    conditional(histogram_pt_up)
    histogram_pt_up.SetName('histo_nominal_PTUp')
    histogram_pt_up.SetTitle('histo_nominal_PTUp')
    histogram_pt_up.Write('histo_nominal_PTUp')

    print "Now OPT 2D l1"
    alpha=1.5*float(xBinslowedge[0])
    h1,h2=unequalScale(histo_xz,"histo_nominal_OPT",alpha,-1,2)
    conditional(h1)
    h1.SetName('histo_nominal_OPTUp')
    h1.SetTitle('histo_nominal_OPTUp')
    h1.Write('histo_nominal_OPTUp')
    conditional(h2)
    h2.SetName('histo_nominal_OPTDown')
    h2.SetTitle('histo_nominal_OPTDown')
    h2.Write('histo_nominal_OPTDown')
        
    fout_xz.Close()
    
    fout_yz = ROOT.TFile.Open('save_new_shapes_%s_%s_%s_COND2D_l2.root'%(options.year,sample,purity),'RECREATE')
    fout_yz.cd()  
    conditional(histo_yz)
    histo_yz.SetTitle('histo_nominal')
    histo_yz.SetName('histo_nominal')
    histo_yz.Write('histo_nominal')

    print "Now PT 2D l2"
    alpha=1.5/float(xBinslowedge[-1])
    histogram_pt_up,histogram_pt_down=unequalScale(histo_yz,"histo_nominal_PT",alpha,1,2)
    conditional(histogram_pt_down)
    histogram_pt_down.SetName('histo_nominal_PTDown')
    histogram_pt_down.SetTitle('histo_nominal_PTDown')
    histogram_pt_down.Write('histo_nominal_PTDown')
    conditional(histogram_pt_up)
    histogram_pt_up.SetName('histo_nominal_PTUp')
    histogram_pt_up.SetTitle('histo_nominal_PTUp')
    histogram_pt_up.Write('histo_nominal_PTUp')

    print "Now OPT 2D l2"
    alpha=1.5*float(xBinslowedge[0])
    h1,h2=unequalScale(histo_yz,"histo_nominal_OPT",alpha,-1,2)
    conditional(h1)
    h1.SetName('histo_nominal_OPTUp')
    h1.SetTitle('histo_nominal_OPTUp')
    h1.Write('histo_nominal_OPTUp')
    conditional(h2)
    h2.SetName('histo_nominal_OPTDown')
    h2.SetTitle('histo_nominal_OPTDown')
    h2.Write('histo_nominal_OPTDown')
    
    fout_yz.Close()    

def makeNonResCard():

 if options.pdfIn.find("HPHP")!=-1: category_pdf = "VV_HPHP"
 elif options.input.find("HPLP")!=-1: category_pdf = "VV_HPLP"
 else: category_pdf = "VV_LPLP"  
     
 dataset = options.year
 sig = 'BulkGWW'
 
 lumi = {'2016':35900,'2017':41367}
 lumi_unc = {'2016':1.025,'2017':1.023}
 scales = {"2017" :[0.983,1.08], "2016":[1.014,1.086]}

 vtag_unc = {'VV_HPHP':{},'VV_HPLP':{},'VV_LPLP':{}}
 vtag_unc['VV_HPHP'] = {'2016':'1.232/0.792','2017':'1.269/0.763'}
 vtag_unc['VV_HPLP'] = {'2016':'0.882/1.12','2017':'0.866/1.136'}    
 vtag_unc['VV_LPLP'] = {'2016':'1.063','2017':'1.043'}

 vtag_pt_dependence = {'VV_HPHP':'((1+0.06*log(MH/2/300))*(1+0.06*log(MH/2/300)))','VV_HPLP':'((1+0.06*log(MH/2/300))*(1+0.07*log(MH/2/300)))'}
 
 DTools = DatacardTools(scales,vtag_pt_dependence,lumi_unc,vtag_unc,1.0,"","")
 
 cat='_'.join(['JJ',sig,purity,'13TeV_'+dataset])
 card=DataCardMaker('',purity,'13TeV_'+dataset,lumi[dataset],'JJ',cat)
 cardName='datacard_'+cat+'.txt'
 workspaceName='workspace_'+cat+'.root'
      
# DTools.AddSignal(card,dataset,purity,sig,'results_2016',0)
 DTools.AddSignal(card,dataset,purity,sig,'results_%s'%options.year,0)
 hname = 'histo'
 if options.sample!='pythia': hname+=('_'+options.sample)
 print "adding shapes bkg"
# card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],options.pdfIn,hname,['PT:CMS_VV_JJ_nonRes_PT_'+category_pdf,'OPT:CMS_VV_JJ_nonRes_OPT_'+category_pdf,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+category_pdf,'altshape:CMS_VV_JJ_nonRes_altshape_'+category_pdf,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+category_pdf],False,0)
# card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],options.pdfIn,hname,['PT:CMS_VV_JJ_nonRes_PT_'+category_pdf,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+category_pdf],False,0)
# card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],options.pdfIn,hname,['OPTXY:CMS_VV_JJ_nonRes_OPTXY_'+category_pdf,'OPTZ:CMS_VV_JJ_nonRes_OPTZ_'+category_pdf,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+category_pdf],False,0) ,    
 card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],options.pdfIn,hname,['PT:CMS_VV_JJ_nonRes_PT_'+category_pdf,'OPTXY:CMS_VV_JJ_nonRes_OPTXY_'+category_pdf,'OPTZ:CMS_VV_JJ_nonRes_OPTZ_'+category_pdf,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+category_pdf],False,0) ,    
 card.addFixedYieldFromFile("nonRes",1,options.input,"nonRes",1)
 DTools.AddData(card,options.input,"nonRes",lumi[dataset] )
 DTools.AddSigSystematics(card,sig,dataset,purity,0)

 print "Adding systematics to card"
 print "norm"
 card.addSystematic("CMS_VV_JJ_nonRes_norm","lnN",{'nonRes':1.5}) 
 print "OPTZ"
 card.addSystematic("CMS_VV_JJ_nonRes_OPTZ_"+category_pdf,"param",[0.0,0.333]) #orig
 #card.addSystematic("CMS_VV_JJ_nonRes_OPTZ_"+category_pdf,"param",[0.0,0.5])
 print "OPTXY"
 card.addSystematic("CMS_VV_JJ_nonRes_OPTXY_"+category_pdf,"param",[0.0,0.333]) #orig
# card.addSystematic("CMS_VV_JJ_nonRes_OPTXY_"+category_pdf,"param",[0.0,0.5])
 print "OPT3"
# card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+category_pdf,"param",[1.0,0.333]) #orig
 card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+category_pdf,"param",[0.0,0.333]) 
 #card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+category_pdf,"param",[10.,20.])
 print "PT"
 card.addSystematic("CMS_VV_JJ_nonRes_PT_"+category_pdf,"param",[0.0,0.333]) #orig
 
 print " and now make card"     
 card.makeCard()

 t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
 print t2wcmd
 os.system(t2wcmd)
 
 return workspaceName
        
if __name__=="__main__":
     
     #if os.path.exists(options.output):
      #answer = raw_input('The output folder '+options.output+'already exsists. Do you want to remove it first? (YES or NO) ')
     # answer = 'YES'
     # if answer=='YES': 
     #  os.system('rm -rf %s'%options.output) 
     #  os.mkdir(options.output)     
              
     finMC = ROOT.TFile(options.input,"READ");
     hinMC = finMC.Get("nonRes");
     if options.input.find("HPHP")!=-1: purity = "VV_HPHP"
     elif options.input.find("HPLP")!=-1: purity = "VV_HPLP"
     else: purity = "VV_LPLP"  
     print "Using purity: " ,purity    

     print " ########################       makeNonResCard      ###"
     w_name = makeNonResCard()
     print " ########################   DONE    makeNonResCard      ###"
     print 
     print "open file " +w_name
     f = ROOT.TFile(w_name,"READ")
     workspace = f.Get("w")
     f.Close()
     workspace.Print()

     MJ1= workspace.var("MJ1");
     MJ2= workspace.var("MJ2");
     MJJ= workspace.var("MJJ");
    
     argset = ROOT.RooArgSet();
     argset.add(MJJ);
     argset.add(MJ2);
     argset.add(MJ1);

     #################################################
     print " ########################       PostFitTools      ###"          
     Tools = PostFitTools(hinMC,argset,options.xrange,options.yrange,options.zrange,purity+'_'+options.sample,options.output)
     xBins,xBinslowedge,xBinsWidth,yBins,yBinslowedge,yBinsWidth,zBins,zBinslowedge,zBinsWidth = Tools.getBins()
     
     print "x bins:"
     print xBins
     print "x bins low edge:"
     print xBinslowedge
     print "x bins width:"
     print xBinsWidth
     
     print
     print "y bins:"
     print yBins
     print "y bins low edge:"
     print yBinslowedge
     print "y bins width:"
     print yBinsWidth
     
     print 
     print "z bins:"
     print zBins
     print "z bins low edge:"
     print zBinslowedge
     print "z bins width:"
     print zBinsWidth

     #################################################
     
     if options.merge:
      print "merging"
      merge_all()
      sys.exit()
                  
     #################################################                
     model = workspace.pdf("model_b") 
     data = workspace.data("data_obs")
     #del workspace
     print "data ",     data.Print()     
          
     print
     print "Observed number of events:",data.sumEntries()
     
     args  = model.getComponents()
     print "model ",model.Print()
     print "args = model comp[onents ",args.Print()
     pdfName = "pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year

     print "Expected number of QCD events:",(args[pdfName].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getVal()
    
     #################################################
     print "###########        Fitting:            ################"
     fitresult = model.fitTo(data,ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1),ROOT.RooFit.NumCPU(8))#,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
     print "#####   Fitting results ###########" 
     fitresult.Print()
     print "###########        Fitting DONE            ################"
     print "model ",model.Print()

     #################################################
     print            
            
     print 
     print "Prefit nonRes pdf:"
     pdf_nonres_shape_prefit = args["nonResNominal_JJ_"+purity+"_13TeV_%s"%options.year]
     pdf_nonres_shape_prefit.Print()
     print
     print "Postfit nonRes pdf:"
     pdf_nonres_shape_postfit  = args["shapeBkg_nonRes_JJ_"+purity+"_13TeV_%s"%options.year]
     pdf_nonres_shape_postfit.Print()
     pdf_nonres_shape_postfit.funcList().Print()
     pdf_nonres_shape_postfit.coefList().Print()
     print
     
     allpdfsz = [] #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsz.append(pdf_nonres_shape_prefit)
     allpdfsz.append(pdf_nonres_shape_postfit)
     for p in options.pdfz.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsz.append(args[p])

     allpdfsx = [] #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsx.append(pdf_nonres_shape_prefit)
     allpdfsx.append(pdf_nonres_shape_postfit)
     for p in options.pdfx.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsx.append(args[p])

     allpdfsy = [] #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsy.append(pdf_nonres_shape_prefit)
     allpdfsy.append(pdf_nonres_shape_postfit)
     for p in options.pdfy.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsy.append(args[p])
      
     print
    
     norm = (args["pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getVal()
     print "norm after fit "+str(norm)
          
     #################################################
     (args[pdfName].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].dump()     
     norm_nonres = [0,0]
     norm_nonres[0] = (args["pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getVal()
     norm_nonres[1] = (args["pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getPropagatedError(fitresult)
     print "QCD normalization after fit",norm_nonres[0],"+/-",norm_nonres[1]
                   
     #################################################     
     #make projections onto MJJ axis
     if options.projection =="z": Tools.doZprojection(allpdfsz,data,norm_nonres[0])
         
     #make projections onto MJ1 axis
     if options.projection =="x":  Tools.doXprojection(allpdfsx,data,norm_nonres[0])
                  
     #make projections onto MJ2 axis
     if options.projection =="y":  Tools.doYprojection(allpdfsy,data,norm_nonres[0])
         
     if options.projection =="xyz":
         Tools.doZprojection(allpdfsz,data,norm_nonres[0])
         Tools.doXprojection(allpdfsx,data,norm_nonres[0])
         Tools.doYprojection(allpdfsy,data,norm_nonres[0])
     
     #################################################   

     save_shape(pdf_nonres_shape_postfit,norm_nonres,options.sample)
