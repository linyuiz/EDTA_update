# EDTA_update -- This is a modified version of EDTA
For those working on genome transposon annotation, EDTA (Extensive de novo TE Annotator) is a familiar name. It is currently recognized as one of the most accurate annotation pipelines, but the original workflow often presents several frustrating issues during execution:  

**1️⃣Efficiency bottleneck**: Serial execution leads to low CPU utilization, such as in the initial rawTE search phase.  

**2️⃣Catastrophic crashes**: After running for days, it may suddenly throw an error with no solution, even though some errors can be ignored without affecting the results.  

**3️⃣Black-box operations**: A tangled mix of lengthy Shell and Perl commands makes parameter adjustments cumbersome and the code difficult to read.  

To address these problems, we recently undertook a complete overhaul of EDTA—introducing the Nextflow workflow engine alongside Shell scripts, breathing new life into this well-established software.

⭐️If you encounter any issues, feel free to ask in the issue section. Please also support the original authors. **If you use EDTA, kindly cite it:**   

Ou S., Su W., Liao Y., Chougule K., Agda J. R. A., Hellinga A. J., Lugo C. S. B., Elliott T. A., Ware D., Peterson T., Jiang N.✉, Hirsch C. N.✉ and Hufford M. B.✉ (2019). Benchmarking Transposable Element Annotation Methods for Creation of a Streamlined, Comprehensive Pipeline. Genome Biol. 20(1): 275. 

# Installation
### Install with conda/mamba (Linux64) 
To install, first download the latest distribution tarball：zgtools-EDTA_*.tar.gz (not one of the Source code files!) from the github release page：https://github.com/linyuiz/EDTA_update/releases. 
```shell

mamba create -n EDTA_2.3 && conda activate EDTA_2.3
wget https://github.com/oushujun/EDTA/blob/master/EDTA_2.3.yml && sed -i '1d' EDTA_2.3.yml
mamba env update -f EDTA_2.3.yml
```

# Usage

You just need to soft link zgtools to your usual bin folder such as【~/bin】, or use an absolute path such as【/project/softawre/zgtools EDTA_update】.
```shell
Usage:

	zgtools EDTA_update genome.fa 60 5 RepeatModeler2-families.fa curated.TElib.fa slurm EDTA_2.3 /opt/conda

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

	zgtools EDTA_update genome.fa 60 2 none none local EDTA_2.3 /opt/conda

Exmaple2:

	zgtools EDTA_update genome.fa 60 5 none curated.TElib.fa slurm EDTA_2.3 /opt/conda

```
Note that the total Threads are threads multiplied by Parallel Task Num, for example: 60 x 3 = 180 threads.

# Run log

This is the command【zgtools EDTA_update genome.fa 7e-9 60 5 RM2-families.fa Plant.TElib.fa slurm EDTA_2.3 /opt/conda】runtime log:   
<img alt="image" src="https://github.com/user-attachments/assets/accae835-723c-4b9c-a9c4-64fd88c8f4f0" width=70%/>

# Main output


