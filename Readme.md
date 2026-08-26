# EDTA-mod -- This is a modified version of EDTA
For those working on genome transposon annotation, EDTA (Extensive de novo TE Annotator) is a familiar name. It is currently recognized as one of the most accurate annotation pipelines, but the original workflow often presents several frustrating issues during execution:  

**1️⃣Efficiency bottleneck**: Serial execution leads to low CPU utilization, such as in the initial rawTE search phase.  

**2️⃣Catastrophic crashes**: After running for days, it may suddenly throw an error with no solution, even though some errors can be ignored without affecting the results.  

**3️⃣Black-box operations**: A tangled mix of lengthy Shell and Perl commands makes parameter adjustments cumbersome and the code difficult to read.  

To address these problems, we recently undertook a complete overhaul of EDTA—introducing the Nextflow workflow engine alongside Shell scripts, breathing new life into this well-established software.

⭐️If you encounter any issues, feel free to ask in the issue section. Please also support the original authors. **If you use EDTA, kindly cite it:**   

Ou S., Su W., Liao Y., Chougule K., Agda J. R. A., Hellinga A. J., Lugo C. S. B., Elliott T. A., Ware D., Peterson T., Jiang N.✉, Hirsch C. N.✉ and Hufford M. B.✉ (2019). Benchmarking Transposable Element Annotation Methods for Creation of a Streamlined, Comprehensive Pipeline. Genome Biol. 20(1): 275. 

---

# Other modified versions of the software
<div align="center"><img alt="image" src="https://github.com/user-attachments/assets/729a8e17-94a4-492a-8d01-c902303c06a1" width=30%/></div>

⭐️ For the modified version of annotation tool `EviAnn`, please visit: [EviAnn-mod](https://github.com/linyuiz/EviAnn-mod) (Not recommended for now, currently under upgrade)  

⭐️ For the modified version of TE transposon annotation tool `EDTA`, please visit: [EDTA-mod](https://github.com/linyuiz/EDTA-mod) (Beta version)  

⭐️ For the modified version of scaffolding tool `C-Phasing`, please visit: [CPhasing-mod](https://github.com/linyuiz/CPhasing-mod) (Beta version)   

---

# Installation
## Install with conda/mamba (Linux64) 
To install, first download the latest distribution tarball：[zgtools-EDTA_*.tar.gz](https://github.com/linyuiz/EDTA-mod/releases/download/v2.3.0-5/zgtools-EDTA_v2.3.0-5.tar.gz) (not one of the Source code files!) from the github release page：https://github.com/linyuiz/EDTA-mod/releases. 

```shell
#1. EDTA install
mamba create -n EDTA_2.3 && conda activate EDTA_2.3
wget https://github.com/oushujun/EDTA/blob/master/EDTA_2.3.yml && sed -i '1d' EDTA_2.3.yml
#or use [https://github.com/linyuiz/EDTA-mod/blob/master/EDTA_Apr13.yml], [https://github.com/linyuiz/EDTA-mod/blob/master/EDTA_2.3.yml]
mamba env update -f EDTA_2.3.yml
mamba install "pandas<3" tir-learner=3.0.7 repeatmodeler=2.0.5  #issue: https://github.com/oushujun/EDTA/issues/616#issuecomment-3855060533
If your mamba exit with dependency coflicts, you may check out your ~/.condarc file and make sure it use "flexible" solve:
channels:  
  - conda-forge  
  - bioconda  
channel_priority: flexible

#2. nextflow install
mamba create -n nextflow && conda activate nextflow
mamba install -c conda-forge -c bioconda nextflow==22.10.6

#3. If you do not need to run [TEtrimmer], you can skip this step.
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

#4. zgtools install
tar -zxvf zgtools-EDTA_v2.3.0-5.tar.gz
cd zgtools-EDTA_v2.3.0-5 && chmod +x zg*
./zgtools EDTA-mod
#You can add zgtools to your $PATH
#If zg-EDTA-mod cannot be found, please edit $ZG_BIN in zgtools
```
---

# Usage

You just need to soft link zgtools to your usual bin folder such as【~/bin】, or use an absolute path such as【/project/softawre/zgtools EDTA-mod】.
```shell
Usage:

        zgtools EDTA-mod Run_EDTA.cfg

        Run_EDTA.cfg       --Run Config

Example1:

        zgtools EDTA-mod example_cfg

Example2:

        zgtools EDTA-mod Run_EDTA.cfg
```
⭐️Note regarding genome ID format: Chromosome identifiers should follow formats like Chr1, chr1, Chr1A, or ChrA1. Unanchored sequences (contigs/scaffolds) should be named using the format scaffold1, scaffold2, etc.
🚩Note that the total Threads are threads multiplied by Parallel Task Num, for example: 60 x 3 = 180 threads.    
🚩For a multi-node Slurm cluster, the EDTA conda environment must be installed in the same path on each node to ensure functionality. Alternatively, you can package all the EDTA-mod scripts into a single image and distribute the Slurm tasks using that image.    
🚩If you need a reliable TE library, you can check out: https://github.com/simonorozcoarias/PanTEon/   
🚩Or you can download these two files, unzip them, and then concatenate their contents using ```cat```: ```https://www.girinst.org/server/RepBase/protected/repeatmaskerlibraries/RepBaseRepeatMaskerEdition-20181026.tar.gz``` and
```wget https://www.dfam.org/releases/current/families/Dfam-RepeatMasker.lib.gz```.        

---

# Example
1️⃣ First, run `zgtools EDTA-mod example_cfg` to generate a sample configuration file, then modify the parameters below according to your needs:
```
zgtools EDTA-mod example_cfg

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
2️⃣ Then, run `zgtools EDTA-mod Run_EDTA.cfg`. If want to stop the job, please press `Ctrl + C`, not​ `Ctrl + Z`.            
✍️Note:​ You are free to set `TEtrimmer_run_mode`. This will create either a `run_TEtrimmer` or `skip_TEtrimmer` directory under `06.anno/`, where subsequent tasks will be executed without conflicting with other files.

# Run log

This is the command【```zgtools EDTA-mod Run_EDTA.cfg```】runtime log:   
```
#######Data#######
##Data
☆data_work_mode=slurm                           #local or slurm
☆data_genome_fa=NIP.fa                          #genome file
☆data_miu_rate=1.3e-8                           #[plant]Osat:1.3e-8; Atha:7e-9
☆data_RepeatModeler2_exist_lib=none             #none/RM2-families.fa
☆data_TEtrimmer_run_mode=yes                    #whether run TEtrimmer(yes|no)
☆data_curated_TElib=curated.TElib.fa            #none|curated.TElib.fa
##EDTA
EDTA_subtask_threads=30                          #EDTA each task threads
EDTA_parallel_subtask_num=5                      #EDTA parallel subtask number
##TEtrimmer
TEtrimmer_threads=60                             #TEtrimmer threads
☆whether_only_use_TEtrimmer_unknown=no          #yes/no
##RepeatMasker
RepeatMasker_threads=30                          #RepeatMasker each task threads
RepeatMasker_parallel_num=5                      #RepeatMasker parallel num
whether_count_solo_intact_LTR=yes                #whether count S/I rate(yes|no)
##CondaEnv
conda_path=~/miniconda3                          #conda path
EDTA_env_name=EDTA_2.3                           #EDTA env name
nextflow_env_name=nextflow                       #nextflow env name
TEtrimmer_env_name=TEtrimmer                     #TEtrimmer env name
TEtrimmer_path=~/software/TEtrimmer/tetrimmer/   #TEtrimmer path
TEtrimmer_pfam_db=~/software/TEtrimmer/pfam_db/  #TEtrimmer pfam db path

#######Run#######
1. transcode genome ...
Genome Size: 385,710,679 bp
2. denovo discover raw TEs ...
2.1. parallel discover TEs, each task threads: 30 ...
[ec/86fbe9] process > discoverTE (LINE) [100%] 4 of 4 ✔
Duration    : 11h 12m 2s

2.2. deal with rawTE output ...
[a0/38a834] process > deal_with (TIR) [100%] 5 of 5 ✔
Duration    : 32m 11s

2.3. check rawTE results ...
2.4. modify LTR insert time ...
LTR insert time file: /project501/zhangyaolong/01.project/18.EDTA_update/output_of_EDTA-mod/LTR_insert_time.txt
3. filter raw TE candidates and the make stage 1 library ...
3.1. purify raw LTR/Helitron/TIR ...
3.2. clean other TEs ...
[fd/aacb97] process > FilterTE (purify_LTRint) [100%] 2 of 2 ✔
Duration    : 9m 37s

3.3. clean LINEs and LTRs in SINEs ...
[b5/a4e4c6] process > FilterTE (clean_SINE) [100%] 1 of 1 ✔
Duration    : 7m 16s

3.4. clean LTRs and nonLTRs in TIRs and Helitrons ...
[ca/eca345] process > FilterTE (clean_otherTE) [100%] 1 of 1 ✔
Duration    : 12m 22s

3.5. cluster TIRs and Helitrons and make stg1 raw library ...
[b2/8ff066] process > FilterTE (cleanup_nested) [100%] 1 of 1 ✔
Duration    : 1h 16s

3.6. check stg1 raw library ...
4. merge other TE library ...
4.1. identify remaining TEs in the filtered RM2 library ...
[80/2d02b9] process > MergeTE (clean_RM2) [100%] 1 of 1 ✔
Duration    : 1h 42m 49s

4.2. remove known TEs in the EDTA library ...
[6d/b24698] process > MergeTE (clean_HQlib) [100%] 1 of 1 ✔
Duration    : 11m 12s

5. skip TEtrimmer pipeline ~
6. Post-library annotate ...
6.1. split genome ...
6.2. annotate TEs using RepeatMasker with EDTA results ...
[10/19465d] process > AnnoTE (seq_1.fasta)  [100%] 12 of 12 ✔
Duration    : 1h 50m 8s

6.3. merge RepeatMasker output ...
[58/b4e22a] process > AnnoTE (merge_RMout) [100%] 1 of 1 ✔
Duration    : 1m 11s

6.4. make summary table for the non-overlapping annotation ...
TE anno statistic:
Class     Family         Count    bpMasked     %masked
LTR                      65,073   96,368,187   24.98
          Copia          13,285   14,452,400   3.75
          Gypsy          46,460   80,061,806   20.76
          TRIM           1,213    220,677      0.06
          Bel-Pao        14       6,334        0.00
          ERV            396      53,888       0.01
          unknown        2,680    910,113      0.24
DNA                      304,796  104,385,152  27.06
TIR       CACTA          28,607   18,151,556   4.71
          Mutator        70,245   25,897,029   6.71
          PIF-Harbinger  43,830   10,485,982   2.72
          Tc1-Mariner    58,214   15,184,198   3.94
          hAT            24,971   7,334,824    1.90
          unknown        11,953   2,879,052    0.75
NonTIR    Helitron       60,881   25,976,035   6.73
LINE                     15,249   7,115,770    1.84
          R2             642      57,728       0.01
          RTE            622      100,561      0.03
          L1             7,663    4,330,360    1.12
          unknown        4,555    2,417,750    0.63
SINE                     7,012    1,401,742    0.36
          tRNA           1,464    234,088      0.06
          7SL            0        0            0.00
          5S             0        0            0.00
          unknown        5,434    1,175,809    0.30
Unknown                  2,055    671,718      0.17
Total TE                 398,701  212,330,356  55.05

6.5. generate masked genome ...
6.6. skipped calculate solo/intact LTR ratio ...

#######Results#######
Output: /EDTA/output_of_EDTA-mod/
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
