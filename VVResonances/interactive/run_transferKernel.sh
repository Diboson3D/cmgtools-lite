#!/bin/bash

catIn=$1
catOut=$2
samples=(pythia herwig madgraph)
labels=("" _altshapeUp _altshape2)
period=$3 #Run2
year=$4 #"2016,2017,2018"
#create the directory to store the results
mkdir postfit_qcd

#fit MC in catOut category with templates of catIn category
for i in ${!samples[*]}
do
	python transferKernel.py -i results_${period}/JJ_${period}_nonRes_${catOut}${labels[$i]}.root --sample ${samples[$i]} --year ${year} -p xyz --pdfIn results_${period}/JJ_${period}_nonRes_3D_${catIn}.root --channel ${catOut}
done

#merge post-fit 1Dx2Dx2D templates for catOut category
python transferKernel.py -i results_${period}/JJ_${period}_nonRes_${catOut}.root --year ${year} --pdfIn results_${period}/JJ_${period}_nonRes_3D_${catIn}.root --merge

#make post-fit validation plots for category catOut
for i in ${!samples[*]}
do
        python Projections3DHisto.py --mc results_${period}/JJ_${period}_nonRes_${catOut}${labels[$i]}.root,nonRes -k save_new_shapes_${period}_${samples[$i]}_${catOut}_3D.root,histo -o control-plots-${period}-${catOut}-${samples[$i]} --period "${period}"
        python Projections3DHisto_HPHP.py --mc results_${period}/JJ_${period}_nonRes_${catOut}${labels[$i]}.root,nonRes -k save_new_shapes_${period}_${samples[$i]}_${catOut}_3D.root,histo -o control-plots-coarse-${period}-${catOut}-${samples[$i]} --period "${period}"
done	
