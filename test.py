import json


def get_strings(data):
    if type(data) == list:
        return {'mes':False,'data':data,'type':list}
    if type(data) == dict:
        return {'mes':False,'data':data,'type':dict}
    else:
        return {'mes': True, 'data': data,}


with open('./分类.json','r',encoding='utf-8') as f:
    data = json.load(f)
    for key,value in data.items():
        print(f'{key}:{value}')
    # for value in s.values():
    #     if type(value) == list:
    #         for value1 in value:
    #             if type(value1) == list:
    #                 for value2 in value1:
    #                     if type(value2) == list:
    #                         for value3 in value2:
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.value():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     elif type(value2) == dict:
    #                         for value3 in value2.value():
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.value():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     else:
    #                         print(value2)
    #             elif type(value1) == dict:
    #                 for value2 in value1.values():
    #                     if type(value2) == list:
    #                         for value3 in value2:
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.values():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     elif type(value2) == dict:
    #                         for value3 in value2.value():
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.values():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     else:
    #                         print(value2)
    #             else:
    #                 print(value1)
    #     elif type(value) == dict:
    #         for value1 in value.values():
    #             if type(value1) == list:
    #                 for value2 in value1:
    #                     if type(value2) == list:
    #                         for value3 in value2:
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.values():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     elif type(value2) == dict:
    #                         for value3 in value2.values():
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.values():
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             else:
    #                                 print(value3)
    #                     else:
    #                         print(value2)
    #             elif type(value1) == dict:
    #                 for value2 in value1.values():
    #                     if type(value2) == list:
    #                         for value3 in value2:
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.values():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     elif type(value2) == dict:
    #                         for value3 in value2.values():
    #                             if type(value3) == list:
    #                                 for value4 in value3:
    #                                     if type(value4) == list:
    #                                         for value5 in value4:
    #                                             print(5)
    #                             elif type(value3) == dict:
    #                                 for value4 in value3.values():
    #                                     print(value4)
    #                             else:
    #                                 print(value3)
    #                     else:
    #                         print(value2)
    #             else:
    #                 print(value1)
    #     else:
    #         print(value)




