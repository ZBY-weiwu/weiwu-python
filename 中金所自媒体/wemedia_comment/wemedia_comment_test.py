from fake_useragent import UserAgent

ua = UserAgent(path=r".\wemedia_comment\Tools\useragent.json")
if __name__ == '__main__':
    detail_headers = {"User-Agent": ua.chrome}
    print(detail_headers)