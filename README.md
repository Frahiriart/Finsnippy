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
You will have 2 type of folder:
  - 1 folder per sample
  - 1 folder which collect and compare the SNP result of all strain and this folder have also distance matrix and network phylogeny.

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

#### Columns in the TAB/CSV/HTML formats

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

#### Variant Types

Type | Name | Example
-----|------|-------------
SNV  | Single Nucleotide Variant (=SNP) |  A => T
MNV | Multiple Nuclotide Polymorphism |GC => AT
Insertion  | Insertion of Nucleotide | ATT => AGTT
Deletion  | Deletion of Nucleotide | ACGG => ACG
Complex | Combination of snp/mnp | ATTC => GTTA


