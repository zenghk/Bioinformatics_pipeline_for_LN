export IGDATA=/apps/igblast/ncbi-igblast-1.18.0/bin
/apps/igblast/ncbi-igblast-1.18.0/bin/igblastn \
			 -germline_db_V $2/my_IGHV.fasta \
			 -germline_db_J $2/my_IGHJ.fasta \
			 -germline_db_D $2/my_IGHD.fasta \
			 -organism human \
			 -domain_system imgt \
			 -query $1 \
			 -auxiliary_data /apps/igblast/ncbi-igblast-1.18.0/optional_file/human_gl.aux \
			 -num_threads 8 \
			 -outfmt '7 qseqid sseqid pident length mismatch gapopen gaps qstart qend sstart send evalue bitscore qlen slen qseq sseq score frames qframe sframe positive ppos btop staxids stitle sstrand qcovs qcovhsp' \
			 -ig_seqtype Ig \
			 -num_alignments_V 1 \
			 -num_alignments_D 1 \
			 -num_alignments_J 1 \
			 -out IgBLAST.$1.m7.txt
