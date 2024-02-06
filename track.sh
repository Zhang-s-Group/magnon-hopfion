#!/bin/sh

datapath=3d-motion

for i in `ls $datapath/*.out -d`; do
	expectation=0.0
	outputfile=`echo $i | awk '{sub(/^.*\//,""); sub(/\.out/,".csv"); printf $0}'`
	echo "Processing "$i"..."
	nr=0
	for j in `ls $i/m*.ovf`; do
		echo $expectation" expected."
		file1=$i/m000000.ovf
		file2=$j
		line=`python track.py $file1 $file2 $expectation | awk '{gsub(/[\(\)\[\]]/,""); sub(/^ +/, ""); sub(/ +$/, ""); print $0}'`
		echo $line | awk '{gsub(/ +/, ", "); print "'$nr', "$0}' >> $datapath/$outputfile
		expectation=`echo $line | awk '{print $4}'`
		nr=`expr $nr + 1`
	done
done
