import pandas as pd
import numpy as np
import matplotlib
from matplotlib import gridspec
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv, sys, os
import glob

def main(out):
	path = os.getcwd()
	infiles = glob.glob("%s/IGH*/Clone.txt"%path)
	result,resultNum = {}, {}
	for infile in infiles:
		isotype = infile.split("/")[-2]
		df = pd.read_csv(infile, nrows = 100, sep = "\t")
		result.setdefault(isotype, df["Fre"].values)
		resultNum.setdefault("Isotype", {})
		resultNum["Isotype"].setdefault(isotype, df["Size"].sum())
	Numdf = pd.DataFrame(resultNum)
	stable = resultNum["Isotype"]["IGHM"]
	Numdf["RelativeSize"] = np.sqrt(Numdf["Isotype"]/stable)
	Numdf["Size"] = np.where(Numdf["RelativeSize"] > 0.3, Numdf["RelativeSize"], 0.3)
	radiusdic = dict(zip(Numdf.index, Numdf["Size"]))
	isotype = ["IGHM", "IGHD", "IGHG1", "IGHG2", "IGHG3", "IGHG4", "IGHA1", "IGHA2", "IGHE"]
	orderdic = dict(zip(isotype, list(range(9))))
	plt.figure(figsize = (9,1))
	gs = gridspec.GridSpec(1,9)
	for i in isotype:
		iradius = radiusdic.get(i, False)
		if iradius:
			data = result[i]
			order = orderdic[i]
			ax = plt.subplot(gs[order])
			ax.pie(data/data.sum(), counterclock = False, startangle = 90, radius = iradius)
	plt.savefig(out, dpi = 600, bbox_inches = 'tight')

if __name__ == "__main__":
	out = sys.argv[1]
	main(out)
