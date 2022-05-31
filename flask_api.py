# -*- coding: utf-8 -*-

from flask import Flask, request, json
from flask_cors import *
import poetry


app = Flask(__name__)
# 跨域请求
CORS(app, resources=r'/*')


# 获得词牌名列表的api接口
@app.route("/get_brand_name_list", methods=['GET'])
def get_brand_name_list():
    poe_list, word_dict_li = poetry.init()
    result = poetry.get_brand_name_list(poe_list)
    result = json.dumps(result, ensure_ascii=False)
    return result


# 根据词牌名随机生成一首宋词
@app.route("/generate_song_by_brand_name", methods=['GET'])
def generate_song_by_brand_name():
    brand_name = request.args.get('brand_name')
    poe_list, word_dict_li = poetry.init()
    result = poetry.generate_song_by_brand_name(brand_name, poe_list, word_dict_li)
    result = json.dumps(result, ensure_ascii=False)
    return result


# 随机生成一首藏头、藏腹、藏尾诗
@app.route("/generate_tang_by_structure_hide_sentence", methods=['GET'])
def generate_tang_by_structure_hide_sentence():
    sentence = request.args.get('sentence')
    position = int(request.args.get('position'))
    line_len = int(request.args.get('line_len'))
    if line_len == 5:
        structure = [2, 2, 1]
    else:
        structure = [2, 2, 3]
    poe_list, word_dict_li = poetry.init()
    result = poetry.generate_tang_by_structure_hide_sentence(structure, sentence, position, word_dict_li)
    result = json.dumps(result, ensure_ascii=False)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
