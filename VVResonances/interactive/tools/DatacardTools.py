#!/usr/bin/env python
import sys, os
import json
import ROOT
  
class DatacardTools():

 def __init__(self,scales,scalesHiggs,tagger_pt_dependence,PU_unc,lumi_unc,sfQCD,pseudodata,outlabel,doCorrelation=True,fitvjetsmjj=False):
  
  self.scales=scales
  self.tagger_pt_dependence=tagger_pt_dependence
  self.PU_unc = PU_unc
  self.lumi_unc = lumi_unc
  self.sfQCD = sfQCD
  self.pseudodata = pseudodata
  self.outlabel = outlabel
  self.scalesHiggs=scalesHiggs
  self.doCorrelation= doCorrelation
  self.fitvjetsmjj = fitvjetsmjj
 

 def AddOneSignal(self,card,dataset,category,sig,resultsDir,ncontrib):

       print "sig ",sig

       if sig=='ZprimeWW':

        card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0})
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1"%sig,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2"%sig,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        card.product3D("%s"%sig,"%s_Wqq1"%sig,"%s_Wqq2"%sig,"%s_MVV"%sig)
        card.addParametricYieldHVTBR("%s"%sig,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX0(pb)","BRWW",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)

       elif sig == 'WprimeWZ':

        card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.doCorrelation)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1_c1"%sig,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2_c1"%sig,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        if self.doCorrelation:
            print "doing correlation"
            card.product("%s_Wqq_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig)
            card.conditionalProduct("%s_c1"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c1"%sig)
        else:
            print "no MVV correlation"
            card.product3D("%s_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig,"%s_MVV"%sig)

        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1_c2"%sig,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2_c2"%sig,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        if self.doCorrelation:
            print "doing correlation"
            card.product("%s_Wqq_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig)
            card.conditionalProduct("%s_c2"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c2"%sig)
        else:
            card.product3D("%s_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig,"%s_MVV"%sig)

        card.sumSimple("%s"%sig,"%s_c1"%sig,"%s_c2"%sig,"0.5")
       
        if self.outlabel.find("sigOnly")==-1:
         card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX+(pb),CX-(pb)","BRWZ",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        else:
           card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX+(pb),CX-(pb)","BRWZ",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],500.0)
                
       elif 'BulkG' in sig or 'Radion' in sig:
       
        card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0})
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1"%sig,"MJ1" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2"%sig,"MJ2" ,resultsDir+"/JJ_%s_%s_MJrandom_"%(sig,dataset)+"NP.json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        card.product3D("%s"%sig,"%s_Wqq1"%sig,"%s_Wqq2"%sig,"%s_MVV"%sig)

        if sig=='BulkGWW': card.addParametricYieldHVTBR("%s"%sig,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/BulkG.json","sigma","BRWW",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='BulkGZZ': card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/BulkG.json","sigma","BRZZ",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='RadionWW': card.addParametricYieldHVTBR("%s"%sig,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/Radion.json","sigma","BRWW",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='RadionZZ': card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/Radion.json","sigma","BRZZ",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='VBF_BulkGWW': card.addParametricYieldHVTBR("%s"%sig,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/VBF_BulkG.json","sigma","BRWW",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='VBF_BulkGZZ': 
           card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/VBF_BulkG.json","sigma","BRZZ",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='VBF_RadionWW': card.addParametricYieldHVTBR("%s"%sig,ncontrib-1,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/VBF_Radion.json","sigma","BRWW",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
        elif sig=='VBF_RadionZZ': card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/VBF_Radion.json","sigma","BRZZ",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],1.0)
       
       elif 'H' in sig:
     
        card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",resultsDir+"/JJ_%s_%s_MVV.json"%(sig,dataset),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.doCorrelation)

        card.addMJJSignalParametricShapeHiggs("%s_Wqq1_c1"%sig,"MJ1" ,resultsDir+"/JJ_Hjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.scalesHiggs)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq2_c1"%sig,"MJ2" ,resultsDir+"/JJ_Vjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        if self.doCorrelation:
         print "doing correlation"
         card.product("%s_Wqq_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig)
         card.conditionalProduct("%s_c1"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c1"%sig)
        else:
         print "no MVV correlation"
         card.product3D("%s_c1"%sig,"%s_Wqq1_c1"%sig,"%s_Wqq2_c1"%sig,"%s_MVV"%sig)

        card.addMJJSignalParametricShapeHiggs("%s_Wqq2_c2"%sig,"MJ2" ,resultsDir+"/JJ_Hjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_j':1},{'CMS_res_j':1.0},self.scalesHiggs)
        card.addMJJSignalParametricShapeNOEXP("%s_Wqq1_c2"%sig,"MJ1" ,resultsDir+"/JJ_Vjet_%s_%s_MJrandom_%s.json"%(sig,dataset,"NP"),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
        if self.doCorrelation:
         print "doing correlation"
         card.product("%s_Wqq_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig)
         card.conditionalProduct("%s_c2"%sig,"%s_MVV"%sig,"MJ1,MJ2","%s_Wqq_c2"%sig)
        else:
         card.product3D("%s_c2"%sig,"%s_Wqq1_c2"%sig,"%s_Wqq2_c2"%sig,"%s_MVV"%sig)
       
        card.sumSimple("%s"%sig,"%s_c1"%sig,"%s_c2"%sig,"0.5")

        if self.outlabel.find("sigOnly")==-1:
           if 'Zprime' in sig: card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX0(pb)","BRZh",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],500.0)
           elif 'Wprime' in sig: card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX+(pb),CX-(pb)","BRWh",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],500.0)
        else:
           if 'Zprime' in sig: card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX0(pb)","BRZh",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],500.0)
           elif 'Wprime' in sig: card.addParametricYieldHVTBR("%s"%sig,ncontrib,resultsDir+"/JJ_%s_%s_"%(sig,dataset)+category+"_yield.json","../scripts/theoryXsec/HVTB.json","CX+(pb),CX-(pb)","BRWh",1000.,'CMS_tagger_PtDependence',self.tagger_pt_dependence["signal"],500.0)

 def AddMultipleSignals(self,card,dataset,category,sig,resultsDir,ncontrib):
 
  if sig == 'VprimeWV':
   self.AddOneSignal(card,dataset,p,'WprimeWZ',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'ZprimeWW',resultsDir[dataset],ncontrib-1)
  elif sig == 'VprimeVH':
   self.AddOneSignal(card,dataset,p,'WprimeWH',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'ZprimeZH',resultsDir[dataset],ncontrib-1)
  elif sig == 'Wprime':
   self.AddOneSignal(card,dataset,p,'WprimeWZ',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'WprimeWH',resultsDir[dataset],ncontrib-1)
  elif sig == 'Zprime':
   self.AddOneSignal(card,dataset,p,'ZprimeWW',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'ZprimeZH',resultsDir[dataset],ncontrib-1)
  elif sig == 'Vprime':
   self.AddOneSignal(card,dataset,p,'WprimeWZ',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'ZprimeWW',resultsDir[dataset],ncontrib-1)
   self.AddOneSignal(card,dataset,p,'WprimeWH',resultsDir[dataset],ncontrib-2)
   self.AddOneSignal(card,dataset,p,'ZprimeZH',resultsDir[dataset],ncontrib-3)
  elif sig == 'BulkGVV':
   self.AddOneSignal(card,dataset,p,'BulkGWW',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'BulkGZZ',resultsDir[dataset],ncontrib-1)
  elif sig == 'RadionVV':
   self.AddOneSignal(card,dataset,p,'RadionWW',resultsDir[dataset],ncontrib)
   self.AddOneSignal(card,dataset,p,'RadionZZ',resultsDir[dataset],ncontrib-1)
          
 #default implementation not working
 def AddTTBackground(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib):
       print "add TT+jets background"  

       card.addMJJTTJetsParametricShape("TTJets_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShape("TTJets_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addHistoShapeFromFile("TTJets_mjj",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_TTJets_PTZ_'+category,'OPT:CMS_VV_JJ_TTJets_OPTZ_'+category],False,0)       
       card.conditionalProduct3('TTJets','TTJets_mjj','TTJets_mjetRes_l1','TTJets_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")
       
       print "outlabel "+self.outlabel
       if self.pseudodata=="" or self.pseudodata=="Vjets":
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets")
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
           print "add small yield"
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets",0.000001)
       else:
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets")
           
 #new implementation: split in 3 contributions W+W, T+T, nonRes+nonRes
 def AddTTBackground2(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib):
       print "add TT+jets background"  
 
       #load mJJ - assume same for the three contributions (preliminary)
       card.addHistoShapeFromFile("TTJets_mjj",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_TTJets_PTZ_'+category,'OPT:CMS_VV_JJ_TTJets_OPTZ_'+category],False,0)       

       # W+W PDF
       card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.conditionalProduct3('TTJetsW','TTJets_mjj','TTJetsW_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")

       #T+T PDF
       card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.conditionalProduct3('TTJetsTop','TTJets_mjj','TTJetsTop_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")

       #nonRes+nonRes PDF
       card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
       card.conditionalProduct3('TTJetsNonRes','TTJets_mjj','TTJetsNonRes_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ',tag1="",tag2="",tag3="")
       
       print "outlabel "+self.outlabel
       if self.pseudodata=="" or self.pseudodata=="Vjets":
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets")
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
           print "add small yield"
           card.addFixedYieldFromFile('TTJets',ncontrib,rootFileNorm,"TTJets",0.000001)
       else:
           card.addFixedYieldFromFile('TTJetsW',ncontrib,rootFileNorm,"TTJets")
           card.addFixedYieldFromFile('TTJetsTop',ncontrib+1,rootFileNorm,"TTJets")
           card.addFixedYieldFromFile('TTJetsNonRes',ncontrib+2,rootFileNorm,"TTJets")
           
           
           
 
 #new implementation: split in 6 contributions W+W, T+T, nonRes+nonRes, nonRes+T, nonres+W, resT+resW with mjj fit
 def AddTTBackground3(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,uncertainty,normjson):
    print "add TT+jets background"  
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
    #uncjsonfile=open(resultsDir+"/JJ_"+dataset+"_TTJets_MjjUnc_"+category+".json")
    uncjsonfile=open(resultsDir+"/JJ_"+dataset+"_TTJets_MjjUnc_NP.json")
    unc = json.load(uncjsonfile)
    allunc = []
    for i in range(0,len(contrib)):
     allunc.append(unc[contrib[i]])
    print " allunc ",allunc
    maxunc = max(allunc)
    print " max unc is ",maxunc

    for i in range(0,len(contrib)):
     if self.pseudodata.find("ttbar")!=-1:

       #load mJJ - assume same for the three contributions (preliminary)
       #jsonfile = resultsDir+"/JJ_"+contrib[i]+dataset+"_TTJets_MVV_"+category+".json"
       jsonfile = resultsDir+"/JJ_"+dataset+"_TTJets"+contrib[i]+"_MVV_NP.json"
       print "load parametrisation for MVV ttbar contributions ",jsonfile,contrib[i]
       #card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,unc[contrib[i]]])
       card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]]),unc[contrib[i]]])

       #print "load ", rootFileMVV[contrib[i]], " for ttbar contribution"
       #f = ROOT.TFile(rootFileMVV[contrib[i]],"READ")
       #card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",["PT:CMS_VV_JJ_TTJets_PTZ_"+category],False,0)       
     else:
      jsonfile = resultsDir+"/JJ_"+dataset+"_TTJets"+contrib[i]+"_MVV_NP.json"
      slopejson= normjson.replace("Norm","NormSlopes")
      print "load parametrisation for MVV ttbar contributions ",jsonfile,contrib[i],slopejson
      #card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,unc[contrib[i]]])
      #card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0].replace("TTJets",mappdf[contrib[i]]),unc[contrib[i]]],slopejson)
      # have only one slope variation for all 6 contributions, the largest
      card.addMVVMinorBkgParametricShape("TTJets"+contrib[i]+"_mjj",["MJJ"],jsonfile,[uncertainty[0],maxunc],slopejson)


    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    '''
    print " testing uncorrelated mjet unc"
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_W_'+category:1.},{'CMS_res_prunedj_W_'+category:1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_W_'+category:1.},{'CMS_res_prunedj_W_'+category:1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_T_'+category:1.},{'CMS_res_prunedj_T_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_T_'+category:1.},{'CMS_res_prunedj_T_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_'+category:1.},{'CMS_res_prunedj_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj_'+category:1.},{'CMS_res_prunedj_'+category:1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    '''
    # built final PDFs:
    # W+W PDF
    card.conditionalProduct3('TTJetsW','TTJetsresW_mjj','TTJetsW_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')

    #T+T PDF
    card.conditionalProduct3('TTJetsTop','TTJetsresT_mjj','TTJetsTop_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')


    #nonRes+nonRes PDF
    card.conditionalProduct3('TTJetsNonRes','TTJetsnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    
    #resT + nonresT
    card.conditionalProduct3('TTJetsTnonresT','TTJetsresTnonresT_mjj','TTJetsTop_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    #nonresT + resT
    card.conditionalProduct3('TTJetsnonresTresT','TTJetsresTnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsTNonResT','TTJetsTnonresT','TTJetsnonresTresT',"CMS_ratio_const")
        
    #resW + nonresT
    card.conditionalProduct3('TTJetsWnonresT','TTJetsresWnonresT_mjj','TTJetsW_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    #nonresT + resW
    card.conditionalProduct3('TTJetsnonresTresW','TTJetsresWnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsWNonResT','TTJetsWnonresT','TTJetsnonresTresW',"CMS_ratio_const")
    
    #resW + resT
    card.conditionalProduct3('TTJetsresWresT','TTJetsresTresW_mjj','TTJetsW_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')
    #resT + resW 
    card.conditionalProduct3('TTJetsresTresW','TTJetsresTresW_mjj','TTJetsTop_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsResWResT','TTJetsresWresT','TTJetsresTresW',"CMS_ratio_const")
    
       
    print "outlabel "+self.outlabel
    if self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
        print "add small yield"
        for i in range(0,len(contrib)):
         card.addFixedYieldFromFile(mappdf[contrib[i]],ncontrib+i,rootFileNorm[contrib[i]],"TTJets"+mappdf[contrib[i]],0.000001)
    elif self.pseudodata.find("ttbar")!=-1:
     for i in range(0,len(contrib)):
      card.addFixedYieldFromFile(mappdf[contrib[i]],ncontrib+i,rootFileNorm[contrib[i]],"TTJets"+contrib[i])
    else:
        norm = open(normjson,"r")
        norms = json.load(norm)
        for i in range(0,len(contrib)):
            card.addYield(mappdf[contrib[i]],ncontrib+i,norms[contrib[i]])

 #new implementation: split in 6 contributions W+W, T+T, nonRes+nonRes, nonRes+T, nonres+W, resT+resW with mjj templates
 def AddTTBackground4(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,normjson):
    print "add TT+jets background"
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}

    #card.addMJJTTJetsParametricCBShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    #card.addMJJTTJetsParametricCBShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResW("TTJetsW_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    #card.addMJJTTJetsParametricCBShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    #card.addMJJTTJetsParametricCBShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeResT("TTJetsTop_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    #card.addMJJTTJetsParametricShapeNonResGaus("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    #card.addMJJTTJetsParametricShapeNonResGaus("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l1","MJ1",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})
    card.addMJJTTJetsParametricShapeNonRes("TTJetsNonRes_mjetRes_l2","MJ2",resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.})#,{'CMS_f_g1':1.},{'CMS_f_res':1.})

    if self.pseudodata.find("ttbar")!=-1:
     for i in range(0,len(contrib)):
      card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",['TOPPT:CMS_VV_JJ_'+mappdf[contrib[i]]+'_TOPPTZ_'+category],False,0)
    else:
     for i in range(0,len(contrib)):
      card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",['TOPPT:CMS_VV_JJ_TTJets_TOPPTZ_'+category],False,0) 
      #if contrib[i] == "nonresT": card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",['TOPPT:CMS_VV_JJ_'+mappdf[contrib[i]]+'_TOPPTZ_'+category],False,0)
      #else : card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",['TOPPT:CMS_VV_JJ_TTJetsPR_TOPPTZ_'+category],False,0)

    '''
    for i in range(0,len(contrib)):
     card.addHistoShapeFromFile("TTJets"+contrib[i]+"_mjj",["MJJ"],rootFileMVV[contrib[i]],"histo_nominal",['TOPPT:CMS_VV_JJ_'+mappdf[contrib[i]]+'_TOPPTZ_'+category],False,0)
    '''
    # built final PDFs:
    # W+W PDF
    print " *** W+W PDF "
    card.conditionalProduct3('TTJetsW','TTJetsresW_mjj','TTJetsW_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')

    #T+T PDF
    print " *** T+T PDF "
    card.conditionalProduct3('TTJetsTop','TTJetsresT_mjj','TTJetsTop_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')

    #nonRes+nonRes PDF
    print " nonRes + nonRes PDF "
    card.conditionalProduct3('TTJetsNonRes','TTJetsnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')

    #resT + nonresT
    card.conditionalProduct3('TTJetsTnonresT','TTJetsresTnonresT_mjj','TTJetsTop_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    #nonresT + resT
    card.conditionalProduct3('TTJetsnonresTresT','TTJetsresTnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsTNonResT','TTJetsTnonresT','TTJetsnonresTresT',"CMS_ratio_const")

    #resW + nonresT
    card.conditionalProduct3('TTJetsWnonresT','TTJetsresWnonresT_mjj','TTJetsW_mjetRes_l1','TTJetsNonRes_mjetRes_l2','MJJ')
    #nonresT + resW
    card.conditionalProduct3('TTJetsnonresTresW','TTJetsresWnonresT_mjj','TTJetsNonRes_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsWNonResT','TTJetsWnonresT','TTJetsnonresTresW',"CMS_ratio_const")

    #resW + resT
    card.conditionalProduct3('TTJetsresWresT','TTJetsresTresW_mjj','TTJetsW_mjetRes_l1','TTJetsTop_mjetRes_l2','MJJ')
    #resT + resW
    card.conditionalProduct3('TTJetsresTresW','TTJetsresTresW_mjj','TTJetsTop_mjetRes_l1','TTJetsW_mjetRes_l2','MJJ')
    card.sumPdf('TTJetsResWResT','TTJetsresWresT','TTJetsresTresW',"CMS_ratio_const")


    print "outlabel "+self.outlabel
    if self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1:
        print "add small yield"
        for i in range(0,len(contrib)):
         card.addFixedYieldFromFile(mappdf[contrib[i]],ncontrib+i,rootFileNorm[contrib[i]],"TTJets"+mappdf[contrib[i]],0.000001)
    elif self.pseudodata.find("ttbar")!=-1: 
     for i in range(0,len(contrib)):
      card.addFixedYieldFromFile(mappdf[contrib[i]],ncontrib+i,rootFileNorm[contrib[i]],"TTJets"+contrib[i])
    else:
        norm = open(normjson,"r")
        norms = json.load(norm)
        for i in range(0,len(contrib)):
            print " contrib "+contrib[i]+" tagger_pt_dependence "+self.tagger_pt_dependence[contrib[i]]
            if self.tagger_pt_dependence[contrib[i]] == "1" :
             print " no pt dep"
             card.addYield(mappdf[contrib[i]],ncontrib+i,norms[contrib[i]])
            else:
             print " pt dep"
             card.addYieldWithUncertainty(mappdf[contrib[i]],ncontrib+i,norms[contrib[i]],"CMS_tagger_PtDependence",self.tagger_pt_dependence[contrib[i]],1.0)
	          
 def AddWResBackground(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,uncertainty=[]):
       print "add Wres background"  
       sys.path.append(resultsDir)
       module_name = 'JJ_%s_WJets_%s'%(dataset,category)
       module = __import__(module_name)  
       print module_name
       # W+jets 
       if self.fitvjetsmjj == True:
        card.addMVVMinorBkgParametricShape("Wjets_mjj",["MJJ"],rootFileMVV,uncertainty)
       else:
        card.addHistoShapeFromFile("Wjets_mjj_c1",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+category,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l1","MJ1","",getattr(module,'Wjets_TTbar_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
       print " addGaussianShape"
       card.addGaussianShape("Wjets_mjetNonRes_l2","MJ2",getattr(module,'Wjets_TTbar_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj")
       else:
        card.product3D("Wjets_c1","Wjets_mjetRes_l1","Wjets_mjetNonRes_l2","Wjets_mjj_c1")

       # jets + W
       if self.fitvjetsmjj == False:
        card.addHistoShapeFromFile("Wjets_mjj_c2",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+category,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l2","MJ2","",getattr(module,'Wjets_TTbar_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
       card.addGaussianShape("Wjets_mjetNonRes_l1","MJ1",getattr(module,'Wjets_TTbar_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj")
       else:
        card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj_c2")
       card.sumPdf('Wjets',"Wjets_c1","Wjets_c2","CMS_ratio_Wjets_"+category)

       print "outlabel "+self.outlabel
       if self.pseudodata=="" or self.pseudodata=="Vjets":
           card.addFixedYieldFromFile('Wjets',ncontrib,rootFileNorm,"WJets")
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1 or self.pseudodata.find("ttbar")!=-1:
           print "add small yield"
           card.addFixedYieldFromFile('Wjets',ncontrib,rootFileNorm,"WJets",0.0000000000001)
       else:
           card.addFixedYieldFromFileWithUncertainty('Wjets',ncontrib,rootFileNorm,"WJets",1.0,"CMS_tagger_PtDependence",self.tagger_pt_dependence["Wjets"],1.0)

 def AddZResBackground(self,card,dataset,category,rootFileMVV,rootFileNorm,resultsDir,ncontrib,uncertainty=[]):
       print "add Zres background"
       sys.path.append(resultsDir)
       module_name = 'JJ_%s_WJets_%s'%(dataset,category)
       module = __import__(module_name)   
            
       # Z+jets 
       if self.fitvjetsmjj == True:
        #card.addMVVMinorBkgParametricShape("Zjets_mjj_c1",["MJJ"],rootFileMVV,uncertainty)
        card.addMVVMinorBkgParametricShape("Zjets_mjj",["MJJ"],rootFileMVV,uncertainty)
       else:
        card.addHistoShapeFromFile("Zjets_mjj_c1",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+category,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l1","MJ1","",getattr(module,'Zjets_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
       card.addGaussianShape("Zjets_mjetNonRes_l2","MJ2",getattr(module,'Zjets_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Zjets_c1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l2","Zjets_mjj")
       else:
        card.product3D("Zjets_c1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l2","Zjets_mjj_c1")
           
       # jets + Z
       if self.fitvjetsmjj == False:
        card.addHistoShapeFromFile("Zjets_mjj_c2",["MJJ"],rootFileMVV,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+category,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+category],False,0)
       card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l2","MJ2","",getattr(module,'Zjets_%s_Res'%category),{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},self.scales)
       card.addGaussianShape("Zjets_mjetNonRes_l1","MJ1",getattr(module,'Zjets_%s_nonRes'%category))
       if self.fitvjetsmjj == True:
        card.product3D("Zjets_c2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l1","Zjets_mjj")
       else:
        card.product3D("Zjets_c2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l1","Zjets_mjj_c2")
       card.sumPdf('Zjets',"Zjets_c1","Zjets_c2","CMS_ratio_Zjets_"+category)

       if self.pseudodata=="" or self.pseudodata=="Vjets":
             card.addFixedYieldFromFile('Zjets',ncontrib,rootFileNorm,"ZJets") 
       elif self.outlabel.find("sigOnly")!=-1 or self.outlabel.find("sigonly")!=-1 or self.pseudodata.find("ttbar")!=-1:
           card.addFixedYieldFromFile('Zjets',ncontrib,rootFileNorm,"ZJets",0.0000000000001)
       else:
           card.addFixedYieldFromFileWithUncertainty('Zjets',ncontrib,rootFileNorm,"ZJets",1.0,"CMS_tagger_PtDependence",self.tagger_pt_dependence["Zjets"],1.0)
       print "stop Zres background"
   
 def AddNonResBackground(self,card,dataset,category,rootFile3DPDF,rootFileNorm,ncontrib):
      
      card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile3DPDF,"histo",['PT:CMS_VV_JJ_nonRes_PT_'+category,'OPT:CMS_VV_JJ_nonRes_OPT_'+category,'TurnOn:CMS_VV_JJ_nonRes_TurnOn_'+category,'altshape:CMS_VV_JJ_nonRes_altshape_'+category,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+category],False,0)
      #card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile3DPDF,"histo",['PT:CMS_VV_JJ_nonRes_PT_'+category,'OPT:CMS_VV_JJ_nonRes_OPT_'+category,'altshape:CMS_VV_JJ_nonRes_altshape_'+category,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+category,'PT6:CMS_VV_JJ_nonRes_PT6_'+category,'OPT6:CMS_VV_JJ_nonRes_OPT6_'+category,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+category,'TurnOn:CMS_VV_JJ_nonRes_TurnOn_'+category,'PT3:CMS_VV_JJ_nonRes_PT3_'+category],False,0) #,'PT4:CMS_VV_JJ_nonRes_PT4_'+category,'OPT4:CMS_VV_JJ_nonRes_OPT4_'+category,'PT5:CMS_VV_JJ_nonRes_PT5_'+category,'OPT5:CMS_VV_JJ_nonRes_OPT5_'+category,'PT6:CMS_VV_JJ_nonRes_PT6_'+category,'OPT6:CMS_VV_JJ_nonRes_OPT6_'+category],False,0)
          
      if self.outlabel.find("sigonly")!=-1 or self.outlabel.find("sigOnly")!=-1 or self.pseudodata.find("ttbar")!=-1:
          card.addFixedYieldFromFile("nonRes",ncontrib,rootFileNorm,"nonRes",0.0000000000001)
      else:
          card.addFixedYieldFromFile("nonRes",ncontrib,rootFileNorm,"nonRes",self.sfQCD)
 
 def AddData(self,card,fileData,histoName,scaleData):

      card.importBinnedData(fileData,histoName,["MJ1","MJ2","MJJ"],'data_obs',scaleData)
 
 #with old implementation 
 def AddTTSystematics(self,card,sig,dataset,category):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJets':1.2})  
    card.addSystematic("CMS_VV_JJ_TTJets_PTZ_"+category,"param",[0,0.1]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJets_OPTZ_"+category,"param",[0,0.1]) #0.333
   
 #with new implementation
 def AddTTSystematics2(self,card,sig,dataset,category,resultsDir):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.2,'TTJetsTop':1.2,'TTJetsNonRes':1.2})  
    card.addSystematic("CMS_VV_JJ_TTJets_PTZ_"+category,"param",[0,0.1]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJets_OPTZ_"+category,"param",[0,0.1]) #0.333

    f=open(resultsDir+"/JJ_%s_TTJets_%s.json"%(dataset,category))
    info=json.load(f)
    card.addSystematic("TTresW_frac","rateParam", "{formula}".format(formula=info['f_g1'].replace('MJJ','@0')),"JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsW",'MJJ')
    card.addSystematic("TTres_frac","rateParam", "{formula}".format(formula=info['f_res'].replace('MJJ','@0')),"JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsW",'MJJ')
    card.addSystematic("TTresT_frac","rateParam", "(@0*(1-@1))","JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsTop",'TTres_frac,TTresW_frac')
    card.addSystematic("TTnonres_frac","rateParam", "(1-@0)","JJ_{category}_13TeV_{year}".format(category=category,year=dataset), "TTJetsNonRes",'TTres_frac')

 #with old implementation 
 def AddTTSystematics3(self,card,sig,dataset,category):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    #   card.addSystematic("CMS_scale_prunedj_top","param",[0.0,0.02])
    #    card.addSystematic("CMS_res_prunedj_top","param",[0.0,0.08])
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
    card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
    card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.2,'TTJetsTop':1.2,'TTJetsNonRes':1.2,'TTJetsWNonResT':1.2,'TTJetsResWResT':1.2,'TTJetsTNonResT':1.2})  
    #card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJets':1.2})  
    card.addSystematic("CMS_VV_JJ_TTJetsTop_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsTop_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsW_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsW_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsNonRes_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsNonRes_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsTnonresT_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsTnonresT_OPTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsWnonresT_PTZ_"+category,"param",[0,0.333]) #0.333
    card.addSystematic("CMS_VV_JJ_TTJetsWnonresT_OPTZ_"+category,"param",[0,0.333]) #0.333
    
 def AddTTSystematics4(self,card,extra_uncertainty,dataset,category):
    card.addSystematic("CMS_f_g1","param",[0.0,0.02])
    card.addSystematic("CMS_f_res","param",[0.0,0.08])
    #card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJets':1.2})
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
    card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
    '''
    print "decorrelateeeeeeeee "
    card.addSystematic("CMS_scale_prunedj_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_res_prunedj_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_scale_prunedj_W_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_res_prunedj_W_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_scale_prunedj_T_"+category,"param",[0.0,0.3])
    card.addSystematic("CMS_res_prunedj_T_"+category,"param",[0.0,0.3])
    '''
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
    #uncjsonfile=open('results_'+dataset+"/JJ_"+dataset+"_TTJets_MjjUnc_"+category+".json")
    uncjsonfile=open('results_'+dataset+"/JJ_"+dataset+"_TTJets_MjjUnc_NP.json")
    unc = json.load(uncjsonfile)
    allunc = []
    for i in range(0,len(contrib)):
       allunc.append(unc[contrib[i]])

    #card.addSystematic("CMS_scale_prunedj_top","param",[0.0,0.02])
    #card.addSystematic("CMS_res_prunedj_top","param",[0.0,0.08])
    if self.pseudodata.find("ttbar")==-1:
        #card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.2,'TTJetsTop':1.2,'TTJetsNonRes':1.2,'TTJetsWNonResT':1.2,'TTJetsResWResT':1.2,'TTJetsTNonResT':1.2}) 
        card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{'TTJetsW':1.05,'TTJetsTop':1.05,'TTJetsNonRes':1.05,'TTJetsWNonResT':1.05,'TTJetsResWResT':1.05,'TTJetsTNonResT':1.05})
        #card.addSystematic(extra_uncertainty[0],"param",[0.0,extra_uncertainty[1]])
        #card.addSystematic(extra_uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,"param",[0.0,float("{:.3f}".format(unc[contrib[i]]))])
        card.addSystematic(extra_uncertainty[0],"param",[0.0,float("{:.3f}".format(max(allunc)))])
    else:
        for i in range(0,len(contrib)):
         #card.addSystematic(extra_uncertainty[0].replace("TTJets",mappdf[contrib[i]])+"_"+category,"param",[0.0,float("{:.3f}".format(unc[contrib[i]]))])
         card.addSystematic("CMS_VV_JJ_"+mappdf[contrib[i]]+"_norm","lnN",{mappdf[contrib[i]]:3.2})
         card.addSystematic(extra_uncertainty[0].replace("TTJets",mappdf[contrib[i]]),"param",[0.0,float("{:.3f}".format(unc[contrib[i]]))])
    
 def AddTTSystematics5(self,card,category,vbf):
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    #contribPR =["resT","resW","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}

    if category.find("VBF") != -1 and not vbf: category = category.replace("VBF_","")

    if self.pseudodata.find("ttbar")==-1:
        card.addSystematic("CMS_VV_JJ_TTJets_norm","lnN",{mappdf[ttcon]:1.06 for ttcon in contrib})
        card.addSystematic("CMS_VV_JJ_TTJets_TOPPTZ_"+category,"param",[0,1.])
        # try to separate non res from partially res
        #card.addSystematic("CMS_VV_JJ_TTJetsNonRes_TOPPTZ_"+category,"param",[0,1.])
        #card.addSystematic("CMS_VV_JJ_TTJetsPR_TOPPTZ_"+category,"param",[0,1.])
        #card.addSystematic("CMS_VV_JJ_TTJetsNonRes_norm_"+category,"lnN",{"TTJetsNonRes":1.06})
        #card.addSystematic("CMS_VV_JJ_TTJetsPR_norm","lnN",{mappdf[ttcon]:1.06 for ttcon in contribPR}) 
    else:
        for i in range(0,len(contrib)):
         card.addSystematic("CMS_VV_JJ_"+mappdf[contrib[i]]+"_norm","lnN",{mappdf[contrib[i]]:3.2})
         card.addSystematic("CMS_VV_JJ_"+mappdf[contrib[i]]+"_TOPPTZ_"+category,"param",[0,1.])

       
 def AddSigSystematics(self,card,sig,dataset,category,correlate):
      print " signal ",sig
      card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
      card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
      card.addSystematic("CMS_scale_j","param",[0.0,0.012])
      card.addSystematic("CMS_res_j","param",[0.0,0.08])
      card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})
      production = "ggDY"
      signaltype = "signal"
      if category.find("VBF") !=-1:
       production = "VBF"
      if sig.find("VBF") !=-1:
       signaltype = "signalVBF"
      print " production mode ",production
      print "adding PU systematics"
      card.addSystematic("CMS_PU","lnN",{'%s'%sig:self.PU_unc[production][signaltype],"Wjets":self.PU_unc[production]["PRbackground"],"Zjets":self.PU_unc[production]["PRbackground"],'TTJetsW':self.PU_unc[production]["PRbackground"],'TTJetsTop':self.PU_unc[production]["PRbackground"],'TTJetsNonRes':self.PU_unc[production]["PRbackground"],'TTJetsWNonResT':self.PU_unc[production]["PRbackground"],'TTJetsResWResT':self.PU_unc[production]["PRbackground"],'TTJetsTNonResT':self.PU_unc[production]["PRbackground"]})
      prefiringperiods = ["2016","2017"]
      for year in prefiringperiods:
       card.addSystematic("CMS_L1prefiring"+year+"_"+production,"lnN",{'%s'%sig:1.01,"Wjets":1.01,"Zjets":1.01,'TTJetsW':1.01,'TTJetsTop':1.01,'TTJetsNonRes':1.01,'TTJetsWNonResT':1.01,'TTJetsResWResT':1.01,'TTJetsTNonResT':1.01})

      if correlate:
       card.addSystematic("CMS_lumi","lnN",{'%s'%sig:self.lumi_unc[dataset],"Wjets":self.lumi_unc[dataset],"Zjets":self.lumi_unc[dataset],
                                            'TTJetsW':self.lumi_unc[dataset],'TTJetsTop':self.lumi_unc[dataset],'TTJetsNonRes':self.lumi_unc[dataset],'TTJetsWNonResT':self.lumi_unc[dataset],'TTJetsResWResT':self.lumi_unc[dataset],'TTJetsTNonResT':self.lumi_unc[dataset]})   
      else: 
       card.addSystematic("CMS_lumi","lnN",{'%s'%sig:self.lumi_unc[dataset]})
      
    
 def AddTaggingSystematics(self,card,signal,p,jsonfile): 
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}
    uncup_t = {}
    uncdown_t = {}
    with open(jsonfile[0]) as json_file_sig:
     data_sig = json.load(json_file_sig)
    with open(jsonfile[1]) as json_file_w:
     data_w = json.load(json_file_w)
    with open(jsonfile[2]) as json_file_z:
     data_z = json.load(json_file_z)
    with open(jsonfile[3]) as json_file_t:
     data_t = json.load(json_file_t)
    sig = signal
    if signal.find('Zprime')!=-1 and signal.find("ZH")!=-1: sig = "ZprimeToZh"
    if signal.find('Zprime')!=-1 and signal.find("WW")!=-1: sig = "ZprimeToWW"
    if signal.find('Wprime')!=-1 and signal.find("WH")!=-1: sig = "WprimeToWh"
    if signal.find('Wprime')!=-1 and signal.find("WZ")!=-1: sig = "WprimeToWZ"
    if signal.find('BulkGWW')!=-1 : sig = "BulkGravToWW"
    if signal.find('BulkGZZ')!=-1 : sig = "BulkGravToZZ"
    if signal.find('VBF')!=-1 : sig = "VBF_"+sig

    uncup_s   = data_sig[signal+"_CMS_VV_JJ_DeepJet_Htag_eff"][p+"_up"]
    uncdown_s = data_sig[signal+"_CMS_VV_JJ_DeepJet_Htag_eff"][p+"_down"]
    uncup_w   = data_w["WJets_CMS_VV_JJ_DeepJet_Htag_eff"]["WJets."+p+"_up"]
    uncdown_w = data_w["WJets_CMS_VV_JJ_DeepJet_Htag_eff"]["WJets."+p+"_down"]
    uncup_z   = data_z["ZJets_CMS_VV_JJ_DeepJet_Htag_eff"]["ZJets."+p+"_up"]
    uncdown_z = data_z["ZJets_CMS_VV_JJ_DeepJet_Htag_eff"]["ZJets."+p+"_down"]
    for c in contrib:
     uncup_t.update( {mappdf[c] :data_t["TTJets_CMS_VV_JJ_DeepJet_Htag_eff"][mappdf[c]+"."+p+"_up"] })
     uncdown_t.update({mappdf[c] : data_t["TTJets_CMS_VV_JJ_DeepJet_Htag_eff"][mappdf[c]+"."+p+"_down"]})
    unc = {'%s'%signal: str(uncdown_s)+"/"+ str(uncup_s) ,'Wjets': str(uncdown_w)+"/"+ str(uncup_w),'Zjets': str(uncdown_z)+"/"+ str(uncup_z),"TTJetsW":str(uncdown_t["TTJetsW"])+"/"+ str(uncup_t["TTJetsW"]),"TTJetsWNonResT":str(uncdown_t["TTJetsWNonResT"])+"/"+ str(uncup_t["TTJetsWNonResT"]),"TTJetsResWResT": str(uncdown_t["TTJetsResWResT"])+"/"+ str(uncup_t["TTJetsResWResT"])}
    if p.find('VV_HPHP') !=-1 or p.find('VH_HPLP') !=-1 or p.find('VV_HPLP') !=-1:
     if p.find('VV_HPHP') !=-1: ap = 'VH_HPHP'
     if p.find('VH_HPLP') !=-1: ap = 'VH_LPHP'
     if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
     if p.find('VBF') !=-1 : ap = 'VBF_'+ap
     uncup_s   = data_sig[signal+"_CMS_VV_JJ_DeepJet_Htag_eff"][ap+"_up"]
     uncdown_s = data_sig[signal+"_CMS_VV_JJ_DeepJet_Htag_eff"][ap+"_down"]
     uncup_w   = data_w["WJets_CMS_VV_JJ_DeepJet_Htag_eff"]["WJets."+ap+"_up"]
     uncdown_w = data_w["WJets_CMS_VV_JJ_DeepJet_Htag_eff"]["WJets."+ap+"_down"]
     uncup_z   = data_z["ZJets_CMS_VV_JJ_DeepJet_Htag_eff"]["ZJets."+ap+"_up"]
     uncdown_z = data_z["ZJets_CMS_VV_JJ_DeepJet_Htag_eff"]["ZJets."+ap+"_down"]
     for c in contrib:
      uncup_t.update( {mappdf[c] :data_t["TTJets_CMS_VV_JJ_DeepJet_Htag_eff"][mappdf[c]+"."+ap+"_up"] })
      uncdown_t.update({mappdf[c] : data_t["TTJets_CMS_VV_JJ_DeepJet_Htag_eff"][mappdf[c]+"."+ap+"_down"]})
     unc = {'%s'%signal: str(uncup_s)+"/"+ str(uncdown_s) ,'Wjets': str(uncup_w)+"/"+ str(uncdown_w),'Zjets': str(uncup_z)+"/"+ str(uncdown_z),"TTJetsW":str(uncup_t["TTJetsW"])+"/"+ str(uncdown_t["TTJetsW"]),"TTJetsWNonResT":str(uncup_t["TTJetsWNonResT"])+"/"+ str(uncdown_t["TTJetsWNonResT"]),"TTJetsResWResT": str(uncup_t["TTJetsResWResT"])+"/"+ str(uncdown_t["TTJetsResWResT"])}
    print unc
    card.addSystematic("CMS_VV_JJ_DeepJet_Htag_eff","lnN",unc)
    
    uncup_s   = data_sig[signal+"_CMS_VV_JJ_DeepJet_Vtag_eff"][p+"_up"]
    uncdown_s = data_sig[signal+"_CMS_VV_JJ_DeepJet_Vtag_eff"][p+"_down"]
    uncup_w   = data_w["WJets_CMS_VV_JJ_DeepJet_Vtag_eff"]["WJets."+p+"_up"]
    uncdown_w = data_w["WJets_CMS_VV_JJ_DeepJet_Vtag_eff"]["WJets."+p+"_down"]
    uncup_z   = data_z["ZJets_CMS_VV_JJ_DeepJet_Vtag_eff"]["ZJets."+p+"_up"]
    uncdown_z = data_z["ZJets_CMS_VV_JJ_DeepJet_Vtag_eff"]["ZJets."+p+"_down"]
    for c in contrib:     
     uncup_t.update( {mappdf[c] :data_t["TTJets_CMS_VV_JJ_DeepJet_Vtag_eff"][mappdf[c]+"."+p+"_up"]} )
     uncdown_t.update({mappdf[c] : data_t["TTJets_CMS_VV_JJ_DeepJet_Vtag_eff"][mappdf[c]+"."+p+"_down"]})
    unc = {'%s'%signal: str(uncdown_s)+"/"+ str(uncup_s) ,'Wjets': str(uncdown_w)+"/"+ str(uncup_w),'Zjets': str(uncdown_z)+"/"+ str(uncup_z),"TTJetsW":str(uncdown_t["TTJetsW"])+"/"+ str(uncup_t["TTJetsW"]),"TTJetsWNonResT":str(uncdown_t["TTJetsWNonResT"])+"/"+ str(uncup_t["TTJetsWNonResT"]),"TTJetsResWResT": str(uncdown_t["TTJetsResWResT"])+"/"+ str(uncup_t["TTJetsResWResT"])}
    if p.find('VH_LPHP')  !=-1 or p.find('VV_HPLP') !=-1 :
     if p.find('VH_LPHP') !=-1: ap = 'VV_HPHP'
     if p.find('VV_HPLP') !=-1: ap = 'VH_HPLP'
     if p.find('VBF') !=-1 : ap = 'VBF_'+ap
     uncup_s   = data_sig[signal+"_CMS_VV_JJ_DeepJet_Vtag_eff"][ap+"_up"]
     uncdown_s = data_sig[signal+"_CMS_VV_JJ_DeepJet_Vtag_eff"][ap+"_down"]
     uncup_w   = data_w["WJets_CMS_VV_JJ_DeepJet_Vtag_eff"]['WJets.'+ap+"_up"]
     uncdown_w = data_w["WJets_CMS_VV_JJ_DeepJet_Vtag_eff"]['WJets.'+ap+"_down"]
     uncup_z   = data_z["ZJets_CMS_VV_JJ_DeepJet_Vtag_eff"]['ZJets.'+ap+"_up"]
     uncdown_z = data_z["ZJets_CMS_VV_JJ_DeepJet_Vtag_eff"]['ZJets.'+ap+"_down"]
     for c in contrib:     
      uncup_t.update( {mappdf[c] :data_t["TTJets_CMS_VV_JJ_DeepJet_Vtag_eff"][mappdf[c]+"."+ap+"_up"]} )
      uncdown_t.update({mappdf[c] : data_t["TTJets_CMS_VV_JJ_DeepJet_Vtag_eff"][mappdf[c]+"."+ap+"_down"]})
     unc = {'%s'%signal: str(uncup_s)+"/"+ str(uncdown_s) ,'Wjets': str(uncup_w)+"/"+ str(uncdown_w),'Zjets': str(uncup_z)+"/"+ str(uncdown_z),"TTJetsW":str(uncup_t["TTJetsW"])+"/"+ str(uncdown_t["TTJetsW"]),"TTJetsWNonResT":str(uncup_t["TTJetsWNonResT"])+"/"+ str(uncdown_t["TTJetsWNonResT"]),"TTJetsResWResT": str(uncup_t["TTJetsResWResT"])+"/"+ str(uncdown_t["TTJetsResWResT"])}
    card.addSystematic("CMS_VV_JJ_DeepJet_Vtag_eff","lnN",unc)
    
    uncup_s   = data_sig[signal+"_CMS_VV_JJ_DeepJet_TOPtag_mistag"][p+"_up"]
    uncdown_s = data_sig[signal+"_CMS_VV_JJ_DeepJet_TOPtag_mistag"][p+"_down"]
    uncup_w   = data_w["WJets_CMS_VV_JJ_DeepJet_TOPtag_mistag"]["WJets."+p+"_up"]
    uncdown_w = data_w["WJets_CMS_VV_JJ_DeepJet_TOPtag_mistag"]["WJets."+p+"_down"]
    uncup_z   = data_z["ZJets_CMS_VV_JJ_DeepJet_TOPtag_mistag"]["ZJets."+p+"_up"]
    uncdown_z = data_z["ZJets_CMS_VV_JJ_DeepJet_TOPtag_mistag"]["ZJets."+p+"_down"]
    for c in contrib:
     uncup_t.update( {mappdf[c] :data_t["TTJets_CMS_VV_JJ_DeepJet_TOPtag_mistag"][mappdf[c]+"."+p+"_up"]} )
     uncdown_t.update({mappdf[c] : data_t["TTJets_CMS_VV_JJ_DeepJet_TOPtag_mistag"][mappdf[c]+"."+p+"_down"]})
    unc = {"TTJetsTop" : str(uncdown_t["TTJetsTop"])+"/"+ str(uncup_t["TTJetsTop"]), "TTJetsTNonResT":str(uncdown_t["TTJetsTNonResT"])+"/"+ str(uncup_t["TTJetsTNonResT"]),"TTJetsResWResT":str(uncdown_t["TTJetsResWResT"])+"/"+ str(uncup_t["TTJetsResWResT"]) }
    card.addSystematic("CMS_VV_JJ_DeepJet_TOPtag_mistag","lnN",unc)
     
 def AddResBackgroundSystematics(self,card,category,vbf,extra_uncertainty=[]):
 
       card.addSystematic("CMS_VV_JJ_Wjets_norm","lnN",{'Wjets':1.10})
       card.addSystematic("CMS_VV_JJ_Zjets_norm","lnN",{'Zjets':1.10})
       if category.find("VBF") != -1 and not vbf: category = category.replace("VBF_","")
       if self.fitvjetsmjj == True:
        card.addSystematic(extra_uncertainty[0],"param",[0.0,extra_uncertainty[1]])
        card.addSystematic(extra_uncertainty[2],"param",[0.0,extra_uncertainty[3]])
       else:
        card.addSystematic("CMS_VV_JJ_Wjets_PTZ_"+category,"param",[0,0.1]) #0.333
        card.addSystematic("CMS_VV_JJ_Wjets_OPTZ_"+category,"param",[0,0.1]) #0.333
        card.addSystematic("CMS_VV_JJ_Zjets_PTZ_"+category,"param",[0,0.1]) #0.333
        card.addSystematic("CMS_VV_JJ_Zjets_OPTZ_"+category,"param",[0,0.1]) #0.333


 def AddNonResBackgroundSystematics(self,card,category,vbf):
      print " nonres syst for ",category
      card.addSystematic("CMS_VV_JJ_nonRes_norm_"+category,"lnN",{'nonRes':1.5})
      if category.find("VBF") != -1 and not vbf: category = category.replace("VBF_","")
      print " now ",category
      card.addSystematic("CMS_VV_JJ_nonRes_PT_"+category,"param",[0.0,2.])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_OPT6_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_PT6_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_OPT5_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_PT5_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_OPT4_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_PT4_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_OPT2_"+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_PT2_"+category,"param",[0.0,2.])
      card.addSystematic("CMS_VV_JJ_nonRes_TurnOn_"+category,"param",[1.,2.])
      card.addSystematic('CMS_VV_JJ_nonRes_altshape2_'+category,"param",[0.0,2.])
      card.addSystematic('CMS_VV_JJ_nonRes_altshape_'+category,"param",[0.0,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+category,"param",[1.,2.])
      #card.addSystematic("CMS_VV_JJ_nonRes_PT3_"+category,"param",[1.,2.])
