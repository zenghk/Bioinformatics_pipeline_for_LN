Scriptdir="/share/home/zenghuikun/Novaseqsamples/.Script"
Referencedir="/share/home/zenghuikun/Novaseqsamples/Reference"

for k in $1;do cd ${k};python ${Scriptdir}/Rename.py;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "Rename" 10s


for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -f $i.txt ];then
bsub -n 20 -q mpi -e err -o out python ${Scriptdir}/GetConsensus_V2.py ${i}.txt 5 ${i}/Consensus.txt;
fi;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "Consensus" 60s


for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -f "${i}/Consensus.txt" ];then 
cd ${i};bsub -n 4 -q mpi -e err -o out python ${Scriptdir}/Csv2fastaofConseusns.py Consensus.txt Consensus.fasta;
else
 continue
fi;cd ../;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "Csv2" 10s


for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do
if [ -f "${i}/Consensus.txt" ];then cd ${i};mkdir -p subfile_fasta;bsub -n 4 -q mpi -e err -o out python ${Scriptdir}/split_to_subfiles.py Consensus.fasta subfile_fasta;cd ../;
else
 continue
fi;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "split" 20s


for k in $1;do cd ${k};for i in `echo Ig*/subfile_fasta`;do cd ${i};for j in `echo merge*.fasta`;do bsub -n 8 -q mpi -e err -o out sh ${Scriptdir}/IgBLAST4HumanBCR.sh ${j} ${Referencedir};done;cd ../../;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "IgBLAST|BCR" 30s



for k in $1;do cd ${k};for i in `echo Ig*/subfile_fasta`;do cd ${i};for j in `echo merge*.fasta`;do bsub -n 2 -q mpi -e err -o out python ${Scriptdir}/new_ParseIgBLAST20210810.py -f ${j} -i IgBLAST.${j}.m7.txt -o Seq${j}.txt;done;cd ../../;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "Parse" 10s


for k in $1;do cd ${k};for i in `echo Ig*/subfile_fasta`;do cd ${i};for j in `echo merge*.fasta`;do bsub -n 2 -q mpi -e err -o out blastn -query ${j} -out BLAST_${j}.txt -db ${Referencedir}/HumanC -outfmt "6 qseqid sseqid mismatch pident qseq sseq";done;cd ../../;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "blastn" 10s


for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -d "${i}" ];then
cd ${i};bsub -n 16 -q mpi -e err -o out python ${Scriptdir}/SumupIgblast.py Seqinfo.txt;cd ../;
else
 continue
fi;done;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "Sumup" 10s


for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -d ${i} ];then
cd ${i};bsub -n 16 -q mpi -e err -o out python ${Scriptdir}/AssembleClone.py SeqinfoPrimer.txt Clone.txt;cd ../;
else
 continue;
fi;done;cd ../;done


for k in $1;do cd ${k};bsub -n 16 -q mpi -e err  -o out python ${Scriptdir}/ReAnalyzebyC.py;cd ../;done
sh ${Scriptdir}/0-CheckJobDone.sh "ReAnalyze" 10s


for k in $1;do
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};bsub -n 8 -q mpi -e err -o out python ${Scriptdir}/AssembleClone.py Seqinfo.txt Clone.txt;cd ../;done;cd ../../;
else continue;fi;done
sh ${Scriptdir}/0-CheckJobDone.sh "Assemble" 10s


for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;bsub -n 2 -q mpi -e err -o out "python ${Scriptdir}/CalTop100.py Top100${k}.pdf";cd ../../;
else continue;fi;done


for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};bsub -n 8 -q mpi -e err -o out python ${Scriptdir}/UsageExpression.py Clone.txt;cd ../;done;cd ../../;else continue;fi;done


for k in $1;do
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};
bsub -n 8 -q mpi -e err -o out python ${Scriptdir}/VJcombination.py Clone.txt VJUE.txt;
bsub -n 8 -q mpi -e err -o out python ${Scriptdir}/VJcombination.py Clone2.txt VJUE2.txt;
cd ../;done;cd ../../;else continue;fi;done



for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;bsub -n 4 -q mpi -e err -o out python ${Scriptdir}/CompareSHMbetweenIsotype.py SHM${k}.png;cd ../../;
else continue;fi;done

:<<BLOCK
for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};bsub -n 4 -q mpi -e err -o out python ${Scriptdir}/SHMposition.py Seqinfo.txt;cd ../;done;cd ../../;else continue;fi;done


for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};bsub -n 2 -q mpi -e err -o out python ${Scriptdir}/Network.py Clone.txt ${i} Network_${k}_${i}.pdf;cd ../;done;cd ../../;else continue;fi;done
BLOCK
