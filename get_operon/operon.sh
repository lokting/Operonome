#!/bin/bash

# 运行 Python 脚本并将输出重定向到 /dev/null


set -e #遇到错误立即退出不再继续运行

output_dir="tmp_output"
mkdir -p "$output_dir" # 创建临时输出目录

# 你的其他脚本内容...


# 获取用户输入的参数
# echo "Please enter SRP IDs (separated by space):"
# read -a srp_ids   # 使用数组来接收多个 SRP ID

# echo "Please enter the module option (yes, no, or reverse):"
# read module

# 运行 0-0.HTseq_count.py
# echo "Running 0-0.HTseq_count.py with SRP IDs and module..."
# python3 code/0-0.HTseq_count.py "${srp_ids[@]}" --module "$module"
# echo "Finished 0-0.HTseq_count.py"

# 运行 0-1.gbff_to_excel.py
echo "Running 0-1.gbff_to_excel.py..."
python3 code/0-1.gbff_to_excel.py 1>/dev/null
echo "Finished 0-1.gbff_to_excel.py"

# 运行 1.gff_to_excel.py
echo "Running 1.gff_to_excel.py..."
python3 code/1.gff_to_excel.py 1>/dev/null
echo "Finished 1.gff_to_excel.py"

# 运行 2.count_file.py
echo "Running 2.count_file.py..."
python3 code/2.count_file.py 1>/dev/null
echo "Finished 2.count_file.py"

# 运行 3.get_intergenegap.py
echo "Running 3.get_intergenegap.py..."
python3 code/3.get_intergenegap.py 1>/dev/null
echo "Finished 3.get_intergenegap.py"

# 运行 4-0.get_operon.py
echo "Running 4-0.get_operon.py..."
python3 code/4-0.get_operon.py 1>/dev/null
echo "Finished 4-0.get_operon.py"

# 运行 4-1.get_operon_function.py
echo "Running 4-1.get_operon_function.py..."
python3 code/4-1.get_operon_function.py 1>/dev/null
echo "Finished 4-1.get_operon_function.py"