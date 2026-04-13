#!/usr/bin/env python3
"""
split_fasta.py - 将FASTA文件按每条序列拆分成单独文件
用法: python split_fasta.py input.fasta [输出目录]
"""

import sys
import os
from pathlib import Path

def split_fasta(input_file, output_dir="split_sequences"):
    """
    将FASTA文件中的每条序列拆分成单独文件
    """
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    sequence_count = 0
    current_header = None
    current_sequence = []
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('>'):
                # 保存上一条序列
                if current_header:
                    sequence_count += 1
                    output_file = os.path.join(output_dir, f"seq_{sequence_count}.fasta")
                    with open(output_file, 'w') as out:
                        out.write(f"{current_header}\n")
                        out.write(''.join(current_sequence) + '\n')
                    print(f"已写入: {output_file}")
                
                # 开始新序列
                current_header = line
                current_sequence = []
            else:
                current_sequence.append(line)
        
        # 保存最后一条序列
        if current_header:
            sequence_count += 1
            output_file = os.path.join(output_dir, f"seq_{sequence_count}.fasta")
            with open(output_file, 'w') as out:
                out.write(f"{current_header}\n")
                out.write(''.join(current_sequence) + '\n')
            print(f"已写入: {output_file}")
    
    print(f"\n完成！共拆分 {sequence_count} 条序列到目录: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python split_fasta.py <input.fasta> [output_dir]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "split_sequences"
    
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)
    
    split_fasta(input_file, output_dir)
