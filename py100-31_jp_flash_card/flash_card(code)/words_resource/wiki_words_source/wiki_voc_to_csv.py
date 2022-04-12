import os
import csv
import re


def convert_source(source_file: str) -> list[dict[str, str]]:
    content_list = []
    with open(source_file, mode='r', encoding='utf-8') as csvfile:
        data = csvfile.readlines()
        for row in data:

            row = re.sub(r'{{Node-count limit exceeded\|ja\|(.+?)}}', r'\g<1>', row)
            sep_row = row.split('-', 1)
            jp = sep_row[0]
            en = sep_row[1]
            jp = jp.replace(' ', '')
            if ',' in jp:
                jp = jp.replace(',', '(') + ')'

            end_index = 0
            while en.find('(', end_index) != -1:
                start_index = en.find('(', end_index)
                end_index = en.find(')', start_index)
                en = en[:start_index].replace(',', '\n') + en[start_index:end_index] + en[end_index:]
            else:
                en = en[:end_index] + en[end_index:].replace(',', '\n')
            content_list.append({'jp': jp,
                                 'en': en})
    return content_list


def output_data(output_file: str, content: list):
    with open(output_file, encoding='utf-8', mode='a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['jp', 'en'])
        if os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerows(content)


task1 = {'wiki_words_source': ['jp_n5-voc.txt'], 'target': '../jp_n5.csv'}
task2 = {'wiki_words_source': ['jp_n4-voc.txt'], 'target': '../jp_n4.csv'}
task3 = {'wiki_words_source': ['jp_n3-voc_p1.txt', 'jp_n3-voc_p2.txt'], 'target': '../jp_n3.csv'}
task4 = {'wiki_words_source': ['jp_n2-voc_p1.txt', 'jp_n2-voc_p2.txt'], 'target': '../jp_n2.csv'}
words = ['a', 'ka', 'sa', 'ta', 'na', 'ha', 'ma', 'ya', 'ra', 'wa', 'katakana']
task5 = {'wiki_words_source': ['jp_n1-voc_' + word + '.txt' for word in words], 'target': '../jp_n1.csv'}
task_list = [task1, task2, task3, task4, task5]

for task in task_list:
    source_list = task['wiki_words_source']
    output_file = task['target']
    for source in source_list:
        content = convert_source(source)
        output_data(output_file, content)
