'''
转换文件格式

@Author: KivenChen
@Date: 2019-04-03

Methods
-------
doc2docx: doc 转 docx

word2pdf: word 转 pdf
'''
from win32com import client


def doc2docx(doc_name, docx_name):
    ''' doc 转 docx

    Params
    ------
    doc_name: 源文件路径

    docx_name: 转换后文件路径

    Return
    ------
    docx_name: 转换后文件路径
    '''
    try:
        word = client.Dispatch("Word.Application")
        # 后台运行
        word.Visible = 0
        word.DisplayAlerts = 0
        doc = word.Documents.Open(doc_name)
        # 将 doc 转换成 docx
        doc.SaveAs(docx_name, 12, False, "", True, "", False, False, False,
                   False)
        print('转换成功：' + docx_name)
        return docx_name
    except Exception as e:
        print('转换失败：' + doc_name)
        raise e
    finally:
        doc.Close()
        word.Quit()


def word2pdf(word_name, pdf_name):
    ''' word 转 pdf

    Params
    ------
    word_name: 源文件路径

    pdf_name: 转换后文件路径

    Return
    ------
    pdf_name: 转换后文件路径
    '''
    try:
        word = client.DispatchEx("Word.Application")
        doc = word.Documents.Open(word_name, ReadOnly=1)
        doc.SaveAs(pdf_name, 17)
        print('转换成功：' + pdf_name)
        return pdf_name
    except Exception as e:
        print('转换失败：' + word_name)
        raise e
    finally:
        doc.Close()
        word.Quit()
