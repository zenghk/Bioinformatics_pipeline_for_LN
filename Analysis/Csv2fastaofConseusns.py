import pandas as pd
import csv, os, sys


def main(infile, output):
	df = pd.read_csv(infile, sep = "\t")
	out = csv.writer(open(output, 'w'), delimiter = "\t")
	for i in df[["UMI5", "UMI3", "CDR3nt", "Consensus", "Consensussize"]].values:
		seqid = "|".join([i[0], i[1], i[2], str(i[4])])
		seq = i[3]
		out.writerow([">%s"%seqid])
		out.writerow([seq])
	
if __name__ == "__main__":
	infile, output = sys.argv[1], sys.argv[2]
	main(infile, output)
	
