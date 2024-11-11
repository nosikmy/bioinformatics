import subprocess
from redun import task, File


@task()
def get_fastq(fastq):
    subprocess.run(f"{fastq.path}", shell=True)
    return File(f"{fastq.path}")


@task()
def minimap_process(fastq, reference):
    subprocess.run(f"minimap2/minimap2 -d ref_output.mmi {reference.path}", shell=True)
    subprocess.run(f"minimap2/minimap2 -a ref_output.mmi {fastq.path} > alignment.sam", shell=True)
    return File("alignment.sam")


@task()
def samtools_view(sam):
    subprocess.run(f"samtools view -bS {sam.path} > alignment.bam", shell=True)
    return File("alignment.bam")


@task()
def samtools_flagstat(bam):
    subprocess.run(f"samtools flagstat {bam.path} > flagstat_output.txt", shell=True)
    return File("flagstat_output.txt")


@task()
def parse_percent(stats):
    with open(stats.path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if " mapped (" in line:
                percent_mapped = line.split("(")[1].split("%")[0]
                with open("percent.txt", 'w') as percent_file:
                    percent_file.write(percent_mapped)
    return File("percent.txt")


@task()
def handle_results(percent_txt, bam, reference):
    with open(percent_txt.path, 'r') as f:
        percent_value = float(f.read())

    if percent_value < 90:
        print("not OK")
        return None
    else:
        print("OK")
        subprocess.run(f"samtools sort {bam.path} > alignment.sorted.bam", shell=True)
        subprocess.run(f"freebayes -f {reference.path} -b alignment.sorted.bam > result.vcf", shell=True)
        return File("result.vcf")


@task()
def workflow():
    fastq = File("DRR614460.fastq")
    reference = File("reference.fna")
    fastqc_html = get_fastq(fastq)
    sam = minimap_process(fastq, reference)
    bam = samtools_view(sam)
    stats = samtools_flagstat(bam)
    percent = parse_percent(stats)
    result_vcf = handle_results(percent, bam, reference)
    return result_vcf
