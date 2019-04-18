'''
从不同格式的文件中解析数据

@Author: KivenChen
@Date: 2019-03-29

Methods
-------
parse_html: 解析 html 文件

parse_pdf(path): 解析 pdf 文件

parse_docx(path): 解析 docx 文件
'''
import re
import os
import pandas as pd
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup


def parse_html(path, encoding='utf-8'):
    ''' 解析 html 文件

    Params
    ------
    path: str, 文件路径

    encoding: html 文件的编码，默认为 utf-8

    Return
    ------
    df: DataFrame 数据
    '''
    try:
        htmlfile = open(path, 'r', encoding=encoding)
        soup = BeautifulSoup(htmlfile.read(), 'lxml')
        tables = soup.find_all('table', class_='list-table')
        df_list = []
        pattern = re.compile(
            r'([\u4e00-\u9fa5].*[司厂])(?:.*）)?\s*([\u4e00-\u9fa5].*牌).*?([A-Z*][^\u4e00-\u9fa5]+?)\s*([\u4e00-\u9fa5]+)'
        )
        for table in tables:
            df_items = pd.concat(
                pd.read_html(table.prettify(), index_col=0, thousands=None)).T
            pz_id = df_items.pop('车辆基本信息')
            df_items['配置 ID'] = pz_id.str.replace(r'\s*配置ID：\s*', '')
            # 获取表格名称信息
            info = table.previous_sibling.previous_sibling.get_text()
            try:
                company, brand, model, vehicle_cat = pattern.search(
                    info).groups()
            except AttributeError:
                company, brand, model, vehicle_cat = '#', '#', '#', '#'
                print('请重新编写正则表达式！')
            df_items['生产企业公司'] = company
            df_items['品牌'] = brand
            df_items['车型'] = model
            df_items['车型分类'] = vehicle_cat
            df_list.append(df_items)
        df = pd.concat(df_list, axis=0)
        df.columns = df.columns.str.strip('：\s').str.replace('（',
                                                             '(').str.replace(
                                                                 '）', ')')
        df['来源'] = os.path.split(path)[-1].split('.')[0]
        print('解析成功：' + path)
        return df
    except Exception as e:
        raise e


def parse_pdf(path):
    ''' 解析 pdf 文件

    Params
    ------
    path: str, 文件路径

    Return
    ------
    df: DataFrame 数据
    '''
    try:
        pdf = pdfplumber.open(path)
        df_list = []
        # 提取所有页面中的表格
        tables = [
            table for page in pdf.pages for table in page.extract_tables()
        ]
        num_pattern = re.compile(r'\d+')
        temp_columns = tables[0][0]
        for table in tables:
            # 判断前后两个表格是否属于同一个表格
            if num_pattern.search(table[0][0]):
                df = pd.DataFrame(table, columns=temp_columns)
            else:
                df = pd.DataFrame(table[1:], columns=table[0])
                df.columns = df.columns.str.replace(r'\s+', '').str.replace(
                    '（', '(').str.replace('）', ')')
                temp_columns = df.columns
            for index, row in df.iterrows():
                df.loc[index] = row.str.replace(r'\s+', '')
            df_list.append(df)
        df = pd.concat(df_list)
        df['来源'] = os.path.split(path)[-1].split('.')[0]
        print('解析成功：' + path)
        return df
    except Exception as e:
        print('解析失败：' + path)
        raise e


def parse_docx(path):
    ''' 解析 docx 文件

    Params
    ------
    path: str, 文件路径

    Return
    ------
    df: DataFrame 数据
    '''
    try:
        document = Document(path)
        df_list = []
        for table in document.tables:
            # 提取每个表格中的信息
            data = [[cell.text for cell in row.cells] for row in table.rows]
            df = pd.DataFrame(data[1:], columns=data[0])
            df.columns = df.columns.str.replace(r'\s+', '').str.replace(
                '（', '(').str.replace('）', ')')
            for index, row in df.iterrows():
                df.loc[index] = row.str.replace(r'\s+', '')
            df_list.append(df)
        df = pd.concat(df_list)
        df['来源'] = os.path.split(path)[-1].split('.')[0]
        print('解析成功：' + path)
        return df
    except Exception as e:
        print('解析失败：' + path)
        raise e
