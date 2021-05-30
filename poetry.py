import re
import os
import random
import time
random.seed(time.time())    # 设置随机数种子


poetry_path = 'resource/Ci.txt'     # 语料库路径
path_1 = 'output/freq1.txt'         # 单字词文件
path_2 = 'output/freq2.txt'         # 双字词文件
path_3 = 'output/freq3.txt'         # 三字词文件

symbols = '[，。！？“”、（）；《》：]'    # 词中的标点符号（用于分句）
err = ['□', '■', '‘', '(', ')']     # 文件中的乱码（用于过滤）
two_lim = 5                         # 双字词判断是词的阈值
three_lim = 15                      # 三字词判断是否为词的阈值


# 诗词类
class Poetry:
    title = None        # 标题
    author = None       # 作者
    content = []        # 内容（列表的每一项是一行）


# 从语料库文件中读出数据，并返回诗词对象列表
# path：语料库路径
# 返回值：诗词对象列表
def load_poetry(path, encoding='utf8'):
    poetry = []
    with open(path, 'r', encoding=encoding) as file:
        title = None
        author = None
        while True:
            string = file.readline()
            blank_lines = 0
            while string == '\n':
                string = file.readline()
                blank_lines += 1
            if blank_lines == 3:                            # 作者前有三个空行
                author = string[:-1]
            elif blank_lines == 2 or blank_lines == 0:      # 题目前有2个空行，第一首词无空行
                title = string[:-1]
            elif blank_lines == 1 and string:               # 内容前有一个空行
                # 将诗歌包装成诗歌对象
                p = Poetry()
                p.title = title
                p.author = author
                p.content = re.split(symbols, string[:-1])[:-1]
                poetry.append(p)
                # print(p.title)
                # print(p.author)
                # print(p.content)
            if not string:                                  # 已读完文件内容
                return poetry


# 统计每个词的出现频率
# poetry：诗词对象列表
# n：元数
# 返回值：词频字典
def frequency(poetry_list, n):
    freq = {}
    # 遍历所有诗词
    for p in poetry_list:
        # 遍历所有句子
        for sentence in p.content:
            # 找潜在的词
            for i in range(len(sentence) - n + 1):
                word = sentence[i: i+n]
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))


# 将频率字典写入文件
# poetry_list：诗词对象列表
# path1\2\3：三种词频文件要写入的路径
def write_file(poetry_list, path1, path2, path3):
    freq = frequency(poetry_list, 1)
    with open(path1, 'w', encoding='utf8') as file:
        for i in freq:
            if i not in err:
                file.write(i + ':' + str(freq[i]) + '\n')

    freq = frequency(poetry_list, 2)
    with open(path2, 'w', encoding='utf8') as file:
        for i in freq:
            flag = False
            for ch in i:
                if ch in err:
                    flag = True
            if freq[i] >= two_lim and not flag:
                file.write(i + ':' + str(freq[i]) + '\n')

    freq = frequency(poetry_list, 3)
    with open(path3, 'w', encoding='utf8') as file:
        for i in freq:
            flag = False
            for ch in i:
                if ch in err:
                    flag = True
            if freq[i] >= three_lim and not flag:
                file.write(i + ':' + str(freq[i]) + '\n')


# 载入一个词频文件
# path：词频文件路径
# 返回值：词频字典
def load_word(path, encoding='utf8'):
    word_dict = {}
    with open(path, 'r', encoding=encoding) as file:
        for line in file.readlines():
            part = line.split(':')
            word_dict[part[0]] = int(part[1])
    return word_dict


# 获得一个词牌名下词的结构信息（如何分词）
# poetry_list：诗词对象列表
# brand_name：词牌名
# wd_dict_list：三种词词频字典的列表
# 返回值：该词牌名词的结构，用列表来表示
def get_structure(poetry_list, brand_name, wd_dict_list):
    structure = []
    for poetry in poetry_list:
        if poetry.title == brand_name:
            # print(poetry.content)
            poe_li = []
            for sentence in poetry.content:
                sen_li = []
                pos = 0
                # print(sentence)
                while pos < len(sentence):
                    # 向前搜索3、2、1个字，判断是不是词
                    # 列表切片索引可越界，返回结果不包含越界部分
                    if pos < len(sentence) and sentence[pos:pos+3] in wd_dict_list[2]:
                        sen_li.append(3)
                        pos += 3
                    elif pos < len(sentence) and sentence[pos:pos+2] in wd_dict_list[1]:
                        sen_li.append(2)
                        pos += 2
                    elif pos < len(sentence) and sentence[pos] in wd_dict_list[0]:
                        sen_li.append(1)
                        pos += 1
                    else:
                        pos += 1
                poe_li.append(sen_li)
            structure.append(poe_li)
    # print(structure[random.randint(0, len(structure) - 1)])
    # 如果未找到
    if len(structure) == 0:
        return None
    # 从所有可能的结构中随机选取一个
    return structure[random.randint(0, len(structure) - 1)]


# 获得所有词牌名（前端界面下拉列表调用）
# poetry_list：诗词对象列表
# 返回值：所有词牌名列表
def get_brand_name_list(poetry_list):
    result = []
    # 统计词牌名
    for poetry in poetry_list:
        if poetry.title not in result:
            result.append(poetry.title)
    return result


# 获取诗词词频迭代列表
# wd_dict_list：三种词词频字典的列表
# 返回值：诗词词频迭代列表
def get_freq_count(wd_dict_list):
    count = []
    for di in wd_dict_list:
        tmp = 0
        for wd in di:
            tmp += di[wd]
        count.append(tmp)
    return count


# 根据词的长度随机生成一个词
# word_len：词的长度
# count：诗词词频迭代列表
# wd_dict_list：三种词词频字典的列表
# 返回值：随机的一个词
def get_random_word(word_len, count, wd_dict_list):
    # 排除太长太短的情况
    if word_len <= 0 or word_len > 3:
        return None
    # 随机生成一个数（不超过词典中所有词词频之和）
    rand = random.randint(0, count[word_len - 1])
    # 遍历所有词
    for word in wd_dict_list[word_len - 1]:
        # 直到该随机数小于等于0，就选取该词
        if rand <= 0:
            return word
        # 在该随机数中减去该词的词频
        rand -= wd_dict_list[word_len - 1][word]


# 寻找符合藏字要求的词
# target：目标字
# word_pos：藏字位置
# wd_dict：词频字典
def search_word(target, word_pos, wd_dict):
    result = []
    for word in wd_dict:
        # 如果找到了要藏的词
        if word[word_pos] == target:
            result.append(word)
    if len(result) == 0:
        return ''
    # 结果随机返回一个
    return result[random.randint(0, len(result) - 1)]


# 根据词牌名随机生成一首宋词
# brand_name：词牌名
# poetry_list：诗词对象列表
# wd_dict_list：三种词词频字典的列表
# 返回值：生成的诗词按句子组成的列表
def generate_song_by_brand_name(brand_name, poetry_list, wd_dict_list):
    result = []
    # 获得该词牌的结构
    structure = get_structure(poetry_list, brand_name, wd_dict_list)
    # 如果无该词牌名
    if structure is None:
        return []
    # print(structure)
    count = get_freq_count(wd_dict_list)
    # 遍历结构列表
    for sen in structure:
        line = ''
        # 随机生成每一行诗句
        for word_len in sen:
            line += get_random_word(word_len, count, wd_dict_list)
        result.append(line)
    return result


# 随机生成一首唐诗
# structure：单句的结构，如[2, 2, 2, 1]表示：一句7个字，按2、2、2、1进行分词
# sen_count：诗句数量
# wd_dict_list：三种词词频字典的列表
# 返回值：生成的诗词按句子组成的列表
def generate_tang_by_structure(structure, sen_count, wd_dict_list):
    result = []
    count = get_freq_count(wd_dict_list)
    for i in range(sen_count):
        line = ''
        # 随机生成每一行诗句
        for word_len in structure:
            line += get_random_word(word_len, count, wd_dict_list)
        result.append(line)
    return result


# 随机生成一首藏头、藏腹、藏尾诗
# structure：单句的结构，如[2, 2, 2, 1]表示：一句7个字，按2、2、2、1进行分词
# sentence：要藏的句子
# position：藏的位置
# wd_dict_list：三种词词频字典的列表
# 返回值：生成的诗词按句子组成的列表
def generate_tang_by_structure_hide_sentence(structure, sentence, position, wd_dict_list):
    result = []
    count = get_freq_count(wd_dict_list)
    for i in range(len(sentence)):
        line = ''
        # 随机生成每一行诗句
        pos = 0
        for word_len in structure:
            # 先根据是不是要藏的词进行处理
            # 如果是要藏的词，此处如果等于，说明是下一个词的开头是要藏的位置
            if pos <= position < pos + word_len:
                word_pos = position - pos
                # 寻找符合藏字要求的词
                cur_word = search_word(sentence[i], word_pos, wd_dict_list[word_len - 1])
                # 如果没找到要藏的字
                if len(cur_word) == 0:
                    # 生成要藏的字前面的词
                    word = get_random_word(word_pos, count, wd_dict_list)
                    if word is not None:
                        cur_word += word
                    # 加入要藏的字
                    cur_word += sentence[i]
                    # 生成要藏的字后面的词
                    word = get_random_word(word_len - word_pos - 1, count, wd_dict_list)
                    if word is not None:
                        cur_word += word
                line += cur_word
                pos += word_len
                # 该词已藏完，跳过后面的步骤
                continue
            line += get_random_word(word_len, count, wd_dict_list)
            pos += word_len
        result.append(line)
    return result


# 初始化诗词库诗词列表，单字词、双字词、三字词词频字典
# 返回值：词库诗词列表，单字词、双字词、三字词词频字典的列表
def init():
    poetry_list = load_poetry(poetry_path)
    if not (os.path.exists(path_1) and os.path.exists(path_2) and os.path.exists(path_3)):
        write_file(poetry_list, path_1, path_2, path_3)
    word_dict1 = load_word(path_1)
    word_dict2 = load_word(path_2)
    word_dict3 = load_word(path_3)
    # print(word_dict1)
    # print(word_dict2)
    # print(word_dict3)
    return poetry_list, [word_dict1, word_dict2, word_dict3]


# 程序入口
if __name__ == '__main__':

    # 初始化诗词对象列表、词频列表
    poe_list, word_dict_li = init()

    # 输出所有的词牌名
    # print(get_brand_name_list(poe_list))

    # 循环输入和生成
    while True:
        brd_name = input('请输入词牌名：')
        # poe = generate_song_by_brand_name(brd_name, poe_list, word_dict_li)
        # poe = generate_tang_by_structure([2, 2, 2, 1], 4, word_dict_li)
        poe = generate_tang_by_structure_hide_sentence([2, 3, 2], '我爱你', 0, word_dict_li)
        print('生成：')
        print(poe)
        print('----------------------------------')
