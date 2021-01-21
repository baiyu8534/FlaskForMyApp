# 存放appapi对应api的数据库操作
import json
import requests
import urllib.parse
from lxml import etree


headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                            }


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

def ting55_search(name, page):
    # 本地去判断是否有下一页，数量足就让请求下一页，最多放回没有而已，服务器不用多做请求
    response = requests.get("https://ting55.com/search/{}/page/{}".format(urllib.parse.quote(name), page),
                            headers=headers)
    if response.status_code == 200:
        html = etree.HTML(response.content.decode())
        p_infos_html = html.xpath('//ul//li')
        p_infos_list = []

        # 有搜索结果
        if len(p_infos_html) > 0:

            for p_info_html in p_infos_html:
                p_info = {}
                p_info["url"] = "https://ting55.com" + p_info_html.xpath('.//div[@class="info"]//a/@href')[0]
                p_info["p_id"] = p_info["url"].split("/")[-1]
                p_info["name"] = p_info_html.xpath('.//div[@class="info"]//a/@title')[0]
                p_info["zhuozhe"] = p_info_html.xpath('.//div[@class="info"]//p/text()')[0]
                p_info["boyin"] = p_info_html.xpath('.//div[@class="info"]//p/text()')[1]
                p_info["time"] = p_info_html.xpath('.//div[@class="info"]//p/text()')[2]
                p_info["content"] = p_info_html.xpath('.//div[@class="info"]//p/text()')[3]
                p_info["image_url"] = "https:" + p_info_html.xpath('.//div[@class="img"]//img/@src')[0]
                p_infos_list.append(p_info)

            response_dict = {}
            response_dict["p_list"] = p_infos_list
            response_dict["status"] = 1
            response_dict["hit"] = "ok"

            content_page_str = "".join(html.xpath('//div[@class="c-page"]//text()'))
            if "下一页" not in content_page_str:
                # 说明是最后一页了
                response_dict["is_have_next_page"] = False
            else:
                response_dict["is_have_next_page"] = True
            res_json = json.dumps(response_dict, ensure_ascii=False)
        else:
            response_dict = {}
            response_dict["p_list"] = []
            response_dict["status"] = -1
            response_dict["hit"] = "没有跟多了"
            response_dict["is_have_next_page"] = False
            res_json = json.dumps(response_dict, ensure_ascii=False)
    else:
        response_dict = {}
        response_dict["p_list"] = []
        response_dict["status"] = -1
        response_dict["hit"] = "服务器开小差了"
        response_dict["is_have_next_page"] = False
        res_json = json.dumps(response_dict, ensure_ascii=False)

    # 返回数据
    return res_json


def get_p_list(p_url):
    response = requests.get(p_url, headers=headers)
    if response.status_code == 200:

        html = etree.HTML(response.content.decode())

        title = html.xpath('//h1/text()')[0]
        p_url_list = ["https://ting55.com" + url for url in html.xpath('//div[@class="plist"]//a/@href')]
        p_name_list = [title + " " + name for name in html.xpath('//div[@class="plist"]//a/text()')]
        response_dict = {}
        # response_dict["p_url_list"] = p_url_list
        # response_dict["p_name_list"] = p_name_list
        p_list = []
        for i in range(len(p_url_list)):
            p_info = {}
            p_info["name"] = p_name_list[i]
            p_info["url"] = p_url_list[i]
            p_info["m_id"] = p_url_list[i].split("/")[-1]
            p_list.append(p_info)
        response_dict["p_list"] = p_list
        response_dict["status"] = 1
        response_dict["hit"] = "ok"
        res_json = json.dumps(response_dict, ensure_ascii=False)
    else:
        response_dict = {}
        response_dict["p_url_list"] = []
        response_dict["p_name_list"] = []
        response_dict["status"] = -1
        response_dict["hit"] = "服务器开小差了"
        res_json = json.dumps(response_dict, ensure_ascii=False)
    # 返回数据
    return res_json


def get_mp3_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        # "Referer": "https://ting55.com/book/3670-11",
        # "xt": "8efefcaf16b788a67a6357bb0ac25586",
        # "Host":"ting55.com",
        # "Origin":"https://ting55.com"
    }
    response_dict = {}
    response = requests.get(url, headers=headers)
    if 200 == response.status_code:
        html = etree.HTML(response.content.decode())
        xt = html.xpath('//meta[@name="_c"]/@content')[0]
        headers["Referer"] = url
        headers["xt"] = xt

        name_ = "`" + html.xpath('//h1/text()')[0]

        name_ = urllib.parse.quote(urllib.parse.quote(name_))
        url_ = urllib.parse.quote(url)
        ting55_history = url_ + name_

        bookId = url.split("/")[-1].split("-")[0]
        page = url.split("/")[-1].split("-")[1]

        mp3_response = requests.post("https://ting55.com/glink", {"bookId": bookId, "isPay": 0, "page": page},
                                     cookies={"ting55_history": ting55_history}, headers=headers)
        if 200 == mp3_response.status_code:
            mp3_res_dict = json.loads(mp3_response.content.decode())

            response_dict["mp3_url"] = mp3_res_dict["url"]
            response_dict["status"] = 1
            response_dict["hit"] = "ok"
            res_json = json.dumps(response_dict, ensure_ascii=False)
        else:
            response_dict["mp3_url"] = ""
            response_dict["status"] = -1
            response_dict["hit"] = "服务器开小差了"
            res_json = json.dumps(response_dict, ensure_ascii=False)
    else:

        response_dict["mp3_url"] = ""
        response_dict["status"] = -1
        response_dict["hit"] = "服务器开小差了"
        res_json = json.dumps(response_dict, ensure_ascii=False)

    return res_json

