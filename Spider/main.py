'''
爬虫主程序

从工信部获取并下载《免征车辆购置税的新能源汽车车型目录》，《新能源汽车推广应用推荐车型目录》，《道路机动车辆生产企业及产品》文件，文件储存至 './data/origin_data'

@Author: KivenChen
@Date: 2019-04-10
'''
import os
import asyncio
from . import output
from .spider import spider_1, spider_2


def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data')
    data = {}
    loop = asyncio.get_event_loop()
    data.update(spider_1(loop, pageNum=8))
    # 数据修正，网页上链接出错
    # 根据规律找到修正网址
    data[
        '新能源汽车推广应用推荐车型目录（2018年第1批）'] = 'http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/201801.html'
    data[
        '新能源汽车推广应用推荐车型目录（2018年第4批）'] = 'http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/201804.html'
    data[
        '新能源汽车推广应用推荐车型目录（2017年第1批）'] = 'http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/201701.htm'
    data[
        '新能源汽车推广应用推荐车型目录（2017年第2批）'] = 'http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/201702.htm'
    print('Spider 1 is done!')
    data.update(spider_2(loop, pageSize=1000))
    print('Spider 2 is done!')
    output.to_files(data, os.path.join(data_path, 'origin_data'))
    loop.close()
    print('=' * 30)
    print('链接爬取已完成!')
    print('=' * 30)


if __name__ == "__main__":
    main()
