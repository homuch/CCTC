from opencc import OpenCC
import json
import multiprocessing
import tqdm
import random

def to_traditional(text):
    cc = OpenCC('s2tw')
    return cc.convert(text)


def replace_quote(text):
    return text.replace('“', '「').replace('”', '」').replace('‘', "「").replace('’', "」")


def clean_text(text):
    text = to_traditional(text)
    text = replace_quote(text)
    return text


def clean_file(i, filename, instruction="這是現代中文，請將其翻譯成文言文。"):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    to_process = []
    for a in list(part['contents'] for part in data):
        to_process += a

    clean_list = []

    for content in tqdm.tqdm(to_process, position=i, desc=filename):
        clean_list.append({
            "instruction": instruction,
            "input": clean_text(content['target']),
            "output": clean_text(content['source'])
        })
    return clean_list


def main():
    file_list = ['lunyu/part1.json', 'shiji/part1.json',
                 'shiji/part2.json', 'zhongyong/part1.json', 'zhongyong/part2.json']
    test_ratio = 0.1
    num_processes = len(file_list)
    with multiprocessing.Pool(processes=num_processes) as p:
        clean_lists = p.starmap(
            clean_file, enumerate(file_list))
    clean_list = []
    for cl in clean_lists:
        clean_list += cl
    random.shuffle(clean_list)
    with open('clean.json', 'w', encoding='utf-8') as f:
        json.dump(clean_list[:int(len(clean_list) * (1 - test_ratio))], f, ensure_ascii=False, indent=2)
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(clean_list[int(len(clean_list) * (1 - test_ratio)):], f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
