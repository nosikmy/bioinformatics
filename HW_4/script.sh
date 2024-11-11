samtools view -bS alignment.sam > alignment.bam
samtools flagstat alignment.bam > flagstat_output.txt

mapped=$(grep -oP '\d+\.\d+%' flagstat_output.txt | head -1 | tr -d '%')



if (( $(echo "$mapped >= 90" | bc -l) )); then
    echo "not OK"
else
    echo "not OK"
fi
