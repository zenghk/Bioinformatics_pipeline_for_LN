rm MergeTotal.fastq;
for i in `echo file*/merge.assembled.fastq`;do
cat $i >> MergeTotal.fastq;
done
