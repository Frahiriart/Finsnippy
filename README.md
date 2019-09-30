# Phylosnip
Pipeline which make phylogeny with sequence of different sample

## Author & Co-Author
Technician, François HIRIART  
  
Hospital Engineers, Aurelien BIRER  
Professor, Richard BONNET

## Synopsis
Phylosnip is a pipeline of bacterial typing. The pipeline use the data of high-throughput sequencing which will be mapped to an haploid reference genome. Next, Phylosnip find SNP, indels and MNP to discriminate sample to a core genome but also between themselves. Finally, Phylosnip will produce a distance matrice and a network graph.

## Installation
This will install the repositories on github.
```
cd where/you/want/to/install
git clone https://github.com/Frahiriart/Phylosnip.git
```
The script "setup.sh" will install all binaries of this program.
```
cd where/you/want/to/install/Phylosnip
chmod u+x setup.sh
./setup.sh
```
## Input File
* a reference genome in FASTA or GENBANK format (can be in multiple contigs)
* sequence read files in FASTQ or FASTA format (can be .gz compressed) format

## Output File
* 1 folder per sample, named by the name of the sample
* 1 folder which collect and compare the SNP result of all strain and this folder have also distance matrix and network phylogeny, named merge_genome_core_result.

### Sample File
This table come from [snippy page](https://github.com/tseemann/snippy)

Extension | Description
----------|--------------
.tab | A simple [tab-separated](http://en.wikipedia.org/wiki/Tab-separated_values) summary of all the variants
.csv | A [comma-separated](http://en.wikipedia.org/wiki/Comma-separated_values) version of the .tab file
.html | A [HTML](http://en.wikipedia.org/wiki/HTML) version of the .tab file
.vcf | The final annotated variants in [VCF](http://en.wikipedia.org/wiki/Variant_Call_Format) format
.bed | The variants in [BED](http://genome.ucsc.edu/FAQ/FAQformat.html#format1) format
.gff | The variants in [GFF3](http://www.sequenceontology.org/gff3.shtml) format
.bam | The alignments in [BAM](http://en.wikipedia.org/wiki/SAMtools) format. Includes unmapped, multimapping reads. Excludes duplicates.
.bam.bai | Index for the .bam file
.log | A log file with the commands run and their outputs
.aligned.fa | A version of the reference but with `-` at position with `depth=0` and `N` for `0 < depth < --mincov` (**does not have variants**)
.consensus.fa | A version of the reference genome with *all* variants instantiated
.consensus.subs.fa | A version of the reference genome with *only substitution* variants instantiated
.raw.vcf | The unfiltered variant calls from Freebayes
.filt.vcf | The filtered variant calls from Freebayes

#### Columns in the TAB/CSV/HTML formats:

Name | Description
-----|------------
CHROM | The sequence the variant was found in eg. the name after the ```>``` in the FASTA reference
POS | Position in the sequence, counting from 1
TYPE | The variant type: snp ins del complex
REF | The nucleotide(s) in the reference
ALT | The alternate nucleotide(s) supported by the reads
[QUAL](https://en.wikipedia.org/wiki/Phred_quality_score) | probability that the ALT allele is incorrectly specified, expressed on the the phred scale (-10log10(probability)).
FILTER | Either "PASS" or a semicolon-separated list of failed quality control filters.
INFO | additional information (TYPE=Variant_Type;DP=Depth;VD=number_of_Variant;AF=Frequence_of_Variant).

#### Variant Types:

Type | Name | Example
-----|------|-------------
SNV  | Single Nucleotide Variant (=SNP) |  A => T
MNV | Multiple Nuclotide Polymorphism |GC => AT
Insertion  | Insertion of Nucleotide | ATT => AGTT
Deletion  | Deletion of Nucleotide | ACGG => ACG
Complex | Combination of snp/mnp | ATTC => GTTA

###  Core File

### Input File
* a set of Snippy folders which used the same reference sequence (`--genome`).

### Output Files

Extension | Description
----------|--------------
.aln | A core SNP alignment in the FASTA format
.full.aln | A whole genome SNP alignment (includes invariant sites)
.tab | Tab-separated columnar list of **core** Variant sites with alleles and annotations
.nway.tab | Tab-separated columnar list of **all** Variant sites with alleles and annotations
.vcf | Multi-sample VCF file with genotype `GT` tags for all discovered alleles
.txt | Tab-separated columnar list of alignment/core-size statistics
_density_filtered_keep.vcf | Tab-separated columnar list of **core** Variant sites with alleles and annotations which are filtered by density
_density_filtered_unkeep.vcf | Tab-separated columnar list of **core** Variant sites with alleles and annotations which are reject after the density filter
_density_filtered_keep_SNP_dist.tsv | Distance Matrice of all sample between themselves
SNP_network | Phylogeny Network

## Quick Start

#### Download Data Test
if you want to test Pylosnipping with data test you must have [SRA toolkit](https://www.ncbi.nlm.nih.gov/sra/docs/toolkitsoft/). You can download SRA toolkit with this command.

```
wget http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.4.1/sratoolkit.2.4.1-ubuntu64.tar.gz
tar xzvf sratoolkit.2.4.1-ubuntu64.tar.gz
```

Data which will be download come from [this](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5800660/)

```
cd where/you/want/to/install/Phylosnip/test
for i in `cat SRR_Acc_List.txt`; do ~/where/is/sratoolkit.2.9/bin/fastq-dump --split-files $i; gzip -9 $i*; done
sudo apt install rename
for b in `awk '{print "s/"$11"/"$8"/";}' SraRunTable.txt`;do rename `echo $b` *; done
wget https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=378697983&
```

#### Execute Phylosnipping

```
cd where/you/want/to/install/Phylosnip/test
/fastq2phylotreeV1.py -input test -g test/sequence.fasta -o where/you/want/your/resut
```

## Requirements

* Java = 1.8
* Perl >= 5.12
* R >= 3.2.5
* Python 3.6
* Perl Modules : bioperl >= 1.6
* snippy >= 4.3.5
* picard.jar >= 2.18.8
* GenomeAnalysisTK.jar >= 4.0.11.0
* samtools >= 1.7
* bwa mem >= 0.7.12
* bcftools >= 1.7
* GNU parallel >= 2013xxxx
* snpEff >= 4.3
* bedtools >= 2.0
* bcftools >= 1.7
* minimap2 >= 2.0
* vcflib >= 1.0 (vcfstreamsort, vcfuniq, vcffirstheader)
* snp-sites >= 2.0
* seqtk >= 1.2
* samclip >= 0.2
* readseq >= 2.0
* vt >= 0.5
* vcflib >= 1.0

For Linux (compiled on Ubuntu 16.04 LTS) some of the binaries, JARs and scripts are included.
And the binaries can be install with the file `setup.sh`.
