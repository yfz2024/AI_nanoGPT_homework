


input_file_path = 'input.txt'  # 输入文件路径
output_file_path = 'output.txt'  # 输出文件路径

# 读取原文件，指定原编码
with open(input_file_path, 'r', encoding='UTF-8') as f:
    data = f.read()

# 将数据写入新文件，指定目标编码
with open(output_file_path, 'w', encoding='UTF-8') as f:
    f.write(data)

print("文件成功转换为 GBK 编码并输出为 'output_gbk.txt'")
