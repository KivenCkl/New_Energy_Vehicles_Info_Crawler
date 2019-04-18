'''
输出数据

@Author: KivenChen
@Date: 2019-04-11

Methods
-------
to_html: 将数据输出到 html 文件中

to_json: 将数据输出至 json 文件

to_files: 下载多个数据并保存为文件
'''
import json
import os
import asyncio
from .download import download


def to_html(data, path):
    '''将数据输出到 html 文件中

    Params
    ------
    data: dict, 键为名称，值为链接

    path: 储存路径
    '''

    head = '''

        <html>
        <meta charset="UTF-8">
        <body>
        <table>

    '''

    foot = '''

        </table>
        </body>
        </html>

    '''

    try:
        if os.path.exists(path):
            print('文件已存在：{}'.format(path))
            return

        with open(path, 'w', encoding='utf-8') as f:
            f.write(head)

            for title, url in sorted(data.items(), key=lambda item: item[0]):
                f.write('<tr><td><a href ={}>{}</a></td>'.format(url, url))
                f.write('<td>{}</td></tr>'.format(title))

            f.write(foot)
        print('文件已保存：{}'.format(path))
    except Exception as e:
        raise e


def to_json(data, path):
    ''' 将数据输出至 json 文件

    Params
    ------
    data: dict, 键为名称，值为链接

    path: 储存路径
    '''
    try:
        if os.path.exists(path):
            print('文件已存在：{}'.format(path))
            return
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        print('文件已保存：{}'.format(path))
    except Exception as e:
        raise e


def to_files(data, dir_name):
    ''' 下载多个数据并保存为文件

    Params
    ------
    data: dict, 键为名称，值为链接

    dir_name: 目标目录路径
    '''
    urls = []
    for key, value in data.items():
        # 提取文件后缀
        file_type = value.split('.')[-1].split('?')[0]
        path = os.path.join(dir_name, key + '.' + file_type)
        if os.path.exists(path):
            print('文件已存在：{}'.format(path))
        else:
            urls.append((value, path))
    try:
        if not urls:
            return
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.ensure_future(_to_file(url, path)) for url, path in urls
        ]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception as e:
        raise e


async def _to_file(url, path):
    ''' 异步下载数据并保存为文件

    Params
    ------
    url: str, 链接

    path: 储存路径
    '''
    response = await download(url, r_type='b')
    with open(path, 'wb') as f:
        f.write(response)
    print('文件已保存：{}'.format(path))
