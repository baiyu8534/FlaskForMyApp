from flask import Flask
from application.settings.dev import DevelopmentConfig
from application.settings.prop import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_pymongo import PyMongo
import application.api.myapp_api as app_api
import json

app = Flask(__name__)

config = {
    'dev': DevelopmentConfig,
    'prop': ProductionConfig,
}

# 设置配置类
Config = config['dev']

# 加载配置
app.config.from_object(Config)

# 创建数据库连接对象
# db = SQLAlchemy(app)
mongo = PyMongo(app)


@app.route('/appapi/')
def hello_world():
    return 'Hello World!'


@app.route('/appapi/image', methods=['GET'])
def get_image_page_json_data():
    page_num = int(request.args.get('page_num'))
    page_size = int(request.args.get('page_size'))
    json_data_str = app_api.get_one_page_image(mongo.db.T2CY_image,
                                               query_filter=({}, {'_id': 0}),
                                               page_num=page_num-1,
                                               page_size=page_size)

    # all_data = mongo.db.XSNS_image.find({}, {'_id': 0})
    # json_data = {}
    # data = []
    # for item_data in all_data:
    #     data.append(item_data)
    # json_data["data"] = data
    # json_data_str = json.dumps(json_data, ensure_ascii=False)
    return json_data_str

@app.route('/appapi/ting55_search', methods=['GET'])
def ting55_search():
    name = request.args.get('name')
    page = int(request.args.get('page'))
    json_data_str = app_api.ting55_search(name,page)

    return json_data_str

@app.route('/appapi/get_p_list', methods=['GET'])
def get_p_list():
    p_id = request.args.get('p_id')
    p_url = "https://ting55.com/book/"+p_id
    json_data_str = app_api.get_p_list(p_url)
    return json_data_str


@app.route('/appapi/get_mp3_url', methods=['GET'])
def get_mp3_url():
    m_id = request.args.get('m_id')
    url = "https://ting55.com/book/"+m_id
    json_data_str = app_api.get_mp3_url(url)
    return json_data_str
    #return m_id + "|||||||||||"+url

if __name__ == '__main__':
    app.run()
