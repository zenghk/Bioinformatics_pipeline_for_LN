import os

def main():
	oldname1 = ['IgA74', 'IgD70', 'IgG1-3', 'IgG2-4', 'IgM73', 'IgE71', 'IgA27', 'IgD22', 'IgG24', 'IgM23', 'IgE28', 'TCRb-CR40', 'V19R-78', 'KCR26',"LCR", "TCRbR55"]
	oldname2 = ["C57IgA-R2", "C57IgM-R","C57IgD-R", "C57IgG1and2-R", "C57IgG3-R", "C57IgE-R"]
	newname1 = ['IgA', 'IgD', 'IgG1', 'IgG2', 'IgM', 'IgE', 'IgA', 'IgD', 'IgG1', 'IgM', 'IgE', "TCRB", "TCRB",'IgK', 'IgL',"TCRB"]
	newname2 = ["IgA", "IgM", "IgD","IgG1", "IgG2", "IgE"]
	oldname = oldname1 + oldname2
	newname = newname1 + newname2
	for ind, i in enumerate(oldname):
		oldpath = "%s_file.txt"%i
		newpath = "%s.txt"%newname[ind]
		if os.path.exists(oldpath):
			os.system("mkdir -p %s"%newname[ind])
			os.system("mv %s %s"%(oldpath, newpath))
		

if __name__ == "__main__":
	main()
