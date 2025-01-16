#!/bin/sh

# Configures here
# Softwares
export PATH=$PATH:/software/biosoft/software/subread-2.0.1-source/bin
export PATH=$PATH:/software/biosoft/software/hisat2-2.0.5
export PATH=$PATH:/software/biosoft/software/samtools-1.9
export PATH=$PATH:/software/biosoft/software/bedtools2/bin

# Input and working directories
work_dir="/path/to/workdir"

ref="/path/to/Homo_sapiens.GRCh37.62.dna.chromosome.all.chr.fa"
GTF="/path/to/Homo_sapiens.GRCh37.72.chr.gtf"
refGene="/path/to/single-transcript-chr"