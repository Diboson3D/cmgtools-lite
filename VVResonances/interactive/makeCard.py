from tools.DatacardTools import *
import sys,os
import ROOT
import json
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p","--period",dest="period",default="2016,2017",help="run period")
parser.add_option("--pseudodata",dest="pseudodata",help="make cards with real data or differen pseudodata sets: Vjets, ZprimeZH etc",default='')
parser.add_option("--signal",dest="signal",default="BulkGWW,BulkGZZ,ZprimeWW,ZprimeZH,WprimeWH,WprimeWZ",help="which signal do you want to run? options are BulkGWW, BulkGZZ, WprimeWZ, ZprimeWW, ZprimeZH")
parser.add_option("--outlabel",dest="outlabel",help="lebel for output workspaces for example sigonly_M4500",default='')
parser.add_option("-c","--category",dest="category",default="VV_HPLP,VV_HPHP,VH_HPLP,VH_HPHP,VH_LPHP",help="run period")


(options,args) = parser.parse_args()

cmd='combineCards.py '



#### to create the preparatory WS for pseudodata with Vjets: pseudodata = "" & doVjets=True 
pseudodata = options.pseudodata

outlabel = options.outlabel

datasets= options.period.split(",")


purities= options.category.split(",")

signals = options.signal.split(",")

doVjets= True
sf_qcd=1.
if outlabel.find("sigonly")!=-1 or outlabel.find("qcdonly")!=-1: doVjets = False
if outlabel.find("sigonly")!=-1 or outlabel.find("Vjetsonly")!=-1: sf_qcd = 0.00001

resultsDir = {'2016':'results_2016','2017':'results_2017'}

lumi = {'2016':35900,'2017':41367}
lumi_unc = {'2016':1.025,'2017':1.023}

scales = {"2017" :[0.983,1.08], "2016":[1.014,1.086]}
scalesHiggs = {"2017" :[0.983,1.08], "2016":[1.014,1.086]}



#quick fix to add VH !!!
vtag_unc = {'VV_HPHP':{},'VV_HPLP':{},'VV_LPLP':{},'VH_HPHP':{},'VH_HPLP':{},'VH_LPHP':{},'VH_LPLP':{}}

vtag_unc['VV_HPHP'] = {'2016':'1.232/0.792','2017':'1.269/0.763'}
vtag_unc['VV_HPLP'] = {'2016':'0.882/1.12','2017':'0.866/1.136'}    
vtag_unc['VV_LPLP'] = {'2016':'1.063','2017':'1.043'}
vtag_unc['VH_HPHP'] = {'2016':'1.','2017':'1.'}
vtag_unc['VH_HPLP'] = {'2016':'1.','2017':'1.'}
vtag_unc['VH_LPHP'] = {'2016':'1.','2017':'1.'}

vtag_pt_dependence = {'VV_HPHP':'((1+0.06*log(MH/2/300))*(1+0.06*log(MH/2/300)))','VV_HPLP':'((1+0.06*log(MH/2/300))*(1+0.07*log(MH/2/300)))','VH_HPHP':'1','VH_HPLP':'1','VH_LPHP':'1','VH_LPLP':'1'}
purities= ['VV_HPLP'] #,'VV_HPHP'] #,'VH_HPLP','VH_HPHP','VH_LPHP']
#purities= ['VV_HPLP','VV_HPHP','VH_HPHP','VH_LPHP']
#purities= ['VV_HPLP','VV_HPHP','VH_HPLP','VH_HPHP','VH_LPHP']
#purities= ['VH_HPLP','VH_HPHP','VH_LPHP']
#purities= ['VH_LPHP',"VH_HPHP"]
#signals = ["BulkGWW", "BulkGZZ","ZprimeWW","WprimeWZ","VprimeWV","'ZprimeZH'"]
#signals = ["ZprimeZH"]
signals = ["BulkGWW"]


doCorrelation = False
if sig.find("H") != -1 : doCorrelation = True
Tools = DatacardTools(scales,scalesHiggs,vtag_pt_dependence,lumi_unc,vtag_unc,sf_qcd,pseudodata,outlabel,doCorrelation)

for sig in signals:
  cmd ="combineCards.py"
  for dataset in datasets:
    cmd_combo="combineCards.py"
    for p in purities:

      ncontrib = 0
      
      cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])
      card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat)
      cmd=cmd+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cmd_combo=cmd_combo+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cardName='datacard_'+cat+'.txt '
      workspaceName='workspace_'+cat+outlabel+'.root'

      Tools.AddSignal(card,dataset,p,sig,resultsDir[dataset],ncontrib)
      ncontrib+=1

      if doVjets:
        print "##########################       including W/Z jets in datacard      ######################"
        rootFileMVV = resultsDir[dataset]+'/JJ_%s_WJets_MVV_'%dataset+p+'.root'    
        rootFileNorm = resultsDir[dataset]+'/JJ_%s_WJets_%s.root'%(dataset,p)
        Tools.AddWResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
        ncontrib+=1
        
        rootFileMVV = resultsDir[dataset]+'/JJ_%s_ZJets_MVV_'%dataset+p+'.root'
        rootFileNorm = resultsDir[dataset]+"/JJ_%s_ZJets_%s.root"%(dataset,p)
        Tools.AddZResBackground(card,dataset,p,rootFileMVV,rootFileNorm,resultsDir[dataset],ncontrib)
        ncontrib+=1

      #rootFile3DPDF = resultsDir[dataset]+'/JJ_2016_nonRes_3D_VV_HPLP.root'
      print "##########################       including QCD in datacard      ######################"
      rootFile3DPDF = resultsDir[dataset]+"/save_new_shapes_%s_pythia_"%dataset+p+"_3D.root"
      #rootFile3DPDF = resultsDir[dataset]+"/save_new_shapes_%s_pythia_"%dataset+"VVVH_all"+"_3D.root"
      print "rootFile3DPDF ",rootFile3DPDF
      rootFileNorm = resultsDir[dataset]+"/JJ_%s_nonRes_"%dataset+p+".root"   
      print "rootFileNorm ",rootFileNorm

      Tools.AddNonResBackground(card,dataset,p,rootFile3DPDF,rootFileNorm,ncontrib) 
      print "##########################       QCD added in datacard      ######################"


#      rootFileData = resultsDir[dataset]+"/JJ_%s_nonRes_3D_%s.root"%(dataset,p) #use this only to prepare workspace for making pseudo data with vjets
      rootFileData = resultsDir[dataset]+"/JJ_%s_nonRes_3D_none.root"%(dataset) #use this only to prepare workspace for making pseudo data with vjets
      histName="histo"
      scaleData=lumi[dataset]

      #if you run on real data or pseudodata
#      rootFileData = resultsDir[dataset]+"/JJ_"+p+".root"
#      histName="data"
#      scaleData=1.0 

      if pseudodata=="noVjets":
        print "Using pseudodata without vjets"
        rootFileData = resultsDir[dataset]+"/JJ_PDnoVjets_"+p+".root"
        histName="datah"
        scaleData=1.0
      if pseudodata=="Vjets":
        print "Using pseudodata with vjets"
        rootFileData = resultsDir[dataset]+"/JJ_PDVjets_"+p+".root"
        histName="data"
        scaleData=1.0
      if pseudodata==sig:
       rootFileData = resultsDir[dataset]+"/pseudodata_sigOnly_"+dataset+"_"+sig+"_"+p+"_"+"M"+outlabel.split("_M")[1]+".root"
       histName="data_obs" 
       scaleData=1.0
      Tools.AddData(card,rootFileData,histName,scaleData)

      print "##########################       data/pseudodata added in datacard      ######################"  
       
      Tools.AddSigSystematics(card,sig,dataset,p,1)
      Tools.AddResBackgroundSystematics(card,p)
      Tools.AddNonResBackgroundSystematics(card,p)
      Tools.AddTaggingSystematics(card,sig,dataset,p,resultsDir[dataset]+'/migrationunc.json')
      print "##########################       systematics added in datacard      ######################"  



        
      card.makeCard()
      t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
      print t2wcmd
      os.system(t2wcmd)
    del card

    print "#####################################"

    #make combined 
    if len(purities)>1:
      print "#######     going to combine purity categories: ",purities    
      combo_card = cardName.replace("VV_HPHP","").replace("VV_HPLP","").replace("VV_LPLP","").replace("VH_HPHP","").replace("VH_HPLP","").replace("VH_LPHP","").replace("VH_LPLP","")
      combo_workspace = workspaceName.replace("VV_HPHP","").replace("VV_HPLP","").replace("VV_LPLP","").replace("VH_HPHP","").replace("VH_HPLP","").replace("VH_LPHP","").replace("VH_LPLP","")
      os.system('rm %s'%combo_card)
      cmd_combo+=' >> %s'%combo_card
      print cmd_combo
      os.system(cmd_combo)
      t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
      print t2wcmd
      os.system(t2wcmd)
      print "#####################################"

  if len(datasets)>1:   
    #make combine 2016+2017 card
    print "more than one year, making combined cards"
    combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.txt'
    combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.root'
    os.system('rm %s'%combo_card)
    cmd+=' >> %s'%combo_card
    print cmd
    os.system(cmd)
    t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
    print t2wcmd
    os.system(t2wcmd)


