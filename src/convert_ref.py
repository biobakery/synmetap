#!/usr/bin/python

import argparse
import os
import sys


def search_name ( ref_path, taxon_path, out_path ):
	
	if ref_path[0].isalpha() == True:
		ref_path = "./" + ref_path
	if taxon_path[0].isalpha() == True:
		taxon_path = "./" + taxon_path
	if out_path[0].isalpha() == True:
		out_path = "./" + out_path
	
	f1 = open ( ref_path , 'r' )
	f2 = open ( taxon_path , 'r' )
	
	file_name = os.path.basename( out_path )
	path_name = os.path.dirname( out_path )
	if not os.path.exists(path_name):
		os.makedirs(path_name)
	f3 = open ( out_path, 'w' )

	f1_l = f1.readlines()
	f2_l = f2.readlines()
	
	f1.close()
	f2.close()
	
	for l1 in f1_l:
		ll1 = l1.strip('\n').split('\t')
		name = ll1[0]
		abun = ll1[1]
		conv_name_fin = ''
		conv_name_draft = ''

		for l2 in f2_l:
			ll2 = l2.strip('\n').split('\t')
			n = len( name )
			if len( ll2[3] ) >= n:
				if name.lower() == ll2[3].lower()[:n] and ll2[2].lower() == 'finished': 
					conv_name_fin = ll2[0]
					f3.write( ll2[0]+'.fna'+'\t'+abun+'\n' )
					break
				if name.lower() == ll2[3].lower()[:n] and ll2[2].lower() == 'draft':
					if conv_name_draft == '':
						conv_name_draft = ll2[0]
					else:
						continue
			else:
				continue
		#if no taxon found in IMG data set, write an empty converted file.
		if conv_name_fin == '' and conv_name_draft == '':
			print "Taxon " + name + " does not exist!\n"
			f3.close()
			os.remove(out_path)
			f3 = open(out_path, 'w')
			f3.close()
			sys.exit()
		elif conv_name_fin == '':
			f3.write( conv_name_draft+'.fna'+'\t'+abun+'\n' )
	f3.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert abun files.')
	parser.add_argument('-i',dest='input_ref',required=True)
	parser.add_argument('-o',dest='output_ref',required=True)
	parser.add_argument('-r',dest='ref_taxa',required=True)

	args = parser.parse_args()

	search_name( args.input_ref, args.ref_taxa, args.output_ref )
