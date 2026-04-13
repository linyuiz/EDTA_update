# EDTA_update -- This is a modified version of EDTA
For those working on genome transposon annotation, EDTA (Extensive de novo TE Annotator) is a familiar name. It is currently recognized as one of the most accurate annotation pipelines, but the original workflow often presents several frustrating issues during execution:  

**Efficiency bottleneck**: Serial execution leads to low CPU utilization, such as in the initial rawTE search phase.  

**Catastrophic crashes**: After running for days, it may suddenly throw an error with no solution, even though some errors can be ignored without affecting the results.  

**Black-box operations**: A tangled mix of lengthy Shell and Perl commands makes parameter adjustments cumbersome and the code difficult to read.  

To address these problems, I recently undertook a complete overhaul of EDTA—introducing the Nextflow workflow engine alongside Shell scripts, breathing new life into this well-established software.

If you encounter any issues, feel free to ask in the issue section. Please also support the original authors. If you use EDTA, kindly cite it:   

Ou S., Su W., Liao Y., Chougule K., Agda J. R. A., Hellinga A. J., Lugo C. S. B., Elliott T. A., Ware D., Peterson T., Jiang N.✉, Hirsch C. N.✉ and Hufford M. B.✉ (2019). Benchmarking Transposable Element Annotation Methods for Creation of a Streamlined, Comprehensive Pipeline. Genome Biol. 20(1): 275. 
