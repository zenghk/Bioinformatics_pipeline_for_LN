import os,sys,csv
import subprocess
from multiprocessing import Pool, Process, Manager
from glob import glob
import Bio
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def batch_iterator(iterator, batch_size) :
	entry = True
	while entry :
		batch = []
		while len(batch) < batch_size :
			try :
				entry = iterator.__next__()
			except StopIteration :
				entry = None
			if entry is None :
				break
			batch.append(entry)
		if batch:
			yield batch

def split_to_subfiles(fasta_iteror):
	for i, batch in enumerate(batch_iterator(fasta_iteror, 25000)):
		filename = "%s/merge_%i.fasta" %(outdir, (i+1))
		handle = open(filename, "w")
		count = SeqIO.write(batch, handle, "fasta")
		handle.close()
		print("Done")

def process_sample(infile):
	fasta_iteror = SeqIO.parse(open(infile), "fasta")
	split_to_subfiles(fasta_iteror)
	
def main(infile):
	process_sample(infile)

if __name__ == '__main__':
	infile = sys.argv[1]
	outdir = sys.argv[2]
	main(infile)
