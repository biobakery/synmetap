#!/usr/bin/env python

import argparse
import csv
import pathway
import sys

c_strComment	= "#"
c_strUnknown	= "unknown"

def _ab( hashGenes, astrPathway, fMedup ):

	adAbs = []
	for strGene in astrPathway:
		adAbs.append( hashGenes.get( strGene, 0 ) )
	adAbs.sort( )
	if fMedup:
		adAbs = adAbs[( len( adAbs ) / 2 ):]
	return ( sum( adAbs ) / len( adAbs ) )

def pathab( aastrGenes, astrPathways, ostm, fStructure, fCoverage, fMedup, strMetadatum ):

	hashPathways = {}
	if fStructure:
		for pPathway in pathway.open( astrPathways ):
			hashPathways[pPathway.id( )] = pPathway
	else:
		for astrLine in csv.reader( astrPathways, csv.excel_tab ):
			hashPathways[astrLine[0]] = astrLine[1:]
	
	aadData = []
	astrGenes = []
	aastrMetadata = []
	fData = ( not strMetadatum )
	for astrLine in aastrGenes:
		if ( len( astrLine ) < 2 ) or \
			astrLine[0].strip( ).startswith( c_strComment ):
			continue
		if fData:
			strGene, astrScores = astrLine[0], astrLine[1:]
			astrGenes.append( strGene )
			aadData.append( [( float(s) if s.strip( ) else 0 ) for s in astrScores] )
		else:
			aastrMetadata.append( astrLine )
			if astrLine[0] == strMetadatum:
				fData = True
	adScores = sorted( [d for a in aadData for d in a] )
	if len( adScores ) > 2:
		d25, d50, d75 = (adScores[int(round( 0.25 * ( i + 1 ) * len( adScores ) ))] for i in range( 3 ))
	else:
		d25, d50, d75 = [adScores[0] if adScores else 0] * 3

	aadPathways = [[] for i in xrange( len( hashPathways ) + 1 )]	
	for iSample in xrange( len( aadData[0] ) ):
		hashGenes = {}
		for i, a in enumerate( aadData ):
			hashGenes[astrGenes[i]] = a[iSample]
		setstrUsed = set()
		for iPathway, (strPathway, pPathway) in enumerate( hashPathways.items( ) ):
			if fStructure:
				setstrUsed.update( pPathway.genes( ) )
				dAb = pPathway.abundance( hashGenes, d50 if fCoverage else None )
			else:
				setstrUsed.update( pPathway )
				dAb = _ab( hashGenes, pPathway, fMedup )
			aadPathways[iPathway].append( dAb )
		setstrUnused = set(hashGenes.keys( )) - setstrUsed
		aadPathways[-1].append( _ab( hashGenes, setstrUnused, fMedup ) )

	csvw = csv.writer( ostm, csv.excel_tab )
	for astrMetadatum in aastrMetadata:
		csvw.writerow( astrMetadatum )
	for strPathway, adPathway in zip( hashPathways.keys( ), aadPathways ):
		if max( adPathway ):
			csvw.writerow( [strPathway] + adPathway )
	if max( aadPathways[-1] ):
		csvw.writerow( [c_strUnknown] + aadPathways[-1] )
			
argp = argparse.ArgumentParser( prog = "pathab.py",
	description = "Given a list of gene family abundances, generate a list of pathway/module abundances." )
argp.add_argument( "-s",		dest = "fStructure",	action = "store_true",
	help = "Treat pathways as boolean structured modules rather than sets" )
argp.add_argument( "-c",		dest = "fCoverage",		action = "store_false",
	help = "Also output calculations for non-covered (absent) pathways" )
argp.add_argument( "-d",		dest = "fMedup",		action = "store_false",
	help = "Use all genes rather than upper 50%% for abundance calculation" )
argp.add_argument( "-m",		dest = "strMetadatum",	metavar = "metadatum",
	type = str,
	help = "If given, row ID of final metadata row preceding data" )
argp.add_argument( "istmPaths",	metavar = "pathways.txt",
	type = argparse.FileType( "r" ),
	help = "File from which pathways are read" )
argp.add_argument( "-i",		dest = "istmGenes",		metavar = "genes.txt",
	type = argparse.FileType( "r" ),
	help = "File from which gene family abundances are read" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + ( __doc__ or "" )

def _main( ):
	args = argp.parse_args( )
	pathab( csv.reader( args.istmGenes or sys.stdin, csv.excel_tab ), args.istmPaths,
		sys.stdout, args.fStructure, args.fCoverage, args.fMedup, args.strMetadatum )
	
if __name__ == "__main__":
	_main( )
