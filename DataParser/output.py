'''
对结果进行输出

@Author: KivenChen
@Date: 2019-03-29

Methods
-------
to_excel: 将 Dataframe 输出至 EXCEL 表格中
'''
import pandas as pd
import os


def to_excel(objs, path):
    ''' 将 Dataframe 输出至 EXCEL 表格中

    Params
    ------
    objs: list or object, DataFrame 数据

    path: str, 输出路径，包括文件名与文件格式
    '''
    try:
        # 判断是单个 DataFrame 数据还是一组 DataFrame 数据
        df = pd.concat(objs) if isinstance(objs, list) else objs
        df.reset_index(drop=True, inplace=True)
        flag = 'y'
        if os.path.exists(path):
            flag = input("{}\n该文件已存在，是否覆盖 (y/n)? ".format(path))
        if flag.lower() == 'y':
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', encoding='utf-8')
            writer.save()
            print('文件已保存：{}'.format(path))
        else:
            print('文件已取消保存：{}'.format(path))
    except Exception as e:
        raise e
