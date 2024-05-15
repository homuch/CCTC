from opencc import OpenCC
import json
import multiprocessing
import tqdm


def to_traditional(text):
    cc = OpenCC('s2tw')
    return cc.convert(text)


def replace_quote(text):
    return text.replace('“', '「').replace('”', '」').replace('‘', "「").replace('’', "」")


def clean_text(text):
    text = to_traditional(text)
    text = replace_quote(text)
    return text


def clean_file(i, filename, instruction="This is modern Chinese text, translate it to wenyanwen."):
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
    num_processes = len(file_list)
    with multiprocessing.Pool(processes=num_processes) as p:
        clean_lists = p.starmap(
            clean_file, enumerate(file_list))
    clean_list = []
    for cl in clean_lists:
        clean_list += cl
    with open('clean.json', 'w', encoding='utf-8') as f:
        json.dump(clean_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
