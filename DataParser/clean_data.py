'''
清洗数据

@Author: KivenChen
@Date: 2019-04-09
'''
import pandas as pd
import os
from . import output


def clean_data():
    # 获取 data 文件夹路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'output')

    df_free_tax = pd.read_excel(
        os.path.join(data_path, '免征车辆购置税的新能源汽车车型目录.xlsx'), encoding='utf-8')
    df_recommend_model = pd.read_excel(
        os.path.join(data_path, '新能源汽车推广应用推荐车型目录.xlsx'), encoding='utf-8')

    # 对 免征车辆购置税的新能源汽车车型目录 数据进行清洗
    # 对相同内容不同列名的列进行整合
    df_free_tax['汽车生产企业名称'] = df_free_tax['汽车生产企业名称'].combine_first(
        df_free_tax['汽车企业名称'])
    df_free_tax['汽车生产企业名称'] = df_free_tax['汽车生产企业名称'].combine_first(
        df_free_tax['生产企业名称'])
    df_free_tax.drop(['汽车企业名称', '生产企业名称'], axis=1, inplace=True)

    # 改正错误内容
    temp_df = df_free_tax.loc[df_free_tax['错误内容'].notnull(), ['车辆型号', '正确内容']]
    df_free_tax.drop(temp_df.index, inplace=True)
    df_free_tax.drop(['错误内容', '正确内容', '序号'], axis=1, inplace=True)
    df_free_tax.loc[df_free_tax['车辆型号'].
                    isin(temp_df['车辆型号']), '汽车生产企业名称'] = list(temp_df['正确内容'])
    # 对于合并单元格，只有第一行有内容，因此需要将后面空白的单元格向前填充
    df_free_tax['汽车生产企业名称'].fillna(method='ffill', inplace=True)
    df_free_tax.rename(
        columns={
            '车辆型号': '车型',
            '整车整备质量(kg)': '整备质量(kg)'
        }, inplace=True)

    # 合并
    df = pd.merge(
        left=df_free_tax,
        right=df_recommend_model,
        how='outer',
        on=['车型', '燃料电池系统额定功率(kW)', '整备质量(kg)'],
        suffixes=('_free_tax', '_recommend_model'))

    output.to_excel(df, os.path.join(data_path, '汇总.xlsx'))


if __name__ == "__main__":
    clean_data()
