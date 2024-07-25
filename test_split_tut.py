import pandas as pd
import argparse
import re


def split_quoted_string(input_str):
    if not isinstance(input_str ,str):
        return []

    # # 定义分隔符为三个双引号后跟一个中文逗号，或者一个中文逗号和一个空格，或者一个中文逗号和一个换行符
    # delimiters = ['","', '", "', '",\n"','",\n\n"', '"\n\n"','"\n\n\n"', ",  ", ", \n", "  ", " \n"]
    #
    # 1
    # # 去除两端的双引号
    # input_str = input_str.strip('"')
    #
    # # 检查是否有分隔符，并分割字符串
    # for delimiter in delimiters:
    #     if delimiter in input_str:
    #         items = input_str.split(delimiter)
    #         break
    #
    #     else:  # 如果没有找到任何分隔符，将整个字符串作为一个元素
    #         items = [input_str]

    # 对列表中的每个元素去除两端的双引号
    # result = [item.strip('"') for item in items if item.strip('"') != '']

    # use regular expression
    # first pattern: string between the first quote and quote followed by a comma + space
    # last pattern: string between quote following a comma + space and the last quote
    # other basic pattern: string between quote following a comma + space and quote followed by a comma + space
    first_pattern = re.compile(r'^"(([^"]|"")+)",\s')
    other_pattern = re.compile(r'(?<=\s")((?:[^"]|"")+)(?=",\s)')
    last_pattern = re.compile(r'(?<=\s")(([^"]|"")+)"$')

    # find the first string
    first_match = first_pattern.match(input_str)
    result = []
    if first_match:
        result.append(first_match.group(1))
        remaining_string = input_str[first_match.end():]
    else:
        remaining_string = input_str

    # find the last string
    last_match = last_pattern.search(remaining_string)
    if last_match:
        last_part = last_match.group(1)
        remaining_string = remaining_string[:last_match.start()].rstrip(", ")
    else:
        last_part = None

    # find other strings in the middle
    matches = other_pattern.findall(remaining_string)
    result.extend(matches)

    # add the last tutorial string
    if last_part:
        result.append(last_part)

    # add other middle strings
    matches = other_pattern.findall(remaining_string)
    result.extend(matches)

    return result


def test_split_from_csv(csv_file):
    dataset_df = pd.read_csv(csv_file)
    for i, row in dataset_df.iterrows():
        tutorial_strings_list = split_quoted_string(row['tutorial_strings'])
        if len(tutorial_strings_list) > 3:
            print(tutorial_strings_list)

if __name__ == "__main__":
    test_split_from_csv("positive_0725.csv")

