#!/usr/bin/env python

import argparse
import csv
import pathway
import sys

c_strComment	= "#"

def _ab( hashGenes, astrPathway, fMedup ):

	adAbs = []
	for strGene in astrPathway:
		adAbs.append( hashGenes.get( strGene, 0 ) )
	adAbs.sort( )
	if fMedup:
		adAbs = adAbs[( len( adAbs ) / 2 ):]
	return ( sum( adAbs ) / len( adAbs ) )

def pathcov( aastrGenes, astrPathways, ostm, fStructure, fMedian ):

	hashPathways = {}
	if fStructure:
		for pPathway in pathway.open( astrPathways ):
			hashPathways[pPathway.id( )] = pPathway
	else:
		for astrLine in csv.reader( astrPathways, csv.excel_tab ):
			hashPathways[astrLine[0]] = astrLine[1:]
	
	hashGenes = {}
	for astrLine in aastrGenes:
		if ( len( astrLine ) < 2 ) or \
			astrLine[0].strip( ).startswith( c_strComment ):
			continue
		strGene, strScore = astrLine[:2]
		hashGenes[strGene] = float(strScore)
	if fMedian:
		adScores = sorted( hashGenes.values( ) )
		d50 = adScores[int(round( 0.5 * len( adScores ) ))]
	else:
		d50 = sum( adScores ) / len( adScores )

	csvw = csv.writer( ostm, csv.excel_tab )
	for strPathway, pPathway in hashPathways.items( ):
		if fStructure:
			dCov = pPathway.coverage( hashGenes, d50 )
		else:
			iHits = 0
			for strGene in pPathway:
				dAb = hashGenes.get( strGene, 0 )
				if dAb > d50:
					iHits += 1
			dCov = float(iHits) / len( pPathway )
		if dCov:
			csvw.writerow( (strPathway, dCov) )
			
argp = argparse.ArgumentParser( prog = "pathab.py",
	description = "Given a list of gene family abundances, generate a list of pathway/module coverages." )
argp.add_argument( "-s",		dest = "fStructure",	action = "store_true",
	help = "Treat pathways as boolean structured modules rather than sets" )
argp.add_argument( "-m",		dest = "fMedian",		action = "store_false",
	help = "Use average rather than median for presence/absence calculations" )
argp.add_argument( "istmPaths",	metavar = "pathways.txt",
	type = argparse.FileType( "r" ),
	help = "File from which pathways are read" )
argp.add_argument( "-i",		dest = "istmGenes",		metavar = "genes.txt",
	type = argparse.FileType( "r" ),
	help = "File from which gene family abundances are read" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + ( __doc__ or "" )

def _main( ):
	args = argp.parse_args( )
	pathcov( csv.reader( args.istmGenes or sys.stdin, csv.excel_tab ), args.istmPaths,
		sys.stdout, args.fStructure, args.fMedian )
	
if __name__ == "__main__":
	_main( )
