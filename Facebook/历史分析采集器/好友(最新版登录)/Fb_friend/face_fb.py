from facebook_scraper import get_posts,get_profile

from FaceBookLogin import Facebook_Login
cookie = Facebook_Login().login("by951118@163.com","golaxy@321")
for i in get_profile("preaudience",cookie):
    print(i)