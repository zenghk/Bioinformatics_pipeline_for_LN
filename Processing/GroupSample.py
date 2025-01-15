import pandas as pd
import csv, os, sys
import numpy as np

def main(infile):
	df = pd.read_csv(infile, sep = "\t")
	for sample, group in df.groupby("Sample_id"):
		os.system("mkdir -p %s"%sample)
		subgroups = group.groupby("Prim3ID")
		print(sample)
		for isotype, subgroup in subgroups:
			subgroup.to_csv("%s/%s_file.txt"%(sample, isotype), sep = "\t", index = False)


if __name__ == "__main__":
	infile = sys.argv[1]
	main(infile)
