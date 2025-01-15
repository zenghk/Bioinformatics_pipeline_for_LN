ScriptDir="/share/home/zenghuikun/Novaseqsamples/.Script"
#$1 the number of library in the novaseq samples

:<<!
for i in `seq 1 $1`;do mkdir -p Lib${i};done

for i in {8,};do cd Lib${i};
mv ../${i}_S*.gz ./;cd ../;
done



for i in {4,8};do cd Lib${i};
sh ${ScriptDir}/split.sh;cd ../;done



for i in {4,8};do 
cd Lib${i};
num=$(($((`ls x*|wc -l`-2))/2))
ver_num=`printf "%03d" ${num}`;
for j in `seq -w 0 $ver_num`;do 
python ${ScriptDir}/FindBarcodeandUMIforLibraryFree20210806.py -LibName Lib${i} -f1 x${j} -f2 x0${j} -Libconf ../conf_library.csv -PFile ${ScriptDir}/conf_seq.csv -BFile ${ScriptDir}/conf_barcode.csv -UMI5Len 12 -UMI3Len 12 -d file_${j} -o outputsummary.txt;done;
cd ../;done


:<<BLOCK
for i in `seq 1 $1`;do cd Lib${i};
num=$(($((`ls x*|wc -l`-2))/2))
ver_num=`printf "%03d" ${num}`;
for j in `seq -w 0 $ver_num`;do cd file_${j};
pear -j 4 -q 20 -f ../x${j} -r ../x0${j} -o merge;cd ../;done;
cd ../;done



for i in `seq 1 $1`;do cd Lib${i};
num=$(($((`ls x*|wc -l`-2))/2))
ver_num=`printf "%03d" ${num}`;
for j in `seq -w 0 $ver_num`;do cd file_${j};
seqkit fx2tab merge.assembled.fastq -o Seqtab.txt;cd ../;done;
cd ../;done


for i in `seq {4,8}`;do 
cd Lib${i};
python ${ScriptDir}/Sumupoutput.py Libinfo.txt;cd ../;done



python ${ScriptDir}/showresult.py


mkdir -p Sample && cd Sample;
for i in {4,8};do 
python ${ScriptDir}/GroupSample.py ../Lib${i}/Libinfo.txt;done;
cd ../;

for i in `seq 1 $1`;do cd Lib${i};sh ExtramergeSequence.sh;cd ../;done;


