'''
解析响应内容

@Author: KivenChen
@Date: 2019-04-03

Methods
-------
parser: BeautifulSoup DOM 树处理

get_json_value: 将响应内容解析为字典形式

get_temp_urls: 解析获取公告数据的中转 url

get_gonggao_data: 解析公告数据

get_free_tax_data: 解析免征购置税新能源汽车车型目录数据
'''
import re
import json
from bs4 import BeautifulSoup


def parser(response):
    ''' BeautifulSoup DOM 树处理

    Params
    ------
    response: str, 网页响应内容

    Return
    ------
    soup: 树处理后结果
    '''
    if not response:
        return
    try:
        soup = BeautifulSoup(response, 'lxml')
        return soup
    except Exception as e:
        raise e


def get_json_value(response, item=None):
    ''' 将响应内容解析为字典形式

    Params
    ------
    response: str, 网页响应内容

    item: str, 默认为 None

    Return
    ------
    dict or str:
        当 item 为 None 时，返回转换后的 dict 数据
        否则，返回 dict 数据中键为 item 的值
    '''
    # 将响应内容转换为字典，并返回键为 item 的值
    if not response:
        return
    try:
        response = re.findall(r'\{.*\}', response)[0]
        json_data = json.loads(response)
        return json_data[item] if item else json_data
    except Exception as e:
        raise e


def get_temp_urls(response, base_url=None, ret_data=set()):
    ''' 解析获取公告数据的中转 url

    Params
    ------
    response: str, 网页响应内容

    base_url: str, 网页主域名，默认为 None

    ret_data: set, 存储所有解析后的 url 集合

    Return
    ------
    urls: set, 解析后获取的集合
    '''
    urls = set()
    soup = parser(response)
    try:
        parent_nodes = soup.find_all('div', class_='f-left')
        for node in parent_nodes:
            title = node.find('a')['title']
            # 筛选标题带有（第.*批）的数据
            if re.findall(r'（第.*批）', title):
                url = node.find('a')['href']
                if base_url and url.startswith(r'/'):
                    url = base_url + url
                urls.add(url)
    except Exception as e:
        raise e
    ret_data.update(urls)
    return urls


def get_gonggao_data(response, base_url=None, ret_data=dict()):
    ''' 解析公告数据

    Params
    ------
    response: str, 网页响应内容

    base_url: str, 网页主域名，默认为 None

    ret_data: dict, 存储所有解析后的数据

    Return
    ------
    data: dict, 解析后获取的数据
    '''
    data = {}
    title_1 = '新能源汽车推广应用推荐车型目录'
    title_2 = '车辆生产企业及产品'
    title_3 = '道路机动车辆生产企业及产品'
    soup = parser(response)
    try:
        parent_nodes = soup.find('div', id='news_content').find_all('a')
        for node in parent_nodes:
            title = node.get_text()
            url = node['href']
            if base_url and url.startswith(r'/'):
                url = base_url + url
            # 获取批次信息
            pici = re.findall(r'（.*）', title)
            # 筛选带有批次的数据
            if pici:
                # 筛选 新能源汽车推广应用推荐车型目录 数据
                if title_1 in title:
                    data[title_1 + pici[0]] = url
                # 筛选 道路机动车辆生产企业及产品 数据
                elif title_2 in title:
                    data[title_3 + pici[0]] = url
    except Exception as e:
        raise e
    ret_data.update(data)
    return data


def get_free_tax_data(response, base_url=None, ret_data=dict()):
    ''' 解析免征购置税新能源汽车车型目录数据

    Params
    ------
    response: str, 网页响应内容

    base_url: str, 网页主域名，默认为 None

    ret_data: dict, 存储所有解析后的数据

    Return
    ------
    data: dict, 解析后获取的数据
    '''
    data = {}
    title_1 = '免征车辆购置税的新能源汽车车型目录'
    results = get_json_value(response, item='resultMap')
    try:
        for items in results:
            pici = re.findall(r'（第.*批）', items['title'])
            # 筛选带有批次的数据
            if pici:
                # 重构标题
                title = title_1 + pici[0]
                # 解析 url 内容
                soup = parser(items['htmlContent'])
                nodes = soup.find_all('a')
                for node in nodes:
                    # 防止获取的是错误信息
                    if pici[0] in node.get_text():
                        url = node['href']
                        if base_url and url.startswith(r'/'):
                            url = base_url + url
                        data[title] = url
    except Exception as e:
        raise e
    ret_data.update(data)
    return data
