#!/usr/bin/python3

import argparse
import os
import glob
import re
import json
import sys
import subprocess
import multiprocessing



def run():
    """
    Take the argument of the command and give a variable for this
    :return: args
    """
    parser = argparse.ArgumentParser(
        description="This program make a phylogenetic tree with NGS sequence reads and one or more reference genome")
    parser.add_argument('-i', '--repRead', dest="repRead", default='',
                        help='Enter the path of the directory which contain your fasta/fastq/fas/fa(.gz) reads')
    parser.add_argument('-o', '--repResult', dest="repResult", default='',
                        help="""Enter the path of your directory where you want your result (without other result or
                        risk of nothing that will be done)""")
    parser.add_argument('-g', '--repGenomeRef', dest="genomeRef", default='',
                        help="""Enter the path of your directory which contain your reference genome
                        (if no configfile enter the path to your reference genome)""")
    parser.add_argument('-c', '--config', dest="config", default=0, help="Enter the path of your csv file which "
                                                                         "config the association of genome with "
                                                                         "strain (help of csv2json.py for see how "
                                                                         "make this csv file)")
    parser.add_argument('-C', '--core', dest="core", default=multiprocessing.cpu_count(),
                        help="Enter the number of the cores that you want to give to this program")
    parser.add_argument('-f', '--minfrac', dest="minfrac", default=0.8, help="Minumum proportion for variant evidence")
    parser.add_argument('-m', '--mincov', dest="mincov", default=10, help="Minimum coverage of variant site")

    #print(__file__)
    args = parser.parse_args()
    #    cwd = os.getcwd()
    #    print("\n", cwd, "\n") # test path&cwd
    if os.path.exists(args.repRead):  # if the folder of reads exist, continue
        args.repRead = os.path.abspath(args.repRead)
        if os.path.exists(args.genomeRef):  # if the folder of genome exist, continue
            args.genomeRef = os.path.abspath(args.genomeRef)
            if os.path.exists(args.repResult) is None:
                os.makedirs(args.repResult)
            args.repResult = os.path.abspath(args.repResult)

            if args.config == 0:  # if there are no argument for configuration file, call the function main with args
                prog = os.path.abspath(os.path.dirname(__file__))
                os.chdir(prog)
                main(args)

            elif os.path.exists(
                    args.config):  # else if argument for config is given and his path exist,
                # call the function csv2json and after the function main with args
                args.config = os.path.abspath(args.config)
                prog = os.path.abspath(os.path.dirname(__file__))
                os.chdir(prog)
                Jsonconvert(args.config)
                main(args)


    # else : quit the program and print an help message
            else:
                print("your config path don't exists or we haven't the permission\n")
                sys.exit()
        else:
            print("your path of reference genome path don't exists or we haven't the permission\n")
            sys.exit()
    else:
        print("your path of reads don't exists or we haven't the permission\n")
        sys.exit()


def Jsonconvert(csvfile):
    """
    This call csv2json.py and take a csv file for make a json file
    :param: csvfile:
    :return: config_geno_strain.json
    """
    csvfile = "./csv2json.py -i " + csvfile
    # os.system(csvfile)
    p = subprocess.Popen(csvfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    p_status = p.wait()
    print(output, "\n\n", err)
    print("\n\n", p_status)



def main(args):
    """
    This make a configuration file with argument for launch of snakemake
    :param args:
    :return: configfile.json
    """

    """cwd = os.getcwd()
    print(cwd, "\n", prog)
    print(__file__)"""  # test path&cwd

    gzOrNot = [".gz", ""]
    listExtG = [".fasta", ".genbank", "gb", ".fa", ".fas"]
    listExtS = [".fasta", ".fastq", ".fa", ".fas"]

    repRead = args.repRead
    listRepRead = [repRead]
    repResult = args.repResult
    genomeRef = args.genomeRef
    config = args.config
    # """

    configsouche = {}
    species = {}
    temp_dico = {}

    # if configuration file is given, make configfile.json with this for attribute strain to genome
    if config:
        conf = open("config_geno_strain.json", "r")
        config_dico = json.load(conf)
        configsouche = config_dico['dico']
        #print(configsouche["newRef.fasta"], "\n")
        #print(type(configsouche))

        if not os.path.isdir(genomeRef):
            print("""\nYou have enter a file and not the folder which contain genome(s),
             with the option configfile it isn't right\n""")
            sys.exit()

        file_geno = []
        for genome in configsouche:  # browse the list of genome
            #print(genome)
            gename = genome + "*"
            tempath = glob.glob(os.path.join(genomeRef, gename))
            #if there are not "_" after the name of genome but directly the extension(.fasta, .genbank, .etc)
            if len(tempath) == 0:
                gename = genome + ".*"
            tempath = glob.glob(os.path.join(genomeRef, gename))
            #print(tempath, "\n")
            if len(tempath) > 1:
                print("""\nThere are 2 file with the same genome name but different extension please correct this,
                because i can't choose\n""")
                sys.exit()

            if not os.path.exists(tempath[0]):  # if there are missing genome print help message and quit
                print("\nAll genome of the csv file aren't in directory or we haven't the permission to enter\n")
                sys.exit()

            dictStrain = {}
            temp_dico[tempath[0]] = genome
            temp = configsouche[genome]
            for strain in temp:  # browse the list of strain by genome
                tempath = strain + "*.*"
                tempath = glob.glob(os.path.join(repRead, tempath))
                # print(tempath)
                # if there are not only 2 path(for pair end) or 1 path (for single end),
                # print help message and quit program
                if len(tempath) == 1:
                    tempextS = os.path.basename(tempath[0])
                    tempextS = tempextS[len(strain):]
                    dictStrain[strain] = [tempextS]
                elif len(tempath) == 2:
                    tempextS = os.path.basename(tempath[0])
                    tempextS = tempextS[len(strain):]
                    dictStrain[strain] = [tempextS]
                    tempextS = os.path.basename(tempath[1])
                    tempextS = tempextS[len(strain):]
                    dictStrain[strain].append(tempextS)
                else:
                    print(
                        """\nAll strains ((R1 and R2) or single end) of the csv file aren't in directory
                        or too many reads (>3) with same name or we haven't the permission to enter\n""")
                    sys.exit()

            configsouche[genome] = dictStrain

        #print(configsouche)

        #print("\n", file_geno)
        for name in temp_dico:
            print("\nyo ", temp_dico[name])
            nameSpecies = os.path.basename(name)
            tempextG = nameSpecies[len(temp_dico[name]):]
            nameSpecies = temp_dico[name]
            #print(tempextG)
            species[nameSpecies] = tempextG
            test = 0
            for gon in gzOrNot:
                for leg in listExtG:
                    if re.match(".*" + leg + gon + "$", tempextG) is not None:
                        test += 1
            if test == 0:
                print(
                    """\nThe file of your genome reference haven't the good format please verify that you have enter "
                    (if no configfile enter directly the path of reference genome file)""")
                sys.exit()

    #print("\n\n", fileGeno)
    #print(ext)
# ----------------------------------------------------------------------------------------------------------------------
    # else, there no configuration file for this program
    else:
        nameSpecies = os.path.basename(genomeRef)
        genomeRef = genomeRef[0:genomeRef.find(os.path.basename(genomeRef)) - 1]
        nameSpecies = ''.join(nameSpecies)
        extGeno = nameSpecies[nameSpecies.find("."):]
        nameSpecies = nameSpecies[0:nameSpecies.find(".")]
        species[nameSpecies] = extGeno

        test = 0
        for gon in gzOrNot:
            for leg in listExtG:
                if re.match(".*" + leg + gon + "$", extGeno) is not None:
                    test += 1
        if test == 0:
            print(
                """\nThe file of your genome reference haven't the good format please verify that you have enter
                (if no configfile enter directly the path of reference genome file)""")
            sys.exit()

        files = []
        files += glob.glob(os.path.join(repRead, "*.fa*"))
        files.sort()
        print(files)

        nomSouche = {}
        test = 0
        verif = "n"
        temp = 1
        compteur = 0
        for qqch in files:
            nameStrain = os.path.basename(qqch)[0:os.path.basename(qqch).find("_")]
            postNameStrain = os.path.basename(qqch)[os.path.basename(qqch).find("_"):]
            #extStrain.append(postNameStrain)
            #print(postNameStrain)
            #print(nameStrain)
            for gon in gzOrNot:
                for les in listExtS:
                    # extension = re.compile(".*" + les + gon + "$")
                    # print(extension)
                    # print(re.match(".*" + les + gon + "$", postNameStrain))
                    if re.match(".*" + les + gon + "$", postNameStrain) is not None:
                        test += 1
                        # print(test)
                        if nameStrain != temp:
                            nomSouche[nameStrain] = [postNameStrain]
                            temp = nameStrain
                            compteur = 0
                        elif compteur == 0:
                            nomSouche[nameStrain].append(postNameStrain)
                            compteur = 1
                        else:
                            print("There more than 2 read with same strain name")
                            sys.exit()

            #print(test)
            if test == 0 and verif == "n":
                verif = input(
                    """\nIt is normal that some file in reads folder haven't good extension ?
                    (it can be a problem or not) (y/n):""")
                if verif == "n":
                    print("\nMake sure that all reads file have the good extension")
                    sys.exit()
            test = 0

        # print(ext)
        # """
        configsouche[nameSpecies] = nomSouche

    #print(configsouche)

    configfile = open("configfile.json", "w")

    # write the configuration file in json format with all variable used by the snakemake pipeline
    configfile.write(json.dumps({'dirResult': repResult,
                                 'repRead': repRead,
                                 'genomeRef': genomeRef,
                                 'species': species,
                                 'configsouche': configsouche,
                                 'minfrac': args.minfrac,
                                 'mincov': args.mincov},
                                indent=4))
    configfile.close()
    snakelaunch(args)


# """


def snakelaunch(args):
    """
    This function launch the pipeline make with snakemake
    """
    cmd = 'snakemake -s binaries/script/snokey --cores ' + str(args.core)
    print(cmd)
    cwd = os.getcwd()
    print("\n", cwd, "\n")  # test path&cwd
    os.system(cmd)


if __name__ == '__main__':
    run()
