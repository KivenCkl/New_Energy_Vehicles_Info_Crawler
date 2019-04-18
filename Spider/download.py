'''
下载响应页面

@Author: KivenChen
@Date: 2019-04-11

Methods
-------
download: 异步获取网页内容
'''
import aiohttp


async def download(url, r_type='s', encoding=None):
    ''' 异步获取网页内容

    Params
    ------
    url: str, 目标地址

    r_type: str, 返回内容格式，'b' or 's'

    encoding: str, 编码方式，默认为 None，自动解析，当 r_type 为 's' 有效

    Return
    ------
    response: str or bytes, 网页响应内容
    '''
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    retry = 0
    # 最多进行 5 次重连
    while retry < 5:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    assert resp.status == 200
                    response = resp.read() if r_type == 'b' else resp.text(
                        encoding)
                    return await response
        except AssertionError or TimeoutError:
            retry += 1
            print('{} 连接异常，正在进行第{}次尝试！'.format(url, retry))
        except Exception as e:
            raise e
    print('{} 连接失败！'.format(url))