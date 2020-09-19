'''JSON 读写服务'''

import datetime
import json
import os

import numpy


class JsonService:
    '''
    JSON 读写服务
    '''

    # 类变量
    filename = ''  # JSON 文件的目录文件名
    properties = {}  # JSON 文件内容

    def __init__(self, name='settings.json'):
        '''
        初始化
        新建对象时默认执行
        '''

        pass

    def __readFile(self):
        '''
        读取文件所有内容

        返回值：
            jsonText (str): JSON 文件的内容
        '''

        f = open(self.filename, 'r')
        jsonText = f.read()
        f.close()
        return jsonText

    def __writeFile(self, jsonText):
        '''
        所有内容覆盖到文件中

        参数值：
            jsonText (str): JSON 文件的内容

        返回值：
            result (bool): 成功或否
        '''
        try:
            f = open(self.filename, 'w')
            f.write(jsonText)
            f.close()
            return True

        except Exception:
            return False

    def set(self, key, value):
        '''
        保存一个属性。如果 key 不存在，则创建；存在，则覆盖

        参数值：
            key
            value

        返回值：
            result (bool): 成功或否
        '''

        self.properties[key] = value
        jsonText = json.dumps(self.properties)
        return self.__writeFile(jsonText)

    def get(self, key, default=None):
        '''
        获取一个属性值。如果不存在，则返回 default

        参数值：
            key
            default <OPTIONAL = None>

        返回值：
            - 若存在
            value

            - 若不存在
            default
        '''

        if key in self.properties:
            return self.properties.get(key)

        else:
            return default

    def load(self, filename):
        '''
        读取 JSON 文件所有内容

        参数值：
            filename (str): JSON 文件名和目录

        返回值：
            dic (dict): JSON 文件对应的 dict
        '''

        with open(filename, 'r', encoding='utf-8') as json_file:
            dic = json.load(json_file)
        return dic

    def save(self, filename, dic):
        '''
        写入 JSON 文件所有内容

        参数值：
            filename (str): JSON 文件名和目录
            dic (dict): 要写入 JSON 的 dict
        '''

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(dic, json_file, ensure_ascii=False, cls=JsonEncoder)


class JsonEncoder(json.JSONEncoder):
    '''
    供保存时编码使用，不对外使用
    '''

    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.__str__()
        else:
            return super(JsonEncoder, self).default(obj)
            