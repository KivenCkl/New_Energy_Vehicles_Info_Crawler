'''
定义爬虫

第一类爬虫：爬取内容包括 道路机动车辆生产企业及产品 和 新能源汽车推广应用推荐车型目录

第二类爬虫：爬取内容为 免征车辆购置税的新能源汽车车型目录

@Author: KivenChen
@Date: 2019-03-29

Methods
-------
spider: 一个通用异步爬虫，解析给定地址的网页数据

handle_tasks: 多任务异步执行

spider_1: 第一类爬虫

spider_2: 第二类爬虫
'''
import asyncio
from . import parse_resp
from .download import download
from .urls import get_urls


async def spider(url, parser_method, **kwargs):
    ''' 定义一个通用异步爬虫，解析给定地址的网页数据

    Params
    ------
    url: str, 目标地址

    parser_method: function, 网页解析方法

    kwargs: dict, 可接受的字典参数，根据不同的解析方法传递不同的参数

    Return
    ------
    result: 解析后的数据
    '''
    try:
        response = await download(url)
        if response:
            print('spider is working ... ' + url)
            result = parser_method(response, **kwargs)
            return result
    except Exception as e:
        raise e


def handle_tasks(urls, loop, parser_method, **kwargs):
    ''' 多任务异步执行

    Params
    ------
    urls: set, 需要爬取的目标地址集合

    loop: an asyncio event loop

    parser_method: function, 网页解析方法

    kwargs: dict, 可接受的字典参数，根据不同的解析方法传递不同的参数

    Return
    ------
    ret_data: 存储解析后的数据
    '''
    try:
        ret_data = kwargs.get('ret_data')
        tasks = [
            asyncio.ensure_future(spider(url, parser_method, **kwargs))
            for url in urls
        ]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception as e:
        raise e
    return ret_data


def spider_1(loop, pageNum):
    '''第一类爬虫'''

    base_url = 'http://www.miit-eidc.org.cn'
    origin_url = 'http://www.miit-eidc.org.cn/miiteidc/gonggao/index{pageNum}.htm'
    urls = get_urls(origin_url, pageNum=pageNum)
    temp_urls = handle_tasks(
        urls,
        loop,
        parser_method=parse_resp.get_temp_urls,
        base_url=base_url,
        ret_data=set())
    data = handle_tasks(
        temp_urls,
        loop,
        parser_method=parse_resp.get_gonggao_data,
        base_url=base_url,
        ret_data=dict())
    return data


def spider_2(loop, pageSize):
    '''第二类爬虫'''

    base_url = 'http://www.miit.gov.cn'
    origin_url = 'http://www.miit.gov.cn/gdnps/searchIndex.jsp?params=%257B%2522goPage%2522%253A1%252C%2522orderBy%2522%253A%255B%257B%2522orderBy%2522%253A%2522publishTime%2522%252C%2522reverse%2522%253Atrue%257D%252C%257B%2522orderBy%2522%253A%2522orderTime%2522%252C%2522reverse%2522%253Atrue%257D%255D%252C%2522pageSize%2522%253A{pageSize}%252C%2522queryParam%2522%253A%255B%257B%2522shortName%2522%253A%2522title%2522%252C%2522value%2522%253A%2522%25E5%2585%258D%25E5%25BE%2581%25E8%25BD%25A6%25E8%25BE%2586%25E8%25B4%25AD%25E7%25BD%25AE%25E7%25A8%258E%25E7%259A%2584%25E6%2596%25B0%25E8%2583%25BD%25E6%25BA%2590%25E6%25B1%25BD%25E8%25BD%25A6%25E8%25BD%25A6%25E5%259E%258B%25E7%259B%25AE%25E5%25BD%2595%2522%252C%2522type%2522%253A%2522anlyzeStr%2522%257D%252C%257B%257D%252C%257B%2522shortName%2522%253A%2522fbjg%2522%252C%2522value%2522%253A%2522%252F1%252F29%252F1146295%252F1652858%252F1652930%2522%257D%255D%257D'
    urls = get_urls(origin_url, pageSize=pageSize)
    data = handle_tasks(
        urls,
        loop,
        parser_method=parse_resp.get_free_tax_data,
        base_url=base_url,
        ret_data=dict())
    return data
