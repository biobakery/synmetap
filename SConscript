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

Reads_No			= "100"

c_pathInputGenomeDir		= "/n/CHB/data/synthetic_metagenomes/genomes"

c_fileInputTaxonDir		= "/n/CHB/data/IMG_v350/taxontable.txt"

c_pathKO			= "/n/CHB/data/IMG_v350/img_w_v350"

#need to refine this
c_pathInputAbundRef	= sfle.d( pE, fileDirInput, "abun_ref" )
c_allfiles_InputAbundRef= Glob( sfle.d( c_pathInputAbundRef, "*.txt" ))

#Error model
c_pathInputErrModel	= sfle.d( pE, fileDirInput, "error_model" )
c_fileInputErrModel	= File(sfle.d( c_pathInputErrModel, "ill100v5_p.gzip" ))

#src script
c_fileProgConvert	= File(sfle.d( pE, sfle.c_strDirSrc, "convert_ref.py" ))
c_fileProgKO		= File(sfle.d( pE, sfle.c_strDirSrc, "ko_counter.py" ))
c_fileProgCheck		= File(sfle.d( pE, sfle.c_strDirSrc, "check_contig.py"))

#Converted ref files
c_pathConvertedref	= sfle.d( fileDirTmp, "converted" )
c_allfiles_Converted	= [ sfle.d( pE, c_pathConvertedref, sfle.rebase( f ) ) for f in c_allfiles_InputAbundRef ]

#Generate checked genome path
c_pathChecked = sfle.d( fileDirTmp, "checked_genome" )
c_allpaths_Checked = [sfle.d( c_pathChecked, sfle.rebase( InputRef, ".txt" ) ) for InputRef in c_allfiles_InputAbundRef]

#Generate synthetic sequencing data
c_path_Synseq		= sfle.d( fileDirOutput, "Synseq")
c_allfilespath_Synseq_fir	= [sfle.d( pE, c_path_Synseq, sfle.rebase( f, ".txt", "_fir.fastq" ) ) for f in c_allfiles_InputAbundRef]
c_allfilespath_Synseq_sec	= [sfle.d( pE, c_path_Synseq, sfle.rebase( f, ".txt", "_sec.fastq" ) ) for f in c_allfiles_InputAbundRef]

#Log file for synthetic script
c_path_Synseq_log	= sfle.d( fileDirTmp, "Synseq" )

"""
#Generate ko gold standard files
c_path_KO		= sfle.d( pE, fileDirOutput, "KO")
c_allfiles_KO		= [sfle.d( c_path_KO, os.path.basename(f) ) for f in c_allfiles_InputAbundRef]
"""

"""
Processing module 1
===================

Convert reference abundance file and check the genome files to filter out short contigs.
"""

for InputRef in c_allfiles_InputAbundRef:

	Converted = sfle.d( pE, c_pathConvertedref, sfle.rebase( InputRef ) )
	sfle.op( pE, c_fileProgConvert, ["-i", [InputRef], "-r", c_fileInputTaxonDir, "-o", [True, Converted]] )


for ConvertedRef in c_allfiles_Converted:
	Checked = sfle.d( c_pathChecked, sfle.rebase( ConvertedRef, ".txt" ) )
	sfle.sop( pE, "mkdir -p", [[Checked]] )
	sfle.op( pE, c_fileProgCheck, ["-i", [ConvertedRef], "-g", c_pathInputGenomeDir, "-o", [True, Checked]] )

"""
Processing module 2-3
==================

Synthesize sequencing data and generating KO gold standard file
"""

for InputConvert in c_allfiles_Converted:
	Checked_genomes = sfle.d( c_pathChecked, sfle.rebase( InputConvert, ".txt" ) )
	Log = File( sfle.d( c_path_Synseq_log, "Syn_" + sfle.rebase( InputConvert, ".txt", ".log" ) ) )
	SynSeq = File( sfle.d( c_path_Synseq, sfle.rebase( InputConvert, ".txt" ) ) )
	#Create a dummy log file so the script can find the right path
	sfle.sop( pE, "echo >", [[True, Log]] )
	#Run synthetic script
	sfle.sop( pE, "rby_test1.py", [ "-R", [Checked_genomes], "-a", [InputConvert], "-n", Reads_No, "-l", "d", "-m", c_fileInputErrModel, "-c", "-q", "33", "-o", [True,SynSeq], "-p", "-u", "d", "-z", [Log]] )
	Default( SynSeq )

#Generating gold standard files for genes

for InputRef in c_allfiles_Converted:
	KO_Ref = sfle.d( pE, fileDirOutput, "KO", sfle.rebase( InputRef ) )
	sfle.op( pE, c_fileProgKO, ["-i", [InputRef], "-k", c_pathKO, "-o", [True, KO_Ref]] )
	Default( KO_Ref )

