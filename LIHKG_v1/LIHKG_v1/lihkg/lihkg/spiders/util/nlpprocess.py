#!/usr/bin/env python    
# -*- coding: UTF-8 -*-
import sys    
import requests
import json
import base64

class NlpProcess:
	def __init__(self):
		pass

	def process(self, lng, content):
		d = []
		d.append(content)
		url=""
		if lng=='zh':
			url="http://10.20.18.2:8087/golaxy/nlp/synthesisBasic/chinese/v1"
		else :
			url="http://10.20.18.2:8087/golaxy/nlp/synthesisBasic/english/v1"

		header={'Content-Type: application/json','Accept: application/json'}
		r = requests.post(url, data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
		d = json.loads(r.text)
	        #print r.text.encode('utf-8','ignore')
		if(d['message'] == 'success'):
			return d['synthesisBasicResults']
		else:
			return False

if __name__ == "__main__":
	nlp = NlpProcess()
#	text="记者：据报道，日本岩波书店出版的国民辞典在地图中把台湾标注为中华人民共和国的一个省，“台北驻日经济文化代表处”要求岩波书店改正错误。中方对此如何评论？\n　　外交部发言人  华春莹：\n　　台湾难道不是中国的一个省吗？众所周知，台湾是中国领土不可分割的一部分。\n　　外交部：赞赏西班牙奉行一个中国原则\n　　记者：据报道，16日，西班牙法庭作出裁决，将西班牙去年底逮捕的121名大陆和台湾的电信诈骗嫌犯引渡到中国大陆（无视想争取将人带回台湾的台当局抗议），法庭表示西班牙接受一个中国原则。中方对此有何评论？\n　　外交部发言人  华春莹：\n　　中方对西班牙法院作出上述裁决表示欢迎，这是中西两国根据引渡条约开展合作打击犯罪的重要成果。中方对西班牙坚定奉行一个中国原则，决定将台湾籍嫌犯引渡回中国表示高度赞赏。中西两国警方就共同打击涉华电信网络诈骗犯罪保持着密切合作，我们愿与西方共同努力，切实维护好人民群众的合法利益。"

	text="【文匯網訊】\n行政長官辦公室今日(十一月三日)公布，行政長官林鄭月娥在聘任委員會的建議下，委任香港特別行政區第五屆政府兩名政治助理。新獲委任的政治助理為財政司司長政治助理何翠萍和食物及衞生局局長政治助理鄭守崗，兩人將於本月六日履新。\n林鄭月娥說：「我已先後委任現屆政府全部十二名副局長和十四名政治助理。他們都是有心、有力、有承擔、願意為社會服務的人，負責協助司局長廣泛聯繫社會各界，加強行政和立法機關之間的溝通，積極從多渠道聆聽意見及解釋政府的政策和措施。我會領導政治委任團隊以有決心、敢創新，並努力做到無微不至的精神，為市民做實事，建設一個更美好的香港。」簡歷：\n{IMG:1}\n\n現年四十三歲。在加入政府前任職商業電台新聞及公共事務副總監，曾擔任香港新聞行政人員協會主席。她擁有香港浸會大學傳理學社會科學學士學位。\n{IMG:2}\n\n現年三十八歲。在加入政府前任職醫院管理局服務轉型部行政經理，負責策劃及推行臨床公私營協作計劃。他持有香港大學護理學學士及公共衞生碩士學位。責任編輯：于岄鳴"


	res=nlp.process('zh',text)
	data=res[0]
	wordSegmentations = data['wordSegmentations']
	keywords = data['keywords']
	namedEntityRecognitions = data['namedEntityRecognitions']
	sentiment = data['sentiment']
	summary = data['summary']

#	print "keywords:",json.dumps(keywords)

	tt=set()
	for i in keywords:#wordSegmentations:
		word=i['keyword']#.encode('utf-8','ignore')
		if len(word)>1:
			tt.add(word)#print word.encode('utf-8','ignore')
			print (word)
	
	d=[]
	for i in tt:
		d.append(i)
	print (json.dumps(d))
#	print summary.encode('utf-8','ignore')
#	print json.dumps(sentiment)
