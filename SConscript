#Boyu Ren Jan 1 2013

import sfle
import sys
import os
import glob

Import( "*" )
pE = DefaultEnvironment( )

"""
Header
======

Constant and file definitions.
"""

Reads_No			= "1000000"

c_pathInputGenomeDir		= "/n/CHB/data/synthetic_metagenomes/genomes"

c_fileInputTaxonDir		= "/n/CHB/data/IMG_v350/taxontable.txt"

c_pathKO			= "/n/CHB/data/IMG_v350/img_w_v350"

#need to refine this
c_pathInputAbundRef	= sfle.d( pE, fileDirInput, "abun_ref" )
c_allfiles_InputAbundRef= glob.glob( sfle.d( c_pathInputAbundRef, "*.txt" ))

#Error model
c_pathInputErrModel	= sfle.d( pE, fileDirInput, "error_model" )
c_fileInputErrModel	= File(sfle.d( c_pathInputErrModel, "ill100v5_p.gzip" ))

#src script
c_fileProgConvert	= File(sfle.d( pE, sfle.c_strDirSrc, "convert_ref.py" ))
c_fileProgKO		= File(sfle.d( pE, sfle.c_strDirSrc, "ko_counter.py" ))

#Converted ref files
"""
c_pathConvertedref	= sfle.d( pE, fileDirTmp, "converted" )
c_allfiles_Converted	= [(sfle.d( c_pathConvertedref, os.path.basename(f)) ) for f in c_allfiles_InputAbundRef]
"""

#Generate synthetic sequencing data
c_path_Synseq		= sfle.d( pE, fileDirOutput, "Synseq")
c_allfilespath_Synseq	= [sfle.d( c_path_Synseq, os.path.splitext(os.path.basename(f)) ) for f in c_allfiles_InputAbundRef] 

"""
#Generate ko gold standard files
c_path_KO		= sfle.d( pE, fileDirOutput, "KO")
c_allfiles_KO	= [sfle.d( c_path_KO, os.path.basename(f) ) for f in c_allfiles_InputAbundRef]
"""

"""
Processing module 1
===================

Convert reference abundance file.
"""

def funcConvert(target, source, env):
	strT,astrSs = sfle.ts( target, source )
	strRaw, strTaxa, strProg = astrSs[:3]
	return (sfle.ex(["python", strProg, "-i", strRaw, "-o", strT, "-r", strTaxa]))

for InputRef in pE.Glob( sfle.d( c_pathInputAbundRef, "*.txt"  ) ):
	Converted = sfle.d( pE, fileDirTmp, "converted" , sfle.rebase( InputRef ) )
	Command( Converted, [InputRef, c_fileInputTaxonDir, c_fileProgConvert], funcConvert)
	Default( Converted )

c_path_Convertedref = sfle.d( pE, fileDirTmp, "converted" )

"""
Processing module 2-3
==================

Synthesize sequencing data and generating KO gold standard file
"""

#Used for creating source nodes needed by the GemReads.py script (log file path)
def funcSynLog(target, source, env):
	strT, astrSs = sfle.ts( target, source )
	return (sfle.ex( ["echo >", strT] ) )

for Converted in pE.Glob( sfle.d( c_path_Convertedref, "*.txt" ) ):
	Logpath = sfle.d( pE, fileDirTmp, "SynSeq", "Syn_" + sfle.rebase(Converted, ".txt", ".log" ) )
	Command( Logpath, [], funcSynLog )

#generating Synthetic data
def funcSynthSeq(target, source, env):
	strT, astrSs = sfle.ts( target, source )
	strGenome, strRef, strErrModel, strLog = astrSs[:4]
	return (sfle.ex( ["rby_test1.py -R", strGenome, "-a", strRef, "-n", Reads_No, "-l d -m", strErrModel, "-c -q 33 -o", strT, "-p", "-u d -z", strLog] ) )

for InputRef in Glob( sfle.d( c_path_Convertedref, "*.txt" ) ):
	SynSeq = sfle.d( pE, fileDirOutput, "SynSeq", sfle.rebase( InputRef, ".txt" ) )
	Log = sfle.d( pE, fileDirTmp, "SynSeq", "Syn_" + sfle.rebase( InputRef, ".txt", ".log" ) )
 	Command( SynSeq, [c_pathInputGenomeDir, InputRef, c_fileInputErrModel, Log], funcSynthSeq)
	Default( SynSeq )

#Generating gold standard files for genes
def funcKO(target, source, env):
	strT, astrSs = sfle.ts( target, source )
	strRef, strKO, strProg = astrSs[:3]
	return (sfle.ex( ["python", strProg, "-i", strRef, "-k", strKO, "-o", strT] ))

for InputRef in pE.Glob( sfle.d( c_path_Convertedref, "*.txt" ) ):
	KO = sfle.d( pE, fileDirOutput, "KO", sfle.rebase( InputRef ) )
	Command( KO, [InputRef, c_pathKO, c_fileProgKO], funcKO)
	Default( KO )
