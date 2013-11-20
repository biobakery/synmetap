#!/usr/bin/python

import argparse
import csv
import sys
import os

#generate final normalized gene abundance
def ko_counter_raw( ref_path, ako_path ):
	#ref_path: path for bugs abundance files
	try:
		fileIn_ref = open( ref_path, 'rU' )
	except IOError:
		sys.stderr.write( "Cannot open input converted abundance file.\n" )
		raise

	#Ko_dict stores final normalized genes abundance
	hashKo = {}
	#ko_path is the path of folder for img annotation data

	for astrLine_ref in csv.reader( fileIn_ref, csv.excel_tab ):
		strBugID =  astrLine_ref[0].split('.')[0]
		strKo_path_in = strBugID + '/' + strBugID + '.ko.tab.txt'

		strKo_full_path = ""
		for ko_path in ako_path:
			strKo_full_path = ko_path + strKo_path_in
			if os.path.isfile( strKo_full_path ):
				break
		if not strKo_full_path:
			sys.stderr.write( "Cannot find input annotation file.\n" )
			raise

		dKo_abun = float( astrLine_ref[1] )

		try:
			fileIn_Ko = open( strKo_full_path, 'rU' )
		except IOError:
			sys.stderr.write( "Cannot open input ko.tab.txt file.\n" )
			raise
				
		iKo_head = 0
		for astrLine_Ko in csv.reader( fileIn_Ko, csv.excel_tab ):
			iKo_head += 1
			if astrLine_Ko and iKo_head > 1:
				strKoID = astrLine_Ko[9].split(":")[1]
				hashKo[strKoID] = hashKo.get( strKoID, 0 ) + dKo_abun
	return hashKo
		
def norm_hash( hashKo, out_path ):
	
	astrKoID = hashKo.keys()
	adKo_abun = hashKo.values()
	
	dTot_abun = sum( adKo_abun )
	adKo_abun_norm = [ dKo_abun/dTot_abun for dKo_abun in adKo_abun ]

	tKo_abun_norm = zip( astrKoID, adKo_abun_norm )

	try:
		fileOut = open( out_path, 'w' )
	except IOError:
		sys.stderr.write( "Cannot access output KO abundance file.\n" )
		raise

	csv_writer_out = csv.writer( fileOut, csv.excel_tab )
	csv_writer_out.writerows( tKo_abun_norm )

def _main():

	parser = argparse.ArgumentParser( description = 'Generate community specified gold standard gene abundance files.' )
	parser.add_argument( "-i", metavar = "input_abun_file", dest = "input_ref", required = True, help = "Input converted abundance file" )
	parser.add_argument( "-o", metavar = "output_abun_file", dest = "output_ko", required = True, help = "Output gene abundance gold standard file" )
	parser.add_argument( "-k", metavar = "input_anno_file", dest = "ko_path", required = True, help = "Path(s) to input gene annotation files. Multiple paths should be delimited by commas without any whitespaces" )
	args = parser.parse_args()

	ako_path = map( lambda x: x + "/" if x[-1] != "/" else x, args.ko_path.split( "," ) )
	hashKo = ko_counter_raw( args.input_ref, ako_path )
	norm_hash( hashKo, args.output_ko )

if __name__ == "__main__":
	_main()
