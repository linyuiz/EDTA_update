#!/usr/bin/env nextflow
//nextflow.enable.dsl=2
// 读取任务ID文件，创建任务通道
Channel.fromPath("${params.task_file}")
      .splitText()
      .map { it.trim() }
      .filter { it.length() > 0 }
      .toSortedList()  // 关键修改：排序
      .flatten()
      .set { task_id }

// 定义执行任务的过程
process SplitTask {
    tag "${task_id}"
    maxForks params.max_parallel
    
    publishDir "${params.input_dir}/${task_id}", mode: 'copy', pattern: "${params.script_name}.done"

    input:
    val task_id

    output:
    path("${params.script_name}.done") optional true

    script:
    """
    cd ${params.input_dir}/${task_id}
    
    if [ ! -e ${params.script_name}.done ]; then
        echo "Starting task: ${task_id}"
        bash ${params.script_name} 1>${params.script_name}.log 2>${params.script_name}.err
        if [ \$? -eq 0 ]; then
            touch ${params.script_name}.done
            echo "Finished task: ${task_id}"
        else
            echo "Task failed: ${task_id}"
            exit 1
        fi
    else
        echo "Task ${task_id} already completed, skipping"
    fi
    """
}

// 工作流
workflow {
    SplitTask(task_id)
}
