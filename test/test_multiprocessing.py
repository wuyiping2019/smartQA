# -*- coding: utf-8 -*-
import time
import logging
import json
import requests
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def process(item):
    # log = get_logger(item[0])
    # log.info("item: %s" % item[0])

    # time.sleep(5)
    # return item[0] + '!'

    input_data = {'query': '姚明的职业是什么', 'attribute': item[0], 'answer': item[1]}

    # data_send = urllib.parse.urlencode(input_data) # 网址内带数据的形式
    # data_send = json.dumps(input_data).encode('utf-8').decode('unicode_escape')  # 数据以字典形式传送

    base_url = 'http://10.2.13.150:' + str(item[2]) + '/kg/sim'

    result = requests.post(base_url, json=input_data)
    # print("fetched %s" % base_url)

    res_json = json.loads(result.text)
    # print('response : ', res_json)

    return res_json


if __name__ == '__main__':

    print("Number of processors:", mp.cpu_count())

    attribute_list = ['民族', '逝世日期', '初中', '别名', '星座', '民族', '生肖', '语言', '运动项目', '国籍', '中文名',
                      '人物传记', '性别', '拼音', '中文名', '参加工作', '国籍', '主要成就', '国籍', '毕业院校', '职业',
                      '中文名', '出生地', '外文名', '祖籍', '身高', '重要事件', '鞋码', '民族', '信仰', '民族',
                      '中文名', '政治面貌', '中文名', '国籍', '代表作品', '出生日期', '职业', '主要奖项', '体重',
                      '女儿', '所属运动队', '研究生', '祖籍', '语种', '身高', '中文名', '职业', '出生地', '职务',
                      '中文名', '国籍', '职务', '出生地', '拼音', '专业特点', '主要奖项', '位置', '小学', '毕业院校',
                      '生涯最高分', '血型', '重要事件', '出生地', '出生日期', '毕业院校', '性别', '中文名', '入党时间',
                      '出生日期', '民族', '中文名', '代表作品', '出生地', '外文名', '性别', '代表作品', '体重',
                      '出生日期', '国籍', '妻子', '毕业院校', '球衣号码', '重要事件', '主要成就', '国籍', '外文名',
                      '职务', '中文名', '国籍', '国籍', '任职单位', '国籍', '职业']
    answer_list = ['汉族', '2018年1月21日', '上海市第二中学', '明王、移动长城、小巨人、大姚', '处女座', '汉族', '猴',
                   '普通话、英语、吴语', '篮球', '中国', '姚明', '《姚明传奇》', '男', 'yáo míng', '姚明', '1984年7月',
                   '中国', '中国戏歌的开山领路人', '中国', '沈阳音乐学院', '作曲家', '姚明', '上海市徐汇区', 'Yao Ming',
                   '苏州市吴江区震泽镇', '226 cm',
                   '专题影片《姚明年》发行2011年正式宣布退役2016年入选篮球名人堂2017年当选中国篮协主席11号球衣被火箭队退役展开专题影片《姚明年》发行2011年正式宣布退役2016年入选篮球名人堂2017年当选中国篮协主席11号球衣被火箭队退役2002年NBA选秀状元秀\xa0收起',
                   '53码', '汉', '共产主义', '汉族', '姚明', '中共党员', '姚明', '中国',
                   '《说唱脸谱》《前门情思大碗茶》《炊事班的故事》', '1948年', '一级作曲家（享受国务院津贴）',
                   '8次NBA全明星（2003-2009；2011）ESPN全球最有潜力运动员奖(2000)劳伦斯世界最佳新秀奖(2003)中国篮球杰出贡献奖世界最具影响力100人之一',
                   '140.6 公斤', '姚沁蕾', '已退役', '香港大学', '苏州吴江', '普通话、英语、吴语', '226厘米', '姚明',
                   '姚明集团董事长', '安庆', '公务员', '姚明', '中国', '陕西省城固县盐务局副局长', '辽宁省营口市',
                   'yáo míng', '20英尺外精确跳投',
                   '8次NBA全明星（2003-2009；2011）ESPN全球最有潜力运动员奖（2000）劳伦斯世界最佳新秀奖（2003）中国篮球杰出贡献奖世界最具影响力100人之一',
                   '中锋', '上海市高安路第一小学', '上海交通大学安泰经济与管理学院', '41分', 'B型',
                   '专题影片《姚明年》发行2011年正式宣布退役2016年入选篮球名人堂2017年当选中国篮协主席11号球衣被火箭队退役2002年NBA选秀状元秀\xa0收起',
                   '莆田市', '1966年6月', '厦门大学', '男', '姚明', '1994年5月', '1967年7月', '汉族', '姚明',
                   '前门情思大碗茶、故乡是北京、唱脸谱、大黄河、男子汉去飞行、小井胡同', '营口市', 'Yao Ming', '男',
                   '我的世界我的梦', '140.6公斤', '1980年9月12日', '中国', '叶莉',
                   '上海交通大学安泰经济与管理学院、上海市第二中学、香港大学', '11号（火箭队）、13号（国家队）、15号（上海队）',
                   '专题影片《姚明年》发行2011年正式宣布退役2016年入选篮球名人堂2017.2.23当选中国篮协主席',
                   '创建姚明织带饰品有限公司成立厦门姚明集团有限公司', '中国', 'Ming Yao', '姚明集团董事长', '姚明',
                   '中国', '中国', '绍兴市质监局', '中国', '公务员']

    port_list = [8081, 8082, 8083, 8084]

    input_d = []
    j = 0
    for i in range(len(attribute_list)):
        input_d.append([attribute_list[i], answer_list[i], port_list[j]])
        j += 1
        j = j % len(port_list)

    input_d.sort(key=lambda x: x[2])

    port_len_l = [0] * len(port_list)
    for i in range(len(input_d)):
        index_t = port_list.index(input_d[i][2])
        port_len_l[index_t] += 1
        print(input_d[i])

    print(port_len_l)

    # items = ['apple', 'bananan', 'cake', 'dumpling']

    start = time.time()

    input_d = input_d[0:40]
    pool = ThreadPool(2)
    results = pool.map(process, input_d)
    pool.close()
    pool.join()

    print("Done in %d seconds, fetched %s items." % (time.time() - start, len(results)))

    i = 0
    for tt in results:
        print(i, ": ", tt)
        i += 1

    # print(results)
