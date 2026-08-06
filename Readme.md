<div align="center"><img alt="image" src="https://github.com/user-attachments/assets/729a8e17-94a4-492a-8d01-c902303c06a1" width=45%/></div>

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
🚀For other modified versions of the software, please see: https://github.com/linyuiz/zgtools?tab=readme-ov-file#redesigned-software

---
# Installation
## Install with conda/mamba (Linux64) 
To install, first download the latest distribution tarball：[zgtools-EDTA_*.tar.gz](https://github.com/linyuiz/EDTA_update/releases/download/v2.3.0-5/zgtools-EDTA_v2.3.0-5.tar.gz) (not one of the Source code files!) from the github release page：https://github.com/linyuiz/EDTA_update/releases. 

```shell
##EDTA install
mamba create -n EDTA_2.3 && conda activate EDTA_2.3
wget https://github.com/oushujun/EDTA/blob/master/EDTA_2.3.yml && sed -i '1d' EDTA_2.3.yml
#or use[https://github.com/linyuiz/EDTA_update/blob/master/EDTA_2.3.yml], [https://github.com/linyuiz/EDTA_update/blob/master/EDTA_Apr13.yml]
mamba env update -f EDTA_2.3.yml
mamba install "pandas<3" tir-learner=3.0.7 repeatmodeler=2.0.5  #issue: https://github.com/oushujun/EDTA/issues/616#issuecomment-3855060533
##nextflow install
mamba create -n nextflow && conda activate nextflow
mamba install -c conda-forge -c bioconda nextflow==22.10.6

#If you do not need to run [TEtrimmer], you can skip this step.
##intasll TEtrimmer conda env 
mamba create -n TEtrimmer && conda activate TEtrimmer
mamba install -c bioconda python=3.10 samtools=1.22.1 tetrimmer=1.7.2
##git clone TEtrimmer
git clone https://github.com/qjiangzhao/TEtrimmer.git
##download Pfam data
aria2c -x 10 https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
aria2c -x 10 https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.dat.gz
gzip -d Pfam-A.hmm.gz
gzip -d Pfam-A.hmm.dat.gz
conda activate TEtrimmer
hmmpress Pfam-A.hmm

##zgtools install
tar -zxvf zgtools-EDTA_v2.3.0-5.tar.gz
cd zgtools-EDTA_v2.3.0-5 && chmod +x zg*
./zgtools EDTA_update
#You can add zgtools to your $PATH
#If zg-EDTA_update cannot be found, please edit $ZG_BIN in zgtools
```
---

# Usage

You just need to soft link zgtools to your usual bin folder such as【~/bin】, or use an absolute path such as【/project/softawre/zgtools EDTA_update】.
```shell
Usage:

        zgtools EDTA_update Run_EDTA.cfg

        Run_EDTA.cfg       --Run Config

Example1:

        zgtools EDTA_update example_cfg

Example2:

        zgtools EDTA_update Run_EDTA.cfg
```
⭐️Note regarding genome ID format: Chromosome identifiers should follow formats like Chr1, chr1, Chr1A, or ChrA1. Unanchored sequences (contigs/scaffolds) should be named using the format scaffold1, scaffold2, etc.
🚩Note that the total Threads are threads multiplied by Parallel Task Num, for example: 60 x 3 = 180 threads.    
🚩For a multi-node Slurm cluster, the EDTA conda environment must be installed in the same path on each node to ensure functionality. Alternatively, you can package all the EDTA_update scripts into a single image and distribute the Slurm tasks using that image.    
🚩If you need a reliable TE library, you can check out: https://github.com/simonorozcoarias/PanTEon/   
🚩Or you can download these two files, unzip them, and then concatenate their contents using ```cat```: ```https://www.girinst.org/server/RepBase/protected/repeatmaskerlibraries/RepBaseRepeatMaskerEdition-20181026.tar.gz``` and
```wget https://www.dfam.org/releases/current/families/Dfam-RepeatMasker.lib.gz```.        

---

# Example
1️⃣ First, run `zgtools EDTA_update example_cfg` to generate a sample configuration file, then modify the parameters below according to your needs:
```
zgtools EDTA_update example_cfg

Run_EDTA.cfg:
##Data
work_mode=local                                 #local/slurm
genome_fa=genome.fa                             #genome file
miu_rate=1.3e-8                                 #[plant]Osat:1.3e-8; Atha:7e-9
##RepeatAnno
RepeatModeler2_exist_lib=none                   #none/RM2-families.fa
EDTA_used_curated_TElib=curated.TElib.fa        #none/curated.TElib.fa
EDTA_subtask_threads=60                         #EDTA each task threads
EDTA_parallel_subtask_num=2                     #EDTA parallel subtask number
TEtrimmer_run_mode=run                          #run/skip
TEtrimmer_threads=90                            #TEtrimmer threads
TEtrimmer_path=~/software/TEtrimmer/tetrimmer/  #TEtrimmer path
TEtrimmer_pfam_db=./pfam_db                     #TEtrimmer pfam db path
whether_only_use_TEtrimmer_unknown=yes          #yes/no
RepeatMasker_threads=60                         #RepeatMasker each task threads
RepeatMasker_parallel_num=2                     #RepeatMasker parallel num
whether_count_solo_intact_LTR=run               #run/skip
##CondaEnv
EDTA_env_name=EDTA_2.3                          #EDTA env name
TEtrimmer_env_name=TEtrimmer                    #TEtrimmer env name
Nextflow_env_name=nextflow                      #Nextflow env name
conda_path=/opt/conda                           #Conda Path
```
2️⃣ Then, run `zgtools EDTA_update example_cfg`. If want to stop the job, please press `Ctrl + C`, not​ `Ctrl + Z`.            
✍️Note:​ You are free to set `TEtrimmer_run_mode`. This will create either a `run_TEtrimmer` or `skip_TEtrimmer` directory under `06.anno/`, where subsequent tasks will be executed without conflicting with other files.

# Run log

This is the command【```zgtools EDTA_update example_cfg```】runtime log:   
```
#######Run#######
1. transcode genome ...
Genome Size: 385,710,679 bp
2. denovo discover raw TEs ...
2.1. parallel discover TEs, threads: 60
[ec/86fbe9] process > discoverTE (LINE) [100%] 5 of 5 ✔
Duration    : 8h 12m 2s

2.2. deal with rawTE output ...
[a0/38a834] process > deal_with (TIR) [100%] 5 of 5 ✔
Duration    : 32m 11s

2.3. check rawTE results ...
2.4. modify LTR insert time ...
LTR insert time file: /test/02.EDTA_update/03.EDTA+TEtrimmer/output_of_EDTA_update/LTR_insert_time.txt
3. filter raw TE candidates and the make stage 1 library ...
3.1. purify raw LTR/Helitron/TIR ...
3.2. clean other TEs ...
3.3. clean LINEs and LTRs in SINEs ...
3.4. clean LTRs and nonLTRs in TIRs and Helitrons ...
3.6. check stg1 raw library ...
4. merge other TE library ...
4.1. identify remaining TEs in the filtered RM2 library ...
4.2. remove known TEs in the EDTA library ...
5. TEtrimmer generate curated TE library ...
[b6/6325d5] process > trimTE (TEtrimmer) [100%] 1 of 1 ✔
Duration    : 6h 7m 41s

6. Post-library annotate ...
6.1. split genome ...
6.2. annotate TEs using RepeatMasker with TEtrimmer results ...
[2f/89ffc9] process > AnnoTE (seq_3.fasta) [100%] 12 of 12 ✔
Duration    : 9m 20s

6.3. merge RepeatMasker output ...
6.4. make summary table for the non-overlapping annotation ...
TE anno statistic:
Class     Family         Count    bpMasked     %masked
LTR                      52,174   93,424,430   24.22
          Copia          10,046   13,627,935   3.53
          Gypsy          38,371   77,348,124   20.05
          TRIM           943      250,050      0.06
          Bel-Pao        0        0            0.00
          ERV            0        0            0.00
          unknown        1,462    1,364,722    0.35
DNA                      220,972  74,974,112   19.44
TIR       CACTA          19,586   14,327,744   3.71
          Mutator        65,084   22,868,013   5.93
          PIF-Harbinger  40,501   9,735,814    2.52
          Tc1-Mariner    31,473   6,818,056    1.77
          hAT            19,632   5,997,015    1.55
          unknown        9,470    2,215,790    0.57
NonTIR    Helitron       33,752   13,467,592   3.49
LINE                     8,132    4,795,627    1.24
          R2             0        0            0.00
          RTE            0        0            0.00
          L1             4,724    3,030,757    0.79
          unknown        3,408    1,832,455    0.48
SINE                     5,250    861,246      0.22
          tRNA           1,855    328,773      0.09
          7SL            0        0            0.00
          5S             0        0            0.00
          unknown        3,395    544,874      0.14
Unknown                  330      229,356      0.06
Total TE                 286,940  174,130,365  45.15

6.5. generate masked genome ...
6.6. calculate solo/intact LTR ratio ...
Total_solo  Total_intact  Overall_SI_ratio
1,590       93            17.10

#######Results#######
Output: /test/02.EDTA_update/03.EDTA+TEtrimmer/output_of_EDTA_update/
```
The Nextflow execution trace in the diagram has been hidden. For the specific time consumed by each process, please refer to the actual run .log file.    
⭐️The above tests were conducted on four nodes, each with 1TB of memory and 256 threads.

<img width="1481" height="531" alt="c4c7c44d-2e63-42df-bdc8-10469442ada6" src="https://github.com/user-attachments/assets/76bc64ad-9959-4515-84da-cc414f7676cb" />

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
│   ├── genome.fa.mod.EDTA.TElib.merge.fa  ⭐️ (HQlib + EDTA_denovo_lib) 
│   └── genome.fa.mod.EDTA.TElib.novel.fa  ⭐️  
├── 04.EDTA.anno
│   ├── genome.fa.mod.EDTA.TEanno.gff3  ⭐️
│   ├── genome.fa.mod.EDTA.TEanno.out   ⭐️
│   ├── genome.repeat_hard_masked.fa    ⭐️
│   └── genome.repeat_soft_masked.fa    ⭐️   
│   └── genome.fa.mod.EDTA.TEanno.sum   ⭐️
└── LTR_insert_time.txt                 ⭐️
```
