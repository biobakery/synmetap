SynMetaP User Guide v1.1
========================

January 2014

Boyu Ren and Curtis Huttenhower

Table of Contents
-----------------

A. Introduction to SynMetaP  
B. Related Projects and Scripts  
C. Installing SynMetaP  
D. SynMetaP Inputs  
E. SynMetaP Outputs  
F. 

# A. Introduction to SynMetaP

SynMetaP is a [SflE](http://huttenhower.sph.harvard.edu/sfle/output/sphinx/index.html) project used to simulate shotgun metagenomic sequencing data from next-generation sequencing platforms for user-defined microbial communities. It also calculates gold-standard gene and functional contents abundance for the communities if requested. The simuation process is based on an algorithm [GemSIM](http://sourceforge.net/projects/gemsim/) using realistic error-model summarized from sequencing data of certain platforms.

# B. Related Projects and Scripts

[SflE]((http://huttenhower.sph.harvard.edu/sfle/output/sphinx/index.html) is the framework for the SynMetaP. It helps building a stable pipeline to automatically convert the raw input data into useful results. More details can be found in their project homepage.

[GemSIM](http://sourceforge.net/projects/gemsim/) is the core for this pipeline. This project can summarize an error-model of certain sequencing platforms from the real sequencing data and further utilize this model to reconstruct synthetic shotgun sequencing results for known genomes or metagenomes. More details can be found in their project homepage.

[Picard](http://picard.sourceforge.net/) comprises Java-based command-line utitilities that manipulate SAM files. Since the synthetic data from GemSIM are formated as fastq, they are with huge volume and not easy to transfer. We use Picard to convert the fastq files into unaligned bam files to significantly reduce their sizes. The script we use is [FastqToSam](http://picard.sourceforge.net/command-line-overview.shtml#FastqToSam).

# C. Installing SynMetaP

SynMetaP is formulated as a [SflE](http://huttenhower.sph.harvard.edu/sfle/output/sphinx/index.html) project. You need to install the SflE before using SynMetaP. Installation documents can be found [here](http://huttenhower.sph.harvard.edu/sfle/output/sphinx/index.html#download).

Once you have configured SflE successfully, no other prequisites are needed. You can clone the whole SynMetaP repository into `sfle/input` folder. To run SynMetaP, you should use the command:

scons output/synmetap

Noting that you should type it in the root directory of SflE.

# D. SynMetaP Inputs

There are only one required input file for users per community. It should be placed in the folder `sfle/input/synmetap/input`. The name of the file will be used to identify the results for the community in the output folders. Other inputs are either provided in the project or should be downloaded from the official database. The details are listed below:

### 1\. Microbial community composition files (required)
The files should be tab-delimited text files with ".txt" extension. In each file, two columns are found. The first column is the name of organisms that are present in the community and the second column is the relative abundance of it. The relative abundances can also be normalized by a constant for one community. Below are some details of format requirements:

i.  We only need genus level, species level and strain level phylogenetic information for the names of the orgasims.
ii. They should be space delimited and the first two fields will be taken as the genus and species of the organism and the rest will be taken as the strain name.
iii. You should not skip the father level before specifying a child level. Not all three levels are required.
iv. No abbreviation is accepted.

Here are some examples:
Escherichia (accepted)
Escherichia coli (accepted)
Escherichia coli ABU 83972 (accepted)
Escherichia ABU 83972 (not accepted)
E. coli (not accepted)

You can find a complete example in `metasynp/input/abunRef_demo.txt`.

###2\. Reference genomes dataset

We use Intergrated Microbial Genomes(IMG) dataset version 3.5 updated in summer 2012. Unfortunately, IMG ftp server is no longer publicly available so for those users who do not have access to this dataset and would like to use it, please contact [Boyu Ren](bor158@mail.harvard.edu).

Technically speaking, the reference genomes dataset is only a collection of files recording the DNA sequences of genomes of certain organisms. The IMG dataset uses fna files to store the sequences information. The details for the format of such sequences files can be found [here](http://en.wikipedia.org/wiki/FASTA_format). IMG dataset also contains gene annotation files for each genome it holds, these are required when you want to calculate the gold-standard abundances of genes and functional units in the communities.

If users have newly assembled genomes that are not published but are desired to use as the references, these genomes sequences should be placed in `metasynp/input/user_genome`. The accompanied gene annotation files should be placed in the same folder.

The name of each sequences file should be unique (referred as <taxon_id> below) with extension ".fna" and the accompanied annotation files should be placed in a folder with the same name (<taxon_id>). If you have annotation files for one genome with different annotation systems, the names should indicate the systems:

	<taxon_id>.gff - Tab delimited GFF3 format for genes.
	<taxon_id>.cog.tab.txt - Tab delimited file for COG annotation.
	<taxon_id>.kog.tab.txt - Tab delimited file for KOG annotation.
	<taxon_id>.pfam.tab.txt - Tab delimited file for Pfam annotation.
	<taxon_id>.tigrfam.tab.txt - Tab delimited file for TIGRFAM annotation.
	<taxon_id>.ipr.tab.txt - Tab delimited file for "other" (Non-Pfam/TIGRFAM) InterPro hits.
	<taxon_id>.ko.txt - Tab delimited file for KO and EC annotation.
	<taxon_id>.signalp.txt - Tab delimited file for signal peptide annotation.
	<taxon_id>.tmhmm.txt - Tab delimited file for transmembrane helices.

Currently we only use KO and EC annotation files for the calculation of gold-standard abundances of genes and functional units.

### 3\. Taxonomy mapping table

We include this table (`metasynp/input/Taxontable_demo`) in the pipeline. It is distributed with 
the IMG genomes dataset. It maps the name of an organism to a qualified genome and further the <taxon_id> for this genome. It also has some additional information to help determine which genome should be picked when multiple genomes satisfy the name of an input organism. The fields of the table that are used in the pipeline are taxon_oid, Status, Genome Name, Genus, Species, Strain and User Provided. The details for these fields are listed below:
	
	taxon_oid - Unique name for a genome, it is the same with the name of the fna file and gene annotation files.
	Status - Whether the genome is finished or still in draft, accepted values are "Finished", "Draft" and "Permanent Draft".
	Genome Name - Human-readable names for the genomes.
	Genus, Species, Strain - Names of the genus, species and strain for the genome.
	User Provided - Whether the genome is a user-provide novel genome.
	
Users are welcomed to add new entries to this table and all they need to fill in are the columns listed above. Please do not modify the existed contents.

### 4\. Error model

Optionally, users can also supply an error model file generated by GemSIM(GemErr.py) to replace the one we distributed for Illumina GA IIx with TrueSeq SBS Kit v5-GA (`metasynp/ill100v5_p.gzip`). Since the error model is highly sensitive to the sequencing platforma as well as the kit, you should replace it when the targeting platform is not the same as Illumina-v5. Details for generating customized error models can be found [here](http://sourceforge.net/projects/gemsim/files/?source=navbar).

### 5\. Pipeline driving script

For each SflE project, there should be a driving script specifying how the workflow should proceed. It is in the folder `synmetap` with name `SConscript` and contains several user-defined constants that can be modified if needed. Below is a list of all paramters that you can modify to make the pipeline compatible with your data and goal. They are written in the very beginning in `synmetap/SConscript`.

	**c_Reads_No**

	This is the number of resulting sequences. You can see it as the number of sequences that are successfully sequenced by the sequencer.

	**c_Min_Contig_Len**

	This is a constant to define minimum size of contigs that will be preserved in the genome sequences file. It is necessary due to technical issue of GemSIM and to circumvent it we have to filter out contigs that are too short. A number larger than 350 is recommended. More details can be found in Part F 1.2.

	**c_pathInputGenomeDir**

	This is the directory of all fna files of genomes from a large publicly available dataset (e.g. IMG).

	**c_pathKO**

	This is the directory containing the folders of KO gene annotation information for the genomes present in the above directory.

You can also comment out all lines in "Processing module 3" if you do not want to calculate the gold-standard abundance of genes and functional units of the communities. Please do not modify all the other contents in this script.

# E. Output files

### 1\. Synthesized sequencing data

We set the sequencing producing paired-end reads as default. The output files
for each input community are two fastq files with _fir and _sec identifiers 
and a compressed BAM file.

### 2\. Gold standard files for genes, pathways and modules

Currently we only generate gold standard abundance files for genes. You can
find them in output/Gene. We will add files for pathways and modules in
near future.

### 3\. Log files

Log files contain some important information concerning taxonomy name mapping and synthesizing sequencing process. You can find them in output/Log. *_convert.log is for name mapping, *_check.log is for short contigs filtering and *_synseq.log is for sythesizing process.

# F. Details of the pipeline

### 1\. Intermediate processes:

#### 1.1 Convert user given abundance files into GemReads compatible abundance files

The GemReads compatible abundance file is very similar to the user-defined abundance file except that the first column is the exact file names of genome sequence files in the input database. Since the users always want to specify the real name of the bugs, we will do this mapping in the pipeline so the GemReads can be driven correctly.

#### 1.2 Check genome sequence files

Normally, the genome sequence files can contain more than one sequence. In this case, they are called contigs. The length for the contigs in one sequence file can vary dramatically. The too short contigs are very likely to crash GemReads. The reason for this is because by default, we generate paired-end reads by GemReads and it will help you choose an empirical insert length
for the paired reads. This empirical data is drawn from the real Illumina sequencing data which is recorded in the error model file we have included in this project.

For Illumina run, the typical length for each end of a pair is around 100 bps and the error model we used consider the minimal insert length as around 300 bps. On the other hand, GemReads does not concatenate all contigs in one genome into one and randomly pick one position to start. It assigns a length-based probability to each contig in one genome sequence file and pick one contig randomly based on this probability. The picked contig will be treated as the template from which the synthetic sequencing data are drawn.

If one contig in the genome sequence file is shorter than 300 bps, it is likely that we cannot slice a typcial Illumina PE reads from it which will cause GemReads crash.

To deal with this issue, we are performing one filtering procedure to delete the too short contigs in the input genome files. This is usually necessary for the draft genome files which are always highly fragmented. The threshold for length is user-defined.

### 2\. Sequencing simulation

We use GemSIM (doi:10.1186/1471-2164-13-74) to carry out the simulation of Illumina sequencing. GemSIM is composed of several separate scripts and the specific script we implement in our pipeline is GemReads.py. This script can simulate both single genome or metagenome sequencing result. In this pipeline, the script is working under metagenomic mode by default.

The relative abundance will be treaded as abundance of real bugs rather than sequences belong to each bug. So for two bugs whose genomes have large distinction in length, even if their relative abundance is the same, the fraction of sequences belong to each bug can be very different.

### 3\. Gold standard files generate

#### 3.1 Bugs abundance gold standard file

This is the input abundance file.

#### 3.2 Genes abundance file

This is done by reading the annotation files in IMG dataset for each input bug. We count the frequency of all different KO's in each bug recorded in the annotation files and normalize this count by the bug's relative abundance. The resulting relative abundance of each KO with regard to the whole community is the sum of all the individual bug's normalized KO frequency. This relative abundance can be multiplied by arbitrary positive real number.
