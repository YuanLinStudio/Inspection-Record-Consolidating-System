import datetime
import json

import numpy


def loadJson(filename):
    '''load dict from json file'''
    with open(filename, 'r', encoding='utf-8') as json_file:
        dic = json.load(json_file)
    return dic


class JsonEncoder(json.JSONEncoder):

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


def saveJson(filename, dic):
    '''save dict into json file'''
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(dic, json_file, ensure_ascii=False, cls=JsonEncoder)
