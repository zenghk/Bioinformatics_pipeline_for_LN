import pandas as pd
import numpy as np
import csv, os, sys
import glob

def main():
	path = os.getcwd()
	infiles = glob.glob("%s/Lib*/Numberof*"%path)
	totals = []
	for i in infiles:
		df = pd.read_csv(i, sep = "\t", index_col = "Unnamed: 0")
		df = df[df['index'] != "No"]
		df.columns = ["Sample", "Number"]
		totals.append(df)
	result = pd.concat(totals)
	meta = pd.read_csv("%s/conf_library.csv"%path, sep = "\t", usecols = ["Library", "Bar5", "SampleName"])
	meta.columns = ["Index", "Barcode", "Sample"]
	final = pd.merge(meta, result, on = "Sample")	
	figdf = pd.pivot_table(index = "Index", columns = "Barcode", values = "Number", data = final)
	gapdf = pd.DataFrame(index = ["Lib%d"%i for i in range(1,17)], columns = ["B5_%d"%j for j in range(1,9)]).fillna(0)
	gapdf = figdf + gapdf
	gapdf = gapdf.loc[["Lib%d"%i for i in range(1,17)],["B5_%d"%j for j in range(1,9)]].fillna(0)
	seqdate = path.split("/")[-1]
	gapdf.to_csv("NumberofSeq%s.csv"%seqdate, sep = "\t")

if __name__ == "__main__":
	main()
