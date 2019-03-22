# import requests
# from bs4 import BeautifulSoup

# from sachima import conf


# class Publisher(object):
#     @classmethod
#     def get_csrf_token(self, html):
#         soup = BeautifulSoup(html, "html.parser")
#         csrf = soup.find(id="csrf_token").attrs["value"]
#         return csrf

#     @classmethod
#     def to_superset(self, name, type_, param):
#         addr = conf.get("SUPERSET_WEBSERVER_ADDRESS")
#         port = conf.get("SUPERSET_WEBSERVER_PORT")
#         user = conf.get("SUPERSET_USERNAME")
#         pwd = conf.get("SUPERSET_PASSWORD")
#         bp_post = conf.get("SUPERSET_API_TABLE_BP")
#         if addr and port:
#             url = ":".join([addr.rstrip("/"), str(port)])
#             with requests.session() as s:
#                 # 登陆
#                 r = s.get(url + "/login/")

#                 login_data = dict(
#                     username=user,
#                     password=pwd,
#                     csrf_token=self.get_csrf_token(r.text),
#                 )
#                 r = s.post(url + "/login/", data=login_data)

#                 # 调用接口
#                 if r.url.endswith("welcome"):
#                     r = s.post(
#                         url + bp_post,
#                         headers={
#                             "Content-Type": "application/json; charset=utf-8",
#                             "X-CSRFToken": self.get_csrf_token(r.text),
#                         },
#                         json={
#                             "slice_name": name,
#                             "api": type_,
#                             "params": param,
#                         },
#                     )
#                     print(r.text)
#                     print("publish service to superset")
#         else:
#             pass
