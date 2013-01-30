#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(description='Count ko annotations.')
parser.add_argument('-i',dest='input_ref',required=True)
parser.add_argument('-o',dest='output_ko',required=True)
parser.add_argument('-k',dest='ko_path',required=True)

args = parser.parse_args()

#count copy numbers of genes in specific bugs
def add_ko( ko, ko_dict ):
        if ko in ko_dict:
                ko_dict[ko] = ko_dict[ko] + 1
        else:
                ko_dict[ko] = 1
	return ko_dict

#generate final normalized gene abundance
def ko_counter( ref_path, ko_path, out_path ):
	#ref_path: path for bugs abundance files
	f1 = open( ref_path, 'r' )
	f2 = open( out_path, 'w' )
	
	f1_l = f1.readlines()
	f1.close()

	#calculate total relative abundance of all bugs in one ref file
	total_abun = 0
	for l1 in f1_l:
		ll1 = l1.strip('\n').split('\t')
		total_abun = total_abun + float(ll1[1])
	
	#ko_dict stores final normalized genes abundance
	ko_dict = {}
	#ko_path is the path of folder for img data
	ko_path = '/' + ko_path.strip('/') + '/'
	for l1 in f1_l:
		#ko_dict_ind stores bug-specified copy number of genes
		ko_dict_ind = {}
		#ko_dict_ind_norm stores normalized bug-specified genes abundance
		ko_dict_ind_norm = {}
		#inner path for bug-specified ko annotation file
		ll1 = l1.strip('\n').split('\t')
		name = 	ll1[0].split('.')[0]
		ko_name = name + '/' + name + '.ko.tab.txt'
		#percentage of each bug
		weight = float(ll1[1])/float(total_abun)
		
		ko_full_path = ko_path + ko_name
		f3 = open( ko_full_path, 'r' )
		f3_l = f3.readlines()
		f3_l = f3_l[1:]
		f3.close()
		
		#not sure whether this counting method is accordant with the requirement
		for l3 in f3_l:
			ll3 = l3.strip().split('\t')
			if ll3[2] != '':
				ko_dict_ind = add_ko( ll3[9], ko_dict_ind )
		
		#generate normalized ko_dict_ind
		for ko, copy in ko_dict_ind.iteritems():
			ko_dict_ind_norm[ko] = copy * weight
		
		#generate abundance file specified ko abundance data
		if ko_dict == {}:
			ko_dict = ko_dict_ind_norm
		else:
			for ko, abun in ko_dict_ind_norm.iteritems():
				if ko in ko_dict:
					ko_dict[ko] = ko_dict[ko] + abun
				else:
					ko_dict[ko] = abun

	#write the gene abundance data into the file
	for ko, abun in ko_dict.iteritems():
		f2.write( ko+'\t'+str(abun)+'\n' )
	f2.close()

ko_counter( args.input_ref, args.ko_path, args.output_ko )
