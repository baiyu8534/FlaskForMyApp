# 存放appapi对应api的数据库操作
import json


def get_one_page_image(collection, query_filter=None, page_num=0, page_size=10):
    """
    返回指定页数指定数量的图片
    :param collection:
    :param page_num:
    :param page_size:
    :return:
    """
    if page_num < 0:
        page_num = 0
    skip = page_size * page_num
    one_page_data = collection.find(query_filter[0], query_filter[1]).sort("catch_time",-1).limit(page_size).skip(skip)
    json_data = {}
    data = []
    for item_data in one_page_data:
        data.append(item_data)
    json_data["data"] = data
    json_data_str = json.dumps(json_data, ensure_ascii=False)
    return json_data_str
