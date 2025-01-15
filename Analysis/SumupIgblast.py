import pandas as pd 
import numpy as np
import csv, os, sys
import glob
import multiprocessing as mp



def Readfile(infile):
	df = pd.read_csv(infile, sep = "\t")
	#df = df[~df["CDR3nt"].isna()]
	return df

def Readblast(infile):
	df = pd.read_csv(infile, header = None, sep = "\t")
	#df.columns = ["SeqId", "CHits", "identity", "length", "mis", "gap", "q_s", "q_e", "s_s", "s_e", "evalue", "score"]
	df.columns = ["SeqId", "CHits", "Mis", "Identity", "Query", "Subject"]
	df.drop_duplicates(subset = ["SeqId"], inplace = True)
	return df

def main(output):
	path = os.getcwd()
	infiles = glob.glob("%s/subfile_fasta/Seq*"%path)
	print(infiles)
	pool = mp.Pool()
	res = pool.map(Readfile, infiles)
	totaldf = pd.concat(res)
	totaldf.drop_duplicates(subset = ["SeqId"], inplace = True)
	totaldf.to_csv("SeqinfoPrimer.txt", sep = "\t", index = False)
	infiles2 = glob.glob("%s/subfile_fasta/BLAST*.txt"%path)
	pool2 = mp.Pool()
	res2 = pool.map(Readblast, infiles2)
	Cdf = pd.concat(res2)
	Cdf.drop_duplicates(subset = ["SeqId"], inplace = True)
	result = pd.merge(totaldf, Cdf, on = "SeqId")
	result.to_csv(output, sep = "\t", index = False)


if __name__ == "__main__":
	output = sys.argv[1]
	main(output)
