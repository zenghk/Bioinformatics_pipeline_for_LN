import pandas as pd
import numpy as np
import glob
import os, sys, csv


def main(output):
	path = os.getcwd()
	infiles = glob.glob("%s/file_*"%path)
	totallist = []
	totalseq = []
	for i in infiles:
		print(i)
		titlelist = ["SeqId", "Sample_id", "Out5ID", "Out3ID", "Prim5Mis", "Prim5ID", "Prim3Mis", "Prim3ID", "UMI5", "UMI3", "CDR3"]
		typelist = ["category"] * len(titlelist)
		typedic = dict(zip(titlelist, typelist))
		df = pd.read_csv("%s/outputsummary.txt"%i, sep = "\t", usecols = titlelist, dtype = typedic)
		df = df[(df["Sample_id"] != "No") & (df["UMI5"]!="NNNN") & (df["UMI3"] != "NNNN") & (df["CDR3"] != "NNNN")]
		seqdf = pd.read_csv("%s/Seqtab.txt"%i, header = None, sep = "\t", usecols = [0,1], quoting = csv.QUOTE_NONE)
		seqdf.columns = ["SeqIds", "Sequence"]
		seqdf["SeqId"] = seqdf["SeqIds"].str.split(" ", expand = True)[0]
		result = pd.merge(seqdf[["SeqId", "Sequence"]], df, on = "SeqId")
		totallist.append(result)	
	totaldf = pd.concat(totallist)
	totaldf.drop_duplicates(subset = ["SeqId"], inplace = True)
	Seqcount = totaldf["Sample_id"].value_counts().to_frame().reset_index()
	Seqcount.to_csv("NumberofSeq2.txt", sep = "\t")
	totaldf.to_csv(output, sep = "\t", index = False)

if __name__ == "__main__":
	output = sys.argv[1]
	main(output)
