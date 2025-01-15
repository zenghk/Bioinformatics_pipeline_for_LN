import pandas as pd
import numpy as np
import csv, os, sys

def Cal(df, gene):
	result = df.groupby(gene).agg({gene:"size", "Size":"sum"})
	result.columns = ["Clonenum", "Readsnum"]
	result = result.reset_index()
	result["Usage"] = result["Clonenum"]/df.shape[0]
	result["Expression"] = result["Readsnum"]/result["Readsnum"].sum()
	return result

def main(infile, prefix=""):
	df = pd.read_csv(infile, sep = "\t")
	Vdf, Jdf = Cal(df, "Vgene"), Cal(df, "Jgene")
	df = df[~df["Dgene"].isnull()]
	Ddf = Cal(df,"Dgene")
	Vdf.to_csv("Vgeneinfo%s.txt"%prefix, sep = "\t", index = False)
	Ddf.to_csv("Dgeneinfo%s.txt"%prefix, sep = "\t", index = False)
	Jdf.to_csv("Jgeneinfo%s.txt"%prefix, sep = "\t", index = False)

if __name__ == "__main__":
	infile = sys.argv[1]
	main(infile)


