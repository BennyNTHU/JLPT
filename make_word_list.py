import sys

def kata_to_hira(s):
    result = ''
    for ch in s:
        code = ord(ch)
        # 将片假名转换为平假名
        if 0x30A1 <= code <= 0x30F4:
            result += chr(code - 0x60)
        else:
            result += ch
    return result

def main():
    if len(sys.argv) != 4:
        print("用法: python 程式名稱 txt檔案名稱 csv輸出檔案名稱 md輸出檔案名稱")
        sys.exit(1)

    input_txt = sys.argv[1]
    output_csv = sys.argv[2]
    output_md = sys.argv[3]

    entries = []

    with open(input_txt, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            word = ''
            reading = ''
            translation = ''
            if '（' in line and '）' in line:
                idx1 = line.find('（')
                idx2 = line.find('）')
                word = line[:idx1].strip()
                reading = line[idx1+1:idx2].strip()
                translation = line[idx2+1:].strip()
            else:
                parts = line.split(' ', 1)
                word = parts[0].strip()
                translation = parts[1].strip() if len(parts) > 1 else ''
                reading = ''  # 没有读音的情况，读音保持为空
            # 去除每个字段中的空格
            word = word.replace(' ', '')
            reading = reading.replace(' ', '')
            translation = translation.replace(' ', '')
            # 为排序目的，将读音转换为平假名；如果读音为空，使用单词本身
            if reading:
                sorting_reading = kata_to_hira(reading)
            else:
                sorting_reading = kata_to_hira(word)
            entries.append((word, reading, translation, sorting_reading))

    # 根据读音的五十音顺排序
    entries.sort(key=lambda x: (x[3], x[0]))

    # 输出CSV文件
    with open(output_csv, 'w', encoding='utf-8-sig') as f_csv:
        f_csv.write('單字,讀音,中文\n')
        for word, reading, translation, _ in entries:
            f_csv.write(f'{word},{reading},{translation}\n')

    # 输出Markdown文件
    with open(output_md, 'w', encoding='utf-8') as f_md:
        f_md.write('|單字|讀音|中文|\n')
        f_md.write('|---|---|---|\n')
        for word, reading, translation, _ in entries:
            f_md.write(f'|{word}|{reading}|{translation}|\n')

if __name__ == '__main__':
    main()
