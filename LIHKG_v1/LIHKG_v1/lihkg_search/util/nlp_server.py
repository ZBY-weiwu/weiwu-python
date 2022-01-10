# -*- coding: UTF-8 -*-
from nlp_api import *
import json
import sys
class NLP_server:
    def __init__(self,cont):
        self.nlp_json = nlp_deal(cont)
    def index(self):
        if self.nlp_json == 'True':
            return "True"
        nlp_data = json.loads(self.nlp_json)
        nlp_data = nlp_data['value']
        data={}
        lkey = nlp_data.get('lkey',"")
        data['lkey'] = (','.join(lkey))
        vkey_list = nlp_data['vkey']
        vkey = []
        for vkey_d in vkey_list:
            vkey.append(vkey_d['v'])
        data['vkey'] = ",".join(vkey) 
        vrgn_list = nlp_data['vrgn']
        vrgn = []
        for vrgn_d in vrgn_list:
            vrgn.append(vrgn_d['v'])
        data['vrgn'] =",".join(vrgn)
        vpers_list = nlp_data['vpers']
        vpers = []
        for vpers_d in vpers_list:
            vpers.append(vpers_d['v'])
        data['vpers'] = ','.join(vpers)
        data['abstr'] = nlp_data['abstr']
        vorg_list = nlp_data['vorg']
        vorg = []
        for vorg_d in vorg_list:
            vorg.append(vorg_d['v'])
        data['vorg'] = ','.join(vorg)
        if_sent = int(nlp_data['sent'])
        if if_sent>=55:
            sent = "积极"
        elif 45<=if_sent<55:
            sent = "中级"
        else:
            sent = "消极"
        data["sent"] = sent
        data["sent_num"] = if_sent 
       
        item = json.dumps(data,ensure_ascii=False)
        return item
#if __name__=="__main__":
a = """原标题：北京市外办：北京市解除与捷克布拉格市友城关系
    
    2018年11月以来，捷克布拉格市新一届市政当局主要官员等人，无视国际关系基本准则和国际社会共识，不顾中方严正立场和强烈反对，屡屡在台湾、涉藏等涉及中方核心利益的重大问题上采取错误行动并发表不当言论。
    
    新京报快讯（记者 沙雪良）北京市人民政府外事办公室10月9日发布声明，北京市解除与捷克布拉格市友城关系。
    
    北京市外办在声明中称，2018年11月以来，捷克布拉格市新一届市政当局主要官员等人，无视国际关系基本准则和国际社会共识，不顾中方严正立场和强烈反对，屡屡在台湾、涉藏等涉及中方核心利益的重大问题上采取错误行动并发表不当言论，粗暴干涉中国内政，公然挑战同北京市的友城关系，造成恶劣影响，北京市对此表示严正抗议！考虑到两市开展交往的政治前提和基础已不复存在，北京市人民政府授权北京市人民政府外事办公室郑重声明：北京市立即解除与布拉格市友城关系并暂停一切官方往来。希望布拉格市有关人员早日认识错误，以实际行动消除负面影响。
    布拉格是捷克共和国的首都和最大的城市。北京市政府外办网站相关资料显示，2016年3月，北京与布拉格正式缔结友好城市关系，并在旅游、文化、教育、卫生等方面进行了一系列交流合作。
    
    此前，北京市外办9月12日曾发布消息，北京市与56个城市缔结了友好城市关系，分布在五大洲51个国家，其中多数是首都。北京市外办网站相关信息显示，北京市的友城包括日本东京、韩国首尔、俄罗斯莫斯科、德国柏林、希腊雅典、埃及开罗、美国纽约、巴西里约热内卢、澳大利亚堪培拉等。
    新京报记者 沙雪良
    
    编辑 樊一婧 校对 李立军 柳宝庆"""
nlp = NLP_server(a)
#print ("data:",nlp.index())
