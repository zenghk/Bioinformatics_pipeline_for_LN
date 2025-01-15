import pandas as pd
import numpy as np
import csv, os, sys
import glob 

def main():
	path = os.getcwd()
	infiles = glob.glob("%s/Ig*/Seqinfo.txt"%path)
	totalresult = []
	print(infiles)
	for i in infiles:
		df = pd.read_csv(i, sep = "\t")
		totalresult.append(df)
	totaldf = pd.concat(totalresult)
	totaldf["Cgene"] = totaldf["CHits"].str.split("\*", expand = True)[0]
	del totaldf["CHits"]
	groups = totaldf.groupby("Cgene")
	os.system("mkdir -p Analysis")
	for Cgene, group in groups:
		os.system("mkdir -p Analysis/%s"%Cgene)
		group.to_csv("Analysis/%s/Seqinfo.txt"%Cgene, sep = "\t", index = False)
	
if __name__ == "__main__":
	main()
