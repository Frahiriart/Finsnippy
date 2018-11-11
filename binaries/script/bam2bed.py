#!/usr/bin/python3

import argparse, os, re

def run():
    parser= argparse.ArgumentParser(description="convert bam to bed")
    parser.add_argument('-i','--input', dest="bam", default='', help="Enter your input file")
    args=parser.parse_args()
    main(args)

def main(args):
    print(os.getcwd())
    path=args.bam
    dir=os.path.dirname(path) + "/"
    os.system("samtools view -H " + path + " > " + dir + "temp_file_header_bam")
    bam=open(dir + "temp_file_header_bam", 'r')
    bed=open(dir + "good.bed", 'w')
    for line in bam:
        regex = re.search(r"^@SQ\tSN:(?P<chr>[^\t]+)\tLN:(?P<length>\S*)", line)
        part=500000
        if regex is not None:
#            print(line)
#            print(regex.group('chr'))
#            print(regex.group('length'))
            divi = int(regex.group('length'))//part
            reste = int(regex.group('length'))%part
            line_bed=regex.group('chr') + "\t0\t" + regex.group('length') + "\n"
            #bed.write(line_bed)
            i=1
            while i < divi:
                line_bed=regex.group('chr') + "\t" + str((i-1)*part) + "\t" + str(i*part) + "\n"
                i+=1
                print(i)
                bed.write(line_bed)
            line_bed=regex.group('chr') + "\t" + str(divi*part) + "\t" + str(divi*part+reste) + "\n"
            bed.write(line_bed)
            print(reste)
            print(divi)            
            print(regex.group('length'))
    bam.close()
    bed.close()
    os.system("rm " + dir + "temp_file_header_bam")
if __name__ == "__main__":
    run()
