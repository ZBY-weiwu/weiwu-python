import re
url = "https://m.facebook.com/preaudience/friends"
if re.findall("https://\w+\.facebook\.com/\w+/friends",url)[0]:
    print(True)