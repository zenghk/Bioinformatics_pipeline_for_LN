Scriptdir=`pwd`
Referencedir="${Scriptdir/Reference"


for k in $1;do cd ${k};python ${Scriptdir}/Rename.py;cd ../;done



for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -f $i.txt ];then
python ${Scriptdir}/GetConsensus_V2.py ${i}.txt 5 ${i}/Consensus.txt;
fi;done;cd ../;done



for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -f "${i}/Consensus.txt" ];then 
cd ${i};
python ${Scriptdir}/Csv2fastaofConseusns.py Consensus.txt Consensus.fasta;
else
 continue
fi;cd ../;done;cd ../;done



for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do
if [ -f "${i}/Consensus.txt" ];then cd ${i};mkdir -p subfile_fasta;python ${Scriptdir}/split_to_subfiles.py Consensus.fasta subfile_fasta;cd ../;
else
 continue
fi;done;cd ../;done



for k in $1;do cd ${k};for i in `echo Ig*/subfile_fasta`;do cd ${i};for j in `echo merge*.fasta`;do sh ${Scriptdir}/IgBLAST4HumanBCR.sh ${j} ${Referencedir};done;cd ../../;done;cd ../;done




for k in $1;do cd ${k};for i in `echo Ig*/subfile_fasta`;do cd ${i};for j in `echo merge*.fasta`;do python ${Scriptdir}/new_ParseIgBLAST.py -f ${j} -i IgBLAST.${j}.m7.txt -o Seq${j}.txt;done;cd ../../;done;cd ../;done


for k in $1;do cd ${k};for i in `echo Ig*/subfile_fasta`;do cd ${i};for j in `echo merge*.fasta`;do blastn -query ${j} -out BLAST_${j}.txt -db ${Referencedir}/HumanC -outfmt "6 qseqid sseqid mismatch pident qseq sseq";done;cd ../../;done;cd ../;done



for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -d "${i}" ];then
cd ${i};
python ${Scriptdir}/SumupIgblast.py Seqinfo.txt;cd ../;
else
 continue
fi;done;cd ../;done



for k in $1;do cd ${k};for i in {IgM,IgD,IgG1,IgG2,IgA,IgE,IgK,IgL};do 
if [ -d ${i} ];then
cd ${i};python ${Scriptdir}/AssembleClone.py SeqinfoPrimer.txt Clone.txt;cd ../;
else
 continue;
fi;done;cd ../;done


for k in $1;do cd ${k};python ${Scriptdir}/ReAnalyzebyC.py;cd ../;done



for k in $1;do
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};python ${Scriptdir}/AssembleClone.py Seqinfo.txt Clone.txt;cd ../;done;cd ../../;
else continue;fi;done



for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;python ${Scriptdir}/CalTop100.py Top100${k}.pdf;cd ../../;
else continue;fi;done


for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};python ${Scriptdir}/UsageExpression.py Clone.txt;cd ../;done;cd ../../;else continue;fi;done


for k in $1;do
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};
python ${Scriptdir}/VJcombination.py Clone.txt VJUE.txt;
cd ../;done;cd ../../;else continue;fi;done



for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;python ${Scriptdir}/CompareSHMbetweenIsotype.py SHM${k}.png;cd ../../;
else continue;fi;done


for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};python ${Scriptdir}/SHMposition.py Seqinfo.txt;cd ../;done;cd ../../;else continue;fi;done


for k in $1;do 
if [ -d "${k}/Analysis" ];then cd ${k}/Analysis;for i in `echo IG*`;do cd ${i};python ${Scriptdir}/Network.py Clone.txt ${i} Network_${k}_${i}.pdf;cd ../;done;cd ../../;else continue;fi;done

