import pandas as pd
import numpy as np
import csv, os, sys

def Assemble(infile, clonefile):
	df = pd.read_csv(infile, sep = "\t", usecols = ["VHits", "DHits", "JHits", "CDR3nt", "SHM", "Vinfo", "CDR3aa"])
	df.fillna("NotFound", inplace = True)
	df["Vgene"] = df["VHits"].str.split("\*", expand = True)[0]
	df["Dgene"] = df["DHits"].str.split("\*", expand = True)[0]
	df["Jgene"] = df["JHits"].str.split("\*", expand = True)[0]
	print(df.shape[0])
	df = df[~df["CDR3nt"].isnull()]
	print(df.shape[0])
	df["Vlength"] = df["Vinfo"].str.split(";", expand = True)[1].astype(int)
	groups = df.groupby(["Vgene", "Jgene", "CDR3nt"])
	result = groups.size().to_frame().reset_index()
	SHM = groups["SHM"].apply(np.mean).to_frame().reset_index()
	SHM.columns = ["Vgene", "Jgene", "CDR3nt", "AverageSHM"]
	result.columns = ["Vgene", "Jgene", "CDR3nt", "Size"]
	print(result["Size"].sum())
	result["Fre"] = result["Size"]/result["Size"].sum()
	final = pd.merge(result, SHM, on = ["Vgene", "Jgene", "CDR3nt"])
	CDR3df = df[["CDR3nt", "CDR3aa"]]
	Ddf = df[["Vgene", "Dgene", "Jgene", "CDR3nt"]]
	Ddf.drop_duplicates(subset = ["Vgene", "Jgene", "CDR3nt"], inplace = True)
	CDR3info = CDR3df.groupby("CDR3nt").agg(lambda x:x.value_counts().index[0]).reset_index()
	final = pd.merge(final, CDR3info, on = 'CDR3nt', how = 'left')
	final = pd.merge(final, Ddf, on = ["Vgene", "Jgene", "CDR3nt"])
	final.sort_values(by = "Fre", ascending  = False, inplace = True)
	final['CloneRank'] = np.arange(0, final.shape[0])
	final.to_csv(clonefile, sep = "\t", index = False)

if __name__ == "__main__":
	infile, clonefile = sys.argv[1], sys.argv[2]
	Assemble(infile, clonefile)
