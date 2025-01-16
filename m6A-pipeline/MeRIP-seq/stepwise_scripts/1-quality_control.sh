#!/bin/sh

# Configures here
# Softwares
cutadapt="/software/biosoft/software/python/python2.7_2018_12/bin/cutadapt"
trimmomatic="/software/biosoft/software/Trimmomatic-0.36/trimmomatic-0.36.jar"
fastqc="/software/biosoft/software/fastqc/FastQC/fastqc"

# Input and working directories
raw_data_dir="/path/to/raw_data"
work_dir="/path/to/workdir"

# Parameters
threads=8
adapters="CTGTCTCTTATA"

mkdir -p "$work_dir" && cd "$work_dir"
mkdir -p 1-cleandata && cd 1-cleandata && mkdir fastqc

# Step 1: FastQC
${fastqc} ${raw_data_dir}/*.fastq.gz -t ${threads} -o ./fastqc

# Step 2: Cutadapt
# For paired-end data
${cutadapt} -a ${adapters} -A ${adapters} \
            -o cutadapt_1.fastq.gz -p cutadapt_2.fastq.gz \
            ${rawdata}/*1.fastq.gz ${rawdata}/*2.fastq.gz

${fastqc} cutadapt_1.fastq.gz -t 4 -o ./fastqc
${fastqc} cutadapt_2.fastq.gz -t 4 -o ./fastqc

gunzip cutadapt_1.fastq.gz
gunzip cutadapt_2.fastq.gz

# Step 3: Trimmomatic
# For paired-end datas
java -Xmx4g -jar ${trimmomatic} PE -phred33 \
    cutadapt_1.fastq cutadapt_2.fastq \
    trim1_1.fastq.gz unpaired1_1.fastq.gz \
    trim1_2.fastq.gz unpaired1_2.fastq.gz \
    LEADING:20 TRAILING:20 SLIDINGWINDOW:4:15 MINLEN:35

${fastqc} trim1_1.fastq.gz -t 4 -o ./fastqc
${fastqc} trim1_2.fastq.gz -t 4 -o ./fastqc

rm cutadapt_1.fastq
rm cutadapt_2.fastq