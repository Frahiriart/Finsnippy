#!/bin/bash

absoname=$(realpath $0)
echo $absoname
absopath=$(dirname $absoname)
cd $absopath
pwd

sudo apt install python3-pip
sudo apt install python-pip
sudo apt install snakemake
sudo apt install bioperl
sudo apt install samtools
sudo apt install bioperl
sudo apt install git
sudo apt install bcftools
chmod u+x bin/snippy_custom
chmod u+x bin/snippy-core-custom
chmod u+x bin/snippy-vcf2tab_custom
chmod u+x bin/snippy-vcf_to_tab_custom
chmod u+x binaries/script/bam2bed.py
chmod u+x binaries/script/csv2json.py
chmod u+x binaries/script/filter_SNP_density_aurelien_v2.py
chmod u+x binaries/script/mtx2mstV2
chmod u+x binaries/script/snokey
chmod u+x binaries/script/vcf2dist
##perl -MCPAN -e shell
pip3  install snakemake
git clone https://github.com/tseemann/snippy.git
chmod u+x snippy
sudo cp -r snippy/* .
sudo rm -r snippy
pip3 install PyVCF
pip install PyVCF
pip3 install pandas
pip install pandas
pip3 install networkx
pip3 install bokeh
pip3 install numpy
pip3 install scipy
cd binaries/script
git clone --recursive https://github.com/AstraZeneca-NGS/VarDictJava.git
cd VarDictJava
./gradlew clean installDist
./gradlew clean javadoc
./gradlew distZip
cd $absopath
