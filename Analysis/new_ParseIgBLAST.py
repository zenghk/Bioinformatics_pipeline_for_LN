
import os,sys,csv
from Bio import SeqIO
import argparse
import re
import numpy as np

'''Adding the step to cut the beginning of variable region so that the same primer amplified by differetn primers will be the same'''


def trans(s, sstart):
	p, seq, mutnum = 0, [], 0
	SHMs = re.findall('(\d*)([ATGC-])([ATCG-])', s)
	if len(SHMs) == 0:
		return "", 0
	else:
		pos = sstart
		for shm in SHMs:
			continue_match = 0 if shm[0] == '' else int(shm[0])
			pos += continue_match
			if shm[1] == "-":
				seq.append("D%s%d"%(shm[2], pos))
				pos += 1
			elif shm[2] == '-':
				seq.append("I%d%s"%(pos, shm[1]))
			else:
				seq.append("S%s%d%s"%(shm[2], pos, shm[1]))
				pos += 1
				mutnum += 1
		return "".join(seq), mutnum
	
def main():
	fasta_dict = SeqIO.index(infasta,'fasta')
	inf1 = open(infile,'r')
	out = csv.writer(open('%s/%s'%(outdir,outname),'w'),delimiter='\t')
	out.writerow(["CDR3nt", "CDR3aa", "SeqId", "VHits", "DHits", "JHits", "ChainType", "StopCodon", "Frame", "Productive", "Strand", "MultipleBest", "SHM","SHMinfo", "Vinfo", "Dinfo", "Jinfo", "Variable","VRaa"])
	igblast_dict = {}
	myid = ""
	for rec in inf1:
		if rec.startswith("# Query:"):
			if len(myid)!=0:
				if len(Vinfo)>0 and len(Jinfo)>0:
					variable_seq = myseq1.seq[int(Vinfo[8])-1:int(Jinfo[9])]
					if len(cdr3)>0:
						whole_nt = myseq1[int(cdr3[3]) -4:int(cdr3[4]) + 3]
						whole_aa=whole_nt.translate()
						cutoff = (int(Jinfo[9]) - int(cdr3[4]))%3
						FR4 = myseq1[int(cdr3[4]) + 3:int(Jinfo[9]) - cutoff]
						nt_sub, aa_sub = [], []
						for ind, i in enumerate([FR1info, CDR1info, FR2info, CDR2info, FR3info]):
							if ind == 0 and i:
								sinfo, tinfo = int(i[1]) -1 , int(i[2])
								sequences= myseq1[sinfo: tinfo]
								number =  (tinfo - sinfo)%3
								nt_sub.append(str(sequences.seq))
								aa_sub.append(str(sequences[number:].seq.translate()))
							elif ind == 4 and i:
								sinfo, tinfo = int(i[1]) - 1 , int(i[2])
								sequences = myseq1[sinfo:tinfo - 3]
								nt_sub.append(str(sequences.seq))
								aa_sub.append(str(sequences.seq.translate()))
							elif i:
								sinfo, tinfo = int(i[1]) - 1, int(i[2]) 
								sequences= myseq1[sinfo: tinfo]
								nt_sub.append(str(sequences.seq))
								aa_sub.append(str(sequences.seq.translate()))
							else:
								nt_sub.append("NNNN")
								aa_sub.append("NNNN")
						nt_sub.append(str(whole_nt.seq))
						nt_sub.append(str(FR4.seq))
						aa_sub.append(str(whole_nt.seq.translate()))
						aa_sub.append(str(FR4.seq.translate()))
						out.writerow([str(whole_nt.seq),str(whole_aa.seq),myid]+recom+[mutnum, mutinfo, ";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),"|".join(nt_sub), "|".join(aa_sub)])
					else:
						out.writerow(["N/A","N/A",myid]+recom+[mutnum, mutinfo, ";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),"n/A","N/A"])
			myid,recom,cdr3,Vinfo,Dinfo,Jinfo = "",[],[],[],[],[]
			myid = rec.strip().split(" ")[2]
			vnum, dnum, jnum = 0,0,0
			FR1info, CDR1info,FR2info,CDR2info,FR3info = False, False, False, False, False
		elif rec.startswith("IG"):
			recominfo = rec.strip().split("\t")
			if len(recominfo)==8:
				recom = [recominfo[0],"N/A"]+recominfo[1:]
			elif len(recominfo)==9:
				recom = recominfo
		elif rec.startswith("TR"):
			recominfo = rec.strip().split("\t")
			if len(recominfo)==8:
				recom = [recominfo[0],"N/A"]+recominfo[1:]
			elif len(recominfo)==9:
				recom = recominfo
		elif rec.startswith("CDR3\t"):
			cdr3 = rec.strip().split("\t")
		elif rec.startswith("FR1-IMGT"):
			FR1info = rec.strip().split("\t")
		elif rec.startswith("CDR1-IMGT"):
			CDR1info = rec.strip().split("\t")
		elif rec.startswith("FR2-IMGT"):
			FR2info = rec.strip().split("\t")
		elif rec.startswith("CDR2-IMGT"):
			CDR2info = rec.strip().split("\t")
		elif rec.startswith("FR3-IMGT"):
			FR3info = rec.strip().split("\t")
		elif rec.startswith("V\t") and vnum==0:
			Vinfo = rec.strip().split("\t")
			if Vinfo[24]:
				SHMinfo = Vinfo[24]
			else:
				SHMinfo = ""
			Vstart = int(Vinfo[10])
			mutinfo, mutnum = trans(SHMinfo, Vstart)
			if Vinfo[1].startswith("reversed"):
				myseq1 = fasta_dict[myid].reverse_complement()
			else:
				myseq1 = fasta_dict[myid]
			vnum = 1
		elif rec.startswith("D\t") and dnum==0:
			Dinfo = rec.strip().split("\t")
			dnum = 1
		elif rec.startswith("J\t") and jnum==0:
			Jinfo = rec.strip().split("\t")
			jnum = 1
	print(Vinfo, Jinfo, recom)
	if len(Vinfo)>0 and len(Jinfo)>0:
		variable_seq = myseq1.seq[int(Vinfo[8])-1:int(Jinfo[9])]
		if len(cdr3)>0:
			whole_nt= myseq1[int(cdr3[3]) -4:int(cdr3[4]) + 3]
			whole_aa=whole_nt.translate()
			cutoff = (int(Jinfo[9]) - int(cdr3[4]))%3
			FR4 = myseq1[int(cdr3[4]) + 3:int(Jinfo[9]) - cutoff]
			nt_sub, aa_sub = [], []
			for ind, i in enumerate([FR1info, CDR1info, FR2info, CDR2info, FR3info]):
				if ind == 0 and i:
					sinfo, tinfo = int(i[1]) - 1,int(i[2]) 
					sequences= myseq1[sinfo: tinfo]
					number = (tinfo - sinfo)%3
					nt_sub.append(str(sequences.seq))
					aa_sub.append(str(sequences[number:].seq.translate()))
				elif ind == 4 and i:
					sinfo, tinfo = int(i[1]) - 1, int(i[2])
					nt_sub.append(str(myseq1[sinfo:tinfo-3].seq))
					aa_sub.append(str(myseq1.seq[sinfo:tinfo-3].translate()))
				elif i:
					sinfo, tinfo = int(i[1]) - 1, int(i[2])
					sequences= myseq1[sinfo: tinfo]
					nt_sub.append(str(sequences.seq))
					aa_sub.append(str(sequences.seq.translate()))
				else:
					nt_sub.append("NNNN")
					aa_sub.append("NNNN")
			nt_sub.append(str(whole_nt.seq))
			nt_sub.append(str(FR4.seq))
			aa_sub.append(str(whole_nt.seq.translate()))
			aa_sub.append(str(FR4.seq.translate()))
			out.writerow([str(whole_nt.seq),str(whole_aa.seq),myid]+recom+[mutnum, mutinfo, ";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),"|".join(nt_sub),"|".join(aa_sub)])
		else:
			out.writerow(["N/A","N/A",myid]+recom+[mutnum, mutinfo, ";".join(Vinfo[3:12]),";".join(Dinfo[3:12]),";".join(Jinfo[3:12]),"N/A", "N/A"])
	
if __name__=='__main__':
	parser = argparse.ArgumentParser(prog='python ParseIgBLAST.py',usage='%(prog)s -f fasta -i igblast -o outname -d outdir')
	parser.add_argument('-f','--fasta',help='Input fasta format file')
	parser.add_argument('-i','--igblast',help='Input igblast m7 format result')
	parser.add_argument('-d','--outdir',default=".",help='Output file directory')
	parser.add_argument('-o','--outfile',default="result.txt",help='Output tab format file, which record search results.')
	args = parser.parse_args()
	infasta = args.fasta
	infile = args.igblast
	outdir = args.outdir
	outname = args.outfile
	os.system("mkdir -p %s"%outdir)
	main()
