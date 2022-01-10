import json
file_data =open("headers_config.txt", "r+", encoding="utf-8")
head_data = file_data.readlines()
# print(head_data)
item = {}
for data in head_data:
    data_list = data.split(":")
    # print(data_list)
    try:
        item[data_list[0]] = data_list[1].strip()
    except:
    
        item[data_list[0]] = ""
item_data = json.dumps(item,ensure_ascii=False)
print(item_data)

