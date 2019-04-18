'''
表格数据处理主程序

从 './data/origin_data' 获取《免征车辆购置税的新能源汽车车型目录》，《新能源汽车推广应用推荐车型目录》，《道路机动车辆生产企业及产品》文件，并进行表格信息解析，输出至 './data/output'

@Author: KivenChen
@Date: 2019-03-29
'''
import os
import shutil
from collections import defaultdict
from . import output
from .clean_data import clean_data
from .convert import doc2docx
from .parse_data import parse_docx, parse_html, parse_pdf


def main():
    # 获取根目录路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data')
    origin_path = os.path.join(data_path, 'origin_data')
    revised_path = os.path.join(data_path, 'revised_data')
    output_path = os.path.join(data_path, 'output')
    file_dir = os.listdir(origin_path)
    dic = defaultdict(list)
    # 遍历 origin_data 文件中的文件，根据文件名分为三类
    # 将文件复制至 revised_data 文件夹
    for file in file_dir:
        cat = file.split('（')[0]
        file_type = file.split('.')[-1]
        if file_type == 'docx':
            path = os.path.join(revised_path, file[:-1])
        else:
            path = os.path.join(revised_path, file)
        if not os.path.exists(path):
            shutil.copy(os.path.join(origin_path, file), path)
        dic[cat].append(path)
    for key, values in dic.items():
        if key == '免征车辆购置税的新能源汽车车型目录':
            df_list = []
            for value in values:
                file_name, file_type = value.split('.')
                if file_type == 'pdf':
                    df = parse_pdf(value)
                elif os.path.exists(value + 'x'):
                    df = parse_docx(value + 'x')
                # 对 doc 文件先转为 docx 文件，然后进行解析
                else:
                    df = parse_docx(doc2docx(value, value + 'x'))
                df_list.append(df)
            output.to_excel(df_list, os.path.join(output_path, key + '.xlsx'))
        elif key == '新能源汽车推广应用推荐车型目录':
            df_list = [parse_html(value, encoding='GBK') for value in values]
            output.to_excel(df_list, os.path.join(output_path, key + '.xlsx'))
        elif key == '道路机动车辆生产企业及产品':
            pass

    print('=' * 30)
    print('数据解析已完成!')
    print('=' * 30)

    # 清洗数据
    clean_data()

    print('=' * 30)
    print('数据清洗已完成!')
    print('=' * 30)


if __name__ == "__main__":
    main()
