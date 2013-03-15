Synthetic Metagenomics Simulator v 1 Feb 2013

Thank you for using my method, come back later for more details!

This is the first bitbucket repo for me.

You can modify the number of reads generated in SConscript.

You should include rby_test1.py (slightly modified GemRead.py) in your PATH.
This pipeline treats it as an external script. It is included in src/

You should modify the path to FastqToSam.py (used to generate bam files from fastq files) in your Sconscript files. This pipeline treats it as an external script. It is included in src/.

It uses fasta files, KO reference files and taxonomy table from /n/CHB/data/IMG_v350. So please make sure you are in hutlab server or you can modify the path to these files in SConscript file (use absolute path).
For taxonomy table path: modify c_pathInputTaxonDir
For reference genomes path: modify c_pathInputGenomeDir
For reference KO files: modify c_pathKO
