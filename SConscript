#Boyu Ren Jan 1 2013

import sfle
import sys

Import( "*" )
pE = DefaultEnvironment( )

"""
Header
======

Constant and file definitions.
"""

#============User-defined constant===============

#Number of synthesized reads
c_Reads_No				= 1000

#Minimum contig length
c_Min_Contig_Len		= 840

#path to genome sequence files
c_pathInputGenomeDir	= "/n/CHB/data/synthetic_metagenomes/genomes"

#path to annotation files
c_pathKO				= "/n/CHB/data/IMG_v350/img_w_v350"

#============Script-generated constant================

#IMG dataset taxonomy table file
c_fileInputTaxon		= sfle.d( pE, fileDirInput, "taxontable" )

#Error model file
c_fileInputErrModel		= sfle.d( pE, fileDirInput, "ill100v5_p.gzip" )

#Module structure file
c_fileInModulep			= sfle.d( pE, fileDirInput, "modulep" )

#Input user-defined relative abundance files
c_allfiles_InputAbundRef	= Glob( sfle.d( fileDirInput, "*.txt" ) )

#src scripts
c_fileProgConvert		= sfle.d( pE, sfle.c_strDirSrc, "convert_ref.py" )
c_fileProgKO			= sfle.d( pE, sfle.c_strDirSrc, "ko_counter.py" )
c_fileProgCheck			= sfle.d( pE, sfle.c_strDirSrc, "check_contig.py")
c_fileProgGemReads		= sfle.d( pE, sfle.c_strDirSrc, "rby_test1.py" )
c_fileProgPicard		= sfle.d( pE, sfle.c_strDirSrc, "FastqToSam.jar")
c_fileProgPathab		= sfle.d( pE, sfle.c_strDirSrc, "pathab.py" )

#Converted ref files
c_pathConvertedref		= sfle.d( fileDirTmp, "Converted" )
c_allfiles_Converted		= [sfle.d( pE, c_pathConvertedref, sfle.rebase( fileInAbun ) ) for fileInAbun in c_allfiles_InputAbundRef]
#c_allfiles_Converted_log	= [sfle.d( pE, c_pathConvertedref, sfle.rebase( fileInAbun, ".txt", ".log" ) ) for fileInAbun in c_allfiles_InputAbundRef]

#Checked genome sequences files
c_pathChecked 			= sfle.d( fileDirTmp, "Checked_genome" )
c_allpaths_Checked 		= [sfle.d( c_pathChecked, sfle.rebase( fileInAbun, ".txt" ) ) for fileInAbun in c_allfiles_InputAbundRef]
#possible buggy
#c_allfiles_Checked_log 		= [sfle.d( pE, fileDirTmp, "Checked_genome", sfle.rebase( fileInAbun, ".txt" ), sfle.rebase(fileInAbun, ".txt", ".log") ) for fileInAbun in c_allfiles_InputAbundRef]

#Synthetic sequencing data
c_path_Synseq			= sfle.d( fileDirOutput, "Synseq")
c_allfiles_Synseq_fir		= [sfle.d( pE, c_path_Synseq, sfle.rebase( fileInAbun, ".txt", "_fir.fastq" ) ) for fileInAbun in c_allfiles_InputAbundRef]
c_allfiles_Synseq_sec		= [sfle.d( pE, c_path_Synseq, sfle.rebase( fileInAbun, ".txt", "_sec.fastq" ) ) for fileInAbun in c_allfiles_InputAbundRef]
c_allfiles_Synseq_BAM		= [sfle.d( pE, c_path_Synseq, sfle.rebase( fileInAbun, ".txt", ".bam" ) ) for fileInAbun in c_allfiles_InputAbundRef]

#Gene abundance gold standard files
c_path_Gene			= sfle.d( fileDirOutput, "Gene" )
c_path_Module			= sfle.d( fileDirOutput, "Module" )
c_allfiles_Gene			= [sfle.d( pE, c_path_Gene, sfle.rebase( fileInAbun ) ) for fileInAbun in c_allfiles_InputAbundRef]
c_allfiles_Module		= [sfle.d( pE, c_path_Module, sfle.rebase( fileInAbun ) ) for fileInAbun in c_allfiles_InputAbundRef]

#Log files
c_allfiles_Converted_log, c_allfiles_Checked_log, c_allfiles_Synseq_log, c_allfiles_Synseq_remove_log = ([] for i in xrange( 4 ))
for fileInAbun in c_allfiles_InputAbundRef:
	strBase = sfle.d( fileDirOutput, "Log", sfle.rebase( fileInAbun, ".txt" ), sfle.rebase( fileInAbun, ".txt" ) )
	for astrLogs, strSuff in (
		(c_allfiles_Converted_log, "convert"),
		(c_allfiles_Checked_log, "check"),
		(c_allfiles_Synseq_log, "syn"),
		(c_allfiles_Synseq_remove_log, "syn_remove")):
		astrLogs.append( sfle.d( pE, strBase + "_" + strSuff + ".log" ) )

"""
Processing module 1
===================

Convert reference abundance file and check the genome files to filter out short contigs.

Input: User-created abundance files
Output: Converted GemSIM compatible abundance files, short contig filtered genomes sequences files.

"""
#Convert raw input abundance files
for i, fileInRef in enumerate( c_allfiles_InputAbundRef ):
	sfle.op( pE, c_fileProgConvert, ["-i", [fileInRef], "-r", [c_fileInputTaxon], "-o", [True, c_allfiles_Converted[i]],
		"-l", [True, c_allfiles_Converted_log[i]] ] )
	sfle.op( pE, c_fileProgCheck, ["-i", [c_allfiles_Converted[i]], "-g", c_pathInputGenomeDir, "-o", c_allpaths_Checked[i],
		"-l", [True, c_allfiles_Checked_log[i]], "-n", c_Min_Contig_Len ] )

"""
Processing module 2
==================

Synthesize Illumina metagenomic sequencing data

Input: converted GemSIM compatible abundance files, short contig filtered genomes sequences files
Output: synthesized sequences files

"""

for i, fileInConverted in enumerate( c_allfiles_Converted ):

	#Run GemRead.py script
	#named rby1.py for I tweak the raw script a little
	sfle.sop( pE, "python", [[c_fileProgGemReads], "-R", c_allpaths_Checked[i], "-a", [fileInConverted],
		"-n", c_Reads_No, "-l", "d", "-m", [c_fileInputErrModel], "-c", "-q", 33, "-o", [True, c_allfiles_Synseq_fir[i]],
		"-O", [True, c_allfiles_Synseq_sec[i]], "-p", "-u", "d", "-z", [True, c_allfiles_Synseq_log[i]] ] )
	Depends( c_allfiles_Synseq_log[i], c_allfiles_Checked_log[i] )

	#Consider about how to running picard
	#Generate compressed BAM files
	sfle.sop( pE, "java", ["-jar", [c_fileProgPicard], "F1=", [c_allfiles_Synseq_fir[i]], "F2=", [c_allfiles_Synseq_sec[i]],
		"V=Standard", "SM=GemSim", "O=", [True, c_allfiles_Synseq_BAM[i]] ] )
	Default( c_allfiles_Synseq_BAM[i] )
	
	#Delete fastq files from GemReads.py (rby1.py)
	#Might cause dependency issue but now haven't encounter
	#Depends( sfle.scmd( pE, "rm -f", c_allfiles_Synseq_remove_log[i],
	#	[[c_allfiles_Synseq_fir[i]], [c_allfiles_Synseq_sec[i]]] ), c_allfiles_Synseq_BAM[i] )
	#Default( c_allfiles_Synseq_remove_log[i] )

"""
Processing module 3
=================

Generate gold standard files for genes, pathways and modules

Input: converted GemSIM compatible abundance files, IMG gene annotation files
Output: gold standard files for genes, pathways and modules (under construction) relative abundance.
"""

#Generating gold standard files for genes
for i, fileInConverted in enumerate( c_allfiles_Converted ):
	sfle.op( pE, c_fileProgKO, ["-i", [fileInConverted], "-k", c_pathKO, "-o", [True, c_allfiles_Gene[i]]] )
	sfle.pipe( pE, c_allfiles_Gene[i], c_fileProgPathab, c_allfiles_Module[i], ["-s", [c_fileInModulep]] )
	Default( c_allfiles_Module[i] )
