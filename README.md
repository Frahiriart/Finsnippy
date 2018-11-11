# Phylosnip
Pipeline which make phylogeny with sequence of different sample

## Author & Co-Author
Technician, François HIRIART  
  
Hospital Engineers, Aurelien BIRER  
Professor, Richard BONNET

## Synopsis
Phylosnip is a pipeline of bacterial typing. The pipeline use the data of high-throughput sequencing which will be mapped to an haploid reference genome. Next, Phylosnip find SNP, indels and MNP to discriminate strains to the core genome but also between themselves. Finally, Phylosnip will produce a distance matrice and a network graph.

## Installation
This will install the repositories on github.
```
cd where/you/want/to/install
https://github.com/Frahiriart/Phylosnip.git
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
### Strain File
This table come from [here] (https://github.com/tseemann/snippy)

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
