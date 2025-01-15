import pandas as pd
import numpy as np
import csv, os, sys

def Cal(df):
	result = df.groupby(["Vgene", "Jgene"]).agg({"Fre":"size", "Size":"sum"})
	result = result.reset_index()
	result["Usage"] = (result["Fre"]/df.shape[0]) * 100
	result["Expression"] = (result["Size"]/result["Size"].sum()) * 100
	return result

def main(infile, output):
	df = pd.read_csv(infile, sep = "\t")
	result = Cal(df)
	result.to_csv(output, sep = "\t", index = False)
	
if __name__ == "__main__":
	infile, output = sys.argv[1], sys.argv[2]
	main(infile, output)


