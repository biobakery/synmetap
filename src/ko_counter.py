#!/usr/bin/python

import argparse
import csv

parser = argparse.ArgumentParser(description='Count ko annotations.')
parser.add_argument('-i',dest='input_ref',required=True)
parser.add_argument('-o',dest='output_ko',required=True)
parser.add_argument('-k',dest='ko_path',required=True)

args = parser.parse_args()

#count copy numbers of genes in specific bugs
def add_ko( strKo, hashKo ):
	hashKo[strKo] = 1 + hashKo.get( strKo, 0 )
	return hashKo

#generate final normalized gene abundance
def ko_counter( ref_path, ko_path, out_path ):
	#ref_path: path for bugs abundance files
	try:
		fileIn_ref = open( ref_path, 'r' )
	except IOError:
		print "Cannot open input converted abundance file."
	try:
		fileOut_Ko = open( out_path, 'w' )
	except IOError:
		print "Cannot access output KO abundance file."

	csv_reader_ref = csv.reader( fileIn_ref, csv.excel_tab )	

	#Ko_dict stores final normalized genes abundance
	Ko_dict = {}
	#dKo_dict is used to normalize final result
	dKo_overall = 0
	#ko_path is the path of folder for img data
	if ko_path[-1] != '/':
		ko_path = ko_path + '/'

	for astrLine_ref in csv_reader_ref:
		#ko_dict_ind stores bug-specified copy number of genes
		hashKo_ind = {}
		#ko_dict_ind_norm stores normalized bug-specified genes abundance
		hashKo_ind_norm = {}
		strBugID =  astrLine_ref[0].split('.')[0]
		strKo_path_in = strBugID + '/' + strBugID + '.ko.tab.txt'
		
		strKo_full_path = strKo_path_out + strKo_path_in
		try:
			fileIn_Ko = open( strKo_full_path, 'r' )
		except IOError:
			print "Cannot open input ko.tab.txt file."
		csv_reader_Ko = csv.reader( fileIn_Ko, csv.excel_tab )		
	
		for astrLine_Ko in csv_reader_Ko:
			if astrLine_Ko:
				#some of ko do not have id value in the ko.tab.
				#txt file. Whether to ignore them?
				if astrLine_Ko[2] != '':
					hashKo_ind = add_ko( astrLine_Ko[9].split(":")[1], hashKo_ind )
		
		#generate normalized ko_dict_ind
		for strko, copy in hashKo_ind.iteritems():
			hashKo_ind_norm[ko] = copy * astrLine_ref[1]
			dKo_overall += hashKo_ind_norm[ko]
		
		#generate abundance file specified ko abundance data
		if hashKo == {}:
			hashKo = hashKo_ind_norm
		else:
			for ko, abun in hashKo_ind_norm.iteritems():
				hashKo[ko] = hashKo.get( ko, 0 ) + abun

	#normalize the final result so they add up to 1.
	for ko in hashKo.keys():
		hashKo[ko] = hashKo[ko]/dKo_overall
	
	#write the gene abundance data into the file
	csv_writer_out = csv.writer( fileOutKo, csv.excel_tab )
	for ko, abun in hashKo.iteritems():
		csv_writer_out.writerow( [ko, abun] )
	

ko_counter( args.input_ref, args.ko_path, args.output_ko )
