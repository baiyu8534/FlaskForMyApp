from flask import Flask
from application.settings.dev import DevelopmentConfig
from application.settings.prop import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/image', methods=['GET'])
def get_image_page_json_data():
    all_data = mongo.db.XSNS_image.find({}, {'_id': 0})
    json_data = {}
    data = []
    for item_data in all_data:
        data.append(item_data)
    json_data["data"] = data
    json_data_str = json.dumps(json_data, ensure_ascii=False)
    return json_data_str


if __name__ == '__main__':
    app.run()
