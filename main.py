import re
import sys

# 檢查命令行參數
if len(sys.argv) != 3:
    print("Usage: python main.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# 讀取raw.srt檔案
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正則表達式匹配時間戳格式
pattern = r'(\d+)\n(\d+\.\d+) --> (\d+\.\d+)\n(.*?)(?=\n\d+\n|$)'

def convert_timestamp(seconds):
    minutes, seconds = divmod(float(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}'

# 替換時間戳格式
def replace_timestamp(match):
    index = match.group(1)
    start_time = convert_timestamp(match.group(2))
    end_time = convert_timestamp(match.group(3))
    text = match.group(4)
    return f'{index}\n{start_time} --> {end_time}\n{text}\n'

# 執行替換操作
output_content = re.sub(pattern, replace_timestamp, content, flags=re.DOTALL)

# 移除最後一個空行
output_content = output_content.rstrip('\n')

# 將句點替換為逗號
output_content = output_content.replace('.', ',')

# 將轉換後的內容寫入output.srt檔案
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(output_content)