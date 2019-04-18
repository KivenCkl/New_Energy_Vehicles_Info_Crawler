'''
初始化 URL

@Author: KivenChen
@Date: 2019-03-29

Methods
-------
get_urls: 生成 URLs
'''


def get_urls(url, **kwargs):
    ''' 生成 URLs

    Params
    ------
    url: str, 初始 url 样式

    kwargs: dict, 可接受的字典参数，pageNum 或 pageSize
        pageNum: 生成包含网页数目的 url 集合
        pageSize: 生成包含页面大小的 ajax url 集合

    Return
    ------
    urls: set, 生成的 url 集合
    '''
    urls = set()
    try:
        if 'pageNum' in kwargs.keys():
            for i in range(kwargs['pageNum'] + 1):
                if i == 1:
                    urls.add(url.format(pageNum=''))
                else:
                    urls.add(url.format(pageNum=('_' + str(i))))
        if 'pageSize' in kwargs.keys():
            urls.add(url.format(pageSize=kwargs['pageSize']))
    except Exception as e:
        raise e
    return urls
