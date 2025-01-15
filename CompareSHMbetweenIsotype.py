import pandas as pd
import numpy as np
import csv, os, sys
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
font_dir = "/share/home/zenghuikun/font_dir"
for font in font_manager.findSystemFonts(font_dir):
	font_manager.fontManager.addfont(font)
import seaborn as sns
from igraph import *
import re
import Levenshtein
from itertools import combinations
plt.rcParams.update({'font.size':12, 'font.family':'arial'})

def CalSHMrate(infile):
	df = pd.read_csv(infile, sep = "\t", usecols = ["Cgene", "SHM", "CDR3nt"])
	df = df[~df["CDR3nt"].isnull()]
	return df

def SHMfigure(infiles, output, colordic):
	total = []
	for i in infiles:
		df = CalSHMrate(i)
		total.append(df)
	finalresult = pd.concat(total)
	plt.figure(figsize = (2,1.2))
	sns.boxplot(x = "Cgene", y = "SHM", data = finalresult, order = ["IGHM", 'IGHD', "IGHG1", "IGHG2", "IGHG3", "IGHG4", "IGHA1", "IGHA2", "IGHE"],
	palette = colordic, linewidth = 0.5, showfliers = False)
	plt.ylim(0, 100)
	plt.yticks([0,20, 40, 60, 80,100], [0,20, 40, 60, 80,100])
	plt.xticks([0,1,2,3,4,5,6,7,8],["Ig%s"%i for i in ["M", "D", "G1","G2","G3","G4","A1","A2","E"]], rotation = 45)
	plt.savefig(output,dpi = 600, bbox_inches = 'tight')

def CalD(x,y):
	return Levenshtein.distance(x,y)

def Cal(infile, color, output):
	edges = []
	clonedf = pd.read_csv(infile, usecols = ["CDR3aa", "Size", "Fre"], sep = "\t", nrows = 500)
	for i,j in combinations(clonedf.index, 2):
		a, b = clonedf["CDR3aa"][i], clonedf["CDR3aa"][j]
		distance = CalD(a, b)
		if distance <= 1:
			edges.append((i,j))
	g = Graph()
	g.add_vertices(clonedf.shape[0])
	g.add_edges(edges)
	visual_style = {}
	visual_style['vertex_size'] = clonedf["Fre"] * 1500
	visual_style['edge_len'] = 20
	visual_style['bbox'] = (300, 300)
	visual_style['vertex_color'] = np.repeat(color, clonedf.shape[0])
	print(g)
	plot(g, output, **visual_style)

def main(output):
	infiles = glob.glob("IGH*/Seqinfo.txt")
	#Gcolor = ["#22723f", "#58a369", "#9fcd9c", "#d6ead1"]
	#Acolor = ["#cb453e", "#eda791"]
	#colorlist = ['#1f77b4', '#ff7f0e'] + Gcolor + Acolor + ['#da70d6']
	colorlist = ['#7f8084', '#b89353','#f0563f', '#e8876c', '#efac94', '#f7d3c4', '#4f7eb2', '#9fcee9', '#f79464']
	order = ["IGHM", 'IGHD', "IGHG1", "IGHG2", "IGHG3", "IGHG4", "IGHA1", "IGHA2", "IGHE"]
	colordic = dict(zip(order, colorlist))
	SHMfigure(infiles, output, colordic)

	

if __name__ == "__main__":
	output = sys.argv[1]
	main(output)
