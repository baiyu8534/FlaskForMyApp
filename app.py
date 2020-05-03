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
    json_data_str = app_api.get_one_page_image(mongo.db.XSNS_image,
                                               query_filter=({}, {'_id': 0}),
                                               page_num=page_num,
                                               page_size=page_size)

    # all_data = mongo.db.XSNS_image.find({}, {'_id': 0})
    # json_data = {}
    # data = []
    # for item_data in all_data:
    #     data.append(item_data)
    # json_data["data"] = data
    # json_data_str = json.dumps(json_data, ensure_ascii=False)
    return json_data_str


if __name__ == '__main__':
    app.run()
