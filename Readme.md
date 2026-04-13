<div align="center"><img src="https://s2.loli.net/2025/01/10/WzwaHxSGMrKl8st.png" alt="Your Image Description" /></div>

---
# EDTA_update -- This is a modified version of EDTA
For those working on genome transposon annotation, EDTA (Extensive de novo TE Annotator) is a familiar name. It is currently recognized as one of the most accurate annotation pipelines, but the original workflow often presents several frustrating issues during execution:  

**1️⃣Efficiency bottleneck**: Serial execution leads to low CPU utilization, such as in the initial rawTE search phase.  

**2️⃣Catastrophic crashes**: After running for days, it may suddenly throw an error with no solution, even though some errors can be ignored without affecting the results.  

**3️⃣Black-box operations**: A tangled mix of lengthy Shell and Perl commands makes parameter adjustments cumbersome and the code difficult to read.  

To address these problems, we recently undertook a complete overhaul of EDTA—introducing the Nextflow workflow engine alongside Shell scripts, breathing new life into this well-established software.

⭐️If you encounter any issues, feel free to ask in the issue section. Please also support the original authors. **If you use EDTA, kindly cite it:**   

Ou S., Su W., Liao Y., Chougule K., Agda J. R. A., Hellinga A. J., Lugo C. S. B., Elliott T. A., Ware D., Peterson T., Jiang N.✉, Hirsch C. N.✉ and Hufford M. B.✉ (2019). Benchmarking Transposable Element Annotation Methods for Creation of a Streamlined, Comprehensive Pipeline. Genome Biol. 20(1): 275. 

---

# Other modified versions of the software
🚀For other modified versions of the software, please see: https://github.com/linyuiz/zgtools?tab=readme-ov-file#%E6%94%B9%E7%89%88%E8%BD%AF%E4%BB%B6

---
# Installation
### Install with conda/mamba (Linux64) 
To install, first download the latest distribution tarball：[zgtools-EDTA_*.tar.gz](https://github.com/linyuiz/EDTA_update/releases/download/v2.3.0-2/zgtools-EDTA_v2.3.0-2.tar.gz) (not one of the Source code files!) from the github release page：https://github.com/linyuiz/EDTA_update/releases. 
```shell
##EDTA install
mamba create -n EDTA_2.3 && conda activate EDTA_2.3
wget https://github.com/oushujun/EDTA/blob/master/EDTA_2.3.yml && sed -i '1d' EDTA_2.3.yml
mamba env update -f EDTA_2.3.yml
##nextflow install
mamba create -n nextflow && conda activate nextflow
mamba install -c conda-forge -c bioconda nextflow==22.10.6
##zgtools install
tar -zxvf zgtools-EDTA_v2.3.0-2.tar.gz
cd zgtools-EDTA_v2.3.0-2 && chmod +x zg*
./zgtools EDTA_update
```
---

# Usage

You just need to soft link zgtools to your usual bin folder such as【~/bin】, or use an absolute path such as【/project/softawre/zgtools EDTA_update】.
```shell
Usage:

	zgtools EDTA_update genome.fa 1.3e-8 60 5 RepeatModeler2-families.fa curated.TElib.fa slurm EDTA_2.3 /opt/conda

    genomoe.fa            --Genome File
	1.3e-8                --Neutral mutation rate(Example: 1.3e-8 from rice, 7e-9 from atha)
	60                    --Each Task Threads
	5                     --Parallel Task Num
	*-families.fa         --RepeatModeler2 Library(default: none)
	curated.TElib.fa      --Input Curated TE Library(default: none)
	slurm                 --Local/Slurm Mode(local/slurm)
	EDTA_2.3              --Conda Env Name
	/opt/conda            --Conda Path(Must Have: your_path/bin/activate)

Example1:

	zgtools EDTA_update genome.fa 1.3e-8 60 2 none none local EDTA_2.3 /opt/conda

Exmaple2:

	zgtools EDTA_update genome.fa 1.3e-8 60 5 none curated.TElib.fa slurm EDTA_2.3 /opt/conda

```
🚩Note that the total Threads are threads multiplied by Parallel Task Num, for example: 60 x 3 = 180 threads.    
🚩For a multi-node Slurm cluster, the EDTA conda environment must be installed in the same path on each node to ensure functionality. Alternatively, you can package all the EDTA_update scripts into a single image and distribute the Slurm tasks using that image.    
🚩If you need a reliable TE library, you can check out: https://github.com/simonorozcoarias/PanTEon/  

---

# Run log

This is the command【```zgtools EDTA_update genome.fa 7e-9 60 5 RM2-families.fa Plant.TElib.fa slurm EDTA_2.3 /opt/conda```】runtime log:   
<img alt="image" src="https://github.com/user-attachments/assets/b62fa05a-2e67-4107-b064-6c0e4e7b4bc3" width=70%/>   
The Nextflow execution trace in the diagram has been hidden. For the specific time consumed by each process, please refer to the actual run .log file.
The above tests were conducted on four nodes, each with 1TB of memory and 256 threads.

---

# Main output
The output EDTA.TElib.fa is recommended to be adjusted using ```TEtrimmer``` for better TE annotation results.
The output files are basically consistent with the EDTA output results, and the ⭐️-marked files are those commonly used by most people.
```
├── 01.EDTA.raw
│   ├── genome.fa.mod.EDTA.intact.raw.fa        ⭐️
│   ├── genome.fa.mod.EDTA.intact.raw.gff3      ⭐️
│   ├── genome.fa.mod.Helitron.intact.raw.bed
│   ├── genome.fa.mod.Helitron.intact.raw.fa
│   ├── genome.fa.mod.Helitron.intact.raw.fa.anno.list
│   ├── genome.fa.mod.Helitron.intact.raw.gff3
│   ├── genome.fa.mod.LINE.raw.fa
│   ├── genome.fa.mod.LTR.intact.raw.fa
│   ├── genome.fa.mod.LTR.intact.raw.fa.anno.list
│   ├── genome.fa.mod.LTR.intact.raw.gff3
│   ├── genome.fa.mod.LTR.raw.fa
│   ├── genome.fa.mod.RM2.fa
│   ├── genome.fa.mod.SINE.raw.fa
│   ├── genome.fa.mod.TIR.intact.raw.bed
│   ├── genome.fa.mod.TIR.intact.raw.fa
│   ├── genome.fa.mod.TIR.intact.raw.fa.anno.list
│   └── genome.fa.mod.TIR.intact.raw.gff3
├── 02.EDTA.combine
│   ├── genome.fa.mod.EDTA.fa.stg1
│   ├── genome.fa.mod.EDTA.intact.fa.cln
│   ├── genome.fa.mod.Helitron.intact.raw.fa.cln
│   ├── genome.fa.mod.Helitron.intact.raw.fa.int.cln
│   ├── genome.fa.mod.LINE.raw.fa
│   ├── genome.fa.mod.LTR.intact.raw.fa.cln
│   ├── genome.fa.mod.LTR.raw.fa.cln
│   ├── genome.fa.mod.SINE.raw.fa.cln
│   ├── genome.fa.mod.TIR.intact.raw.fa.cln
│   └── genome.fa.mod.TIR.intact.raw.fa.int.cln
├── 03.EDTA.final
│   ├── genome.fa.mod.EDTA.TElib.fa
│   ├── genome.fa.mod.EDTA.TElib.merge.fa(HQlib+EDTA_denovolib)  ⭐️
│   └── genome.fa.mod.EDTA.TElib.novel.fa  ⭐️  
├── 04.EDTA.anno
│   ├── genome.fa.mod.EDTA.TEanno.gff3  ⭐️
│   ├── genome.fa.mod.EDTA.TEanno.out   ⭐️
│   └── genome.fa.mod.EDTA.TEanno.sum   ⭐️
└── LTR_insert_time.txt                 ⭐️
```
