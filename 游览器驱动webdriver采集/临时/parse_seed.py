# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin

from PyQt5.QtWidgets import *
import sys


a = "Anhui|Xuancheng|Suzhou|Wuhu|Tongling|Maanshan|Liuan| Huangshan|Huainan|Huaibei|Hefei|Fuyang|Chuzhou|Chizhou|Haozhou|Bengbu|Anqing|马鞍山|淮北|铜陵|安庆|黄山|阜阳|宿州|滁州|六安|宣城|池州|亳州|合肥|芜湖|蚌埠|淮南|安徽|馬鞍山|銅陵|安慶|阜陽|滁州|蕪湖|安清|福陽|中州|玄城|武湖|마안산|화이북|통링|안칭|황산|푸양|쑤저우|추저우|루안|쉬안청|츠저우|보저우|허페이|우후|벵부|화이난|안후이"
b = "manufacture|innovation|artificial intelligence|AI|technology|information |echnology|IT|speech technology|capital|invest|investment|IFLYTEK|iflytek|smart city|smart cities|High-end Equipment Manufacturing|high-end equipment manufacturing|smart appliances|life and health|green food|digital creativity|Anhui Intelligent Manufacturing|New Energy Vehicles|Automotive Intelligent Networking|Integrated Circuits|Information Technology|Intelligent Voice|Smart Wearable Devices|New Materials|Energy Saving and Environmental Protection|Equipment Manufacturing|Biology|New Energy|NIO|Changxin Storage|Quantum|Manufacturing|Innovation|HKUST iFlytek|Photovoltaic Glass|Cell|Integrated Circuit|New Display Device|Structural Material|Dynamic Memory Chip|New Material|Ultra-thin Glass|Mozihao|9 Chapter|Zuchongzhihao|Artificial Sun|BYD|AVIC Lithium Battery|Funeng Technology|Honeycomb Energy|Glass New Material|Huami Technology|NIO|Changxin|Jianghuai|Chery|Conch|Tongling Nonferrous|Maanshan Steel|Lianbao|Huaibei mining|制造|创新|人工智能|科技|信息技术|语音|资本|讯飞|智慧城市|高端装备制造|智能家电|生命健康|绿色食品|数字创意|安徽智能制造|新能源汽车|汽车智能网联|集成电路|信息技术|智能语音|智能可穿戴设备|新材料|节能环保|装备制造|生物|新能源|蔚来汽车|长鑫存储|量子|制造|创新|科大讯飞|光伏玻璃|电池片|集成电路|新型显示器件|结构材料|动态存储芯片|新材料|超薄玻璃|墨子号|九章|祖冲之号|人造太阳|比亚迪|中航锂电|孚能科技|蜂巢能源|玻璃新材料|华米科技|蔚来|长鑫|江淮|奇瑞|海螺|铜陵有色|马钢|联宝|淮北矿业|蔚來汽車|長鑫存儲|製造|創新|科大訊飛|光伏玻璃|電池片|集成電路|新型顯示器件|結構材料|動態存儲芯片|墨子號|祖沖之號|人造太陽|比亞迪|中航鋰電|孚能科技|蜂巢能源|華米科技|蔚來|長鑫|銅陵有色|馬鋼|聯寶|淮北礦業|安徽智能製造|新能源汽車|汽車智能網聯|集成電路|信息技術|智能語音|智能可穿戴設備|新材料|節能環保|裝備製造|生物|新能源|製造|創新|資訊技術|語音|資本|訊飛|高端裝備製造|智慧家電|綠色食品|數位創意|製造| AVICリチウム電池| Funengテクノロジー|ハニカムエネルギー|ガラス新素材| Huamiテクノロジー|イノベーション|人工知能|テクノロジー|情報技術|音声|資本| Xunfei |スマートシティ|ハイエンド機器製造|スマートアプライアンス|生活と健康|グリーンフード|デジタル創造性|Anhuiインテリジェントマニュファクチャリング|新エネルギー車|自動車インテリジェントネットワーキング|集積回路|情報技術|インテリジェントボイス|スマートウェアラブルデバイス|新素材|省エネと​​環境保護|機器製造|生物学|新エネルギー|Anhui Intelligent Manufacturing|신에너지 차량|자동차 지능형 네트워킹|집적 회로|정보 기술|지능형 음성|스마트 웨어러블 기기|신소재|에너지 절약 및 환경 보호|장비 제조|생물학|신에너지제조|혁신|인공 지능|기술|정보 기술|음성|자본|Xunfei|스마트 시티|고급 장비 제조|스마트 가전|생활과 건강|친환경 식품|디지털 창의력|양자|제조|혁신|태양광 유리|셀|집적 회로|새로운 디스플레이 장치|구조 재료|동적 메모리 칩|신소재|초박형 유리|인공 태양 | 리튬 배터리|유리 신소재|Huaibei 광산"

def parse_keyword_list():
    a = "Anhui|Xuancheng|Suzhou|Wuhu|Tongling|Maanshan|Liuan| Huangshan|Huainan|Huaibei|Hefei|Fuyang|Chuzhou|Chizhou|Haozhou|Bengbu|Anqing|马鞍山|淮北|铜陵|安庆|黄山|阜阳|宿州|滁州|六安|宣城|池州|亳州|合肥|芜湖|蚌埠|淮南|安徽|馬鞍山|銅陵|安慶|阜陽|滁州|蕪湖|安清|福陽|中州|玄城|武湖|마안산|화이북|통링|안칭|황산|푸양|쑤저우|추저우|루안|쉬안청|츠저우|보저우|허페이|우후|벵부|화이난|안후이"
    b = "manufacture|innovation|artificial intelligence|AI|technology|information |echnology|IT|speech technology|capital|invest|investment|IFLYTEK|iflytek|smart city|smart cities|High-end Equipment Manufacturing|high-end equipment manufacturing|smart appliances|life and health|green food|digital creativity|Anhui Intelligent Manufacturing|New Energy Vehicles|Automotive Intelligent Networking|Integrated Circuits|Information Technology|Intelligent Voice|Smart Wearable Devices|New Materials|Energy Saving and Environmental Protection|Equipment Manufacturing|Biology|New Energy|NIO|Changxin Storage|Quantum|Manufacturing|Innovation|HKUST iFlytek|Photovoltaic Glass|Cell|Integrated Circuit|New Display Device|Structural Material|Dynamic Memory Chip|New Material|Ultra-thin Glass|Mozihao|9 Chapter|Zuchongzhihao|Artificial Sun|BYD|AVIC Lithium Battery|Funeng Technology|Honeycomb Energy|Glass New Material|Huami Technology|NIO|Changxin|Jianghuai|Chery|Conch|Tongling Nonferrous|Maanshan Steel|Lianbao|Huaibei mining|制造|创新|人工智能|科技|信息技术|语音|资本|讯飞|智慧城市|高端装备制造|智能家电|生命健康|绿色食品|数字创意|安徽智能制造|新能源汽车|汽车智能网联|集成电路|信息技术|智能语音|智能可穿戴设备|新材料|节能环保|装备制造|生物|新能源|蔚来汽车|长鑫存储|量子|制造|创新|科大讯飞|光伏玻璃|电池片|集成电路|新型显示器件|结构材料|动态存储芯片|新材料|超薄玻璃|墨子号|九章|祖冲之号|人造太阳|比亚迪|中航锂电|孚能科技|蜂巢能源|玻璃新材料|华米科技|蔚来|长鑫|江淮|奇瑞|海螺|铜陵有色|马钢|联宝|淮北矿业|蔚來汽車|長鑫存儲|製造|創新|科大訊飛|光伏玻璃|電池片|集成電路|新型顯示器件|結構材料|動態存儲芯片|墨子號|祖沖之號|人造太陽|比亞迪|中航鋰電|孚能科技|蜂巢能源|華米科技|蔚來|長鑫|銅陵有色|馬鋼|聯寶|淮北礦業|安徽智能製造|新能源汽車|汽車智能網聯|集成電路|信息技術|智能語音|智能可穿戴設備|新材料|節能環保|裝備製造|生物|新能源|製造|創新|資訊技術|語音|資本|訊飛|高端裝備製造|智慧家電|綠色食品|數位創意|製造| AVICリチウム電池| Funengテクノロジー|ハニカムエネルギー|ガラス新素材| Huamiテクノロジー|イノベーション|人工知能|テクノロジー|情報技術|音声|資本| Xunfei |スマートシティ|ハイエンド機器製造|スマートアプライアンス|生活と健康|グリーンフード|デジタル創造性|Anhuiインテリジェントマニュファクチャリング|新エネルギー車|自動車インテリジェントネットワーキング|集積回路|情報技術|インテリジェントボイス|スマートウェアラブルデバイス|新素材|省エネと​​環境保護|機器製造|生物学|新エネルギー|Anhui Intelligent Manufacturing|신에너지 차량|자동차 지능형 네트워킹|집적 회로|정보 기술|지능형 음성|스마트 웨어러블 기기|신소재|에너지 절약 및 환경 보호|장비 제조|생물학|신에너지제조|혁신|인공 지능|기술|정보 기술|음성|자본|Xunfei|스마트 시티|고급 장비 제조|스마트 가전|생활과 건강|친환경 식품|디지털 창의력|양자|제조|혁신|태양광 유리|셀|집적 회로|새로운 디스플레이 장치|구조 재료|동적 메모리 칩|신소재|초박형 유리|인공 태양 | 리튬 배터리|유리 신소재|Huaibei 광산"

    a = a.split("|")
    b = b.split("|")
    print(len(a))
    print(len(b))
    for aa in a:
        for bb in b:
            print(aa+" & "+bb)
if __name__ == '__main__':
    parse_keyword_list()
