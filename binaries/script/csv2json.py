#!/usr/bin/python3

import csv
import json
import argparse
import sys


def run():
    """
   Take the argument of the command and give a variable for this
    :return:
    """
    parser = argparse.ArgumentParser(description= """This program convert your csv file in json wich is readable by fastq2pylotreeV1.py. 
    For that make an excel file with 2 columns (header: \"souches\" and \"genome\",and put your strains in \"souches\" in same line of her reference genome in \"genomes\" """)
    parser.add_argument('-i', '--input', dest="csv_input", default='', help="Enter your csv file")
    args = parser.parse_args()
    main(args)

def main(args):
    """
    Create 1 json file which contain strains associate with her core genome and
    if you have enter a header named "MLST:nameofMLSTschema",
    create a second json file with the st number associate with st number
    :param args:
    :return:
    """

    csvInput=args.csv_input
    with open(csvInput, 'r') as file:
        reader = csv.DictReader(file, dialect='excel')

        dicoSnake = {}
        dicograph = {}
        compteur = 0
        cond = 0
        # read the header of the csv file and find the 2 essential header and the other which are optional
        for head in reader.fieldnames:
            if head == "genomes" or head == "souches":
                compteur += 1
                continue
            elif head.find("MLST:") != -1:
                MLSTtype = head[head.find("MLST:") + 5:]
                cond += 1
                print(MLSTtype)

        if compteur < 2:
            print("There are not the header 'souches' or 'genomes'")
            sys.exit()
        elif compteur > 2:
            print("there are too many header name 'souches' or 'genomes'")
            sys.exit()
        elif cond > 1:
            print("There are more than two header with the word 'MLST'")
            sys.exit(0)

#"""
        print(reader)
        for row in reader:
            indic = 0
            for cle in dicoSnake:
                #print(cle)
                if cle == row['genomes']:
                    dicoSnake[row['genomes']].append(row['souches'])
                    indic = 1
            if indic == 0:
                dicoSnake[row['genomes']] = []
                dicoSnake[row['genomes']].append(row['souches'])
            if cond == 1:
                dicograph[row['souches']] = row[head]

        dicograph['MLST_schema'] = MLSTtype
        print(dicograph)
        #print(dicoSnake)
        configfile = open("config_geno_strain.json", "w")
        configfile.write(json.dumps({'dico': dicoSnake}, indent=4))
        configfile.close

        configfile = open("configSTnumber.json", "w")
        configfile.write(json.dumps({'dico': dicograph}, indent=4))
        configfile.close
#"""


if __name__ == '__main__':
    run()