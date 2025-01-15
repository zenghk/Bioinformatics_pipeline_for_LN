ScriptDir="/share/home/zenghuikun/Novaseqsamples/.Script"
#$1 the number of library in the novaseq samples

:<<!
for i in `seq 1 $1`;do mkdir -p Lib${i};done

for i in {8,};do cd Lib${i};
mv ../${i}_S*.gz ./;cd ../;
done



for i in {4,8};do cd Lib${i};bsub -n 10 -q mpi -e err -o out sh ${ScriptDir}/split.sh;cd ../;done
sh ${ScriptDir}/0-CheckJobDone.sh "split|lit|sp" 10s


for i in {4,8};do 
cd Lib${i};
num=$(($((`ls x*|wc -l`-2))/2))
ver_num=`printf "%03d" ${num}`;
for j in `seq -w 0 $ver_num`;do 
bsub -n 1 -q mpi -e err -o out python ${ScriptDir}/FindBarcodeandUMIforLibraryFree20210806.py -LibName Lib${i} -f1 x${j} -f2 x0${j} -Libconf ../conf_library.csv -PFile ${ScriptDir}/conf_seq.csv -BFile ${ScriptDir}/conf_barcode.csv -UMI5Len 12 -UMI3Len 12 -d file_${j} -o outputsummary.txt;done;
cd ../;done
sh ${ScriptDir}/0-CheckJobDone.sh "Find|Free|20210806|ary" 60s

:<<BLOCK
for i in `seq 1 $1`;do cd Lib${i};
num=$(($((`ls x*|wc -l`-2))/2))
ver_num=`printf "%03d" ${num}`;
for j in `seq -w 0 $ver_num`;do cd file_${j};bsub -n 1 -q mpi -e err -o out pear -j 4 -q 20 -f ../x${j} -r ../x0${j} -o merge;cd ../;done;
cd ../;done
sh ${ScriptDir}/0-CheckJobDone.sh "pear|merge" 60s


for i in `seq 1 $1`;do cd Lib${i};
num=$(($((`ls x*|wc -l`-2))/2))
ver_num=`printf "%03d" ${num}`;
for j in `seq -w 0 $ver_num`;do cd file_${j};bsub -n 1 -q mpi -e err -o out seqkit fx2tab merge.assembled.fastq -o Seqtab.txt;cd ../;done;
cd ../;done
sh ${ScriptDir}/0-CheckJobDone.sh "seqkit|Seqtab" 60s
BLOCK

for i in `seq {4,8}`;do 
cd Lib${i};bsub -n 20 -q fat23 -e err -o out python ${ScriptDir}/Sumupoutput.py Libinfo.txt;cd ../;done
sh ${ScriptDir}/0-CheckJobDone.sh "Sumup|Libinfo" 60s

bsub -n 1 -q mpi -e err -o out python ${ScriptDir}/showresult.py
!

mkdir -p Sample && cd Sample;
for i in {4,8};do 
bsub -n 40 -q mpi -e err -o out python ${ScriptDir}/GroupSample.py ../Lib${i}/Libinfo.txt;done;
cd ../;

#for i in `seq 1 $1`;do cd Lib${i};bsub -n 20 -q mpi -e err -o out sh ExtramergeSequence.sh;cd ../;done;


