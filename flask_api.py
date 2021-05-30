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


# 生成诗词的api接口
@app.route("/gen_poetry", methods=['GET'])
def gen_poetry():
    brand_name = request.args.get('brand_name')
    poe_list, word_dict_li = poetry.init()
    result = poetry.generate(brand_name, poe_list, word_dict_li)
    result = json.dumps(result, ensure_ascii=False)
    return result


if __name__ == "__main__":
    app.run()
