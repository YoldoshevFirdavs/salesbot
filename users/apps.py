# # from django.apps import AppConfig
# #
# #
# # class UsersConfig(AppConfig):
# #     default_auto_field = "django.db.models.BigAutoField"
# #     name = "users"
# import requests
#
# url = "https://mock-sms.zunoy.com/sms/new/message"
# headers = {
#   "Content-Type": "application/json",
#   "Authorization": "p5jGroqzy"
# }
#
# payload = {
#   "message": "Hello My name is Yo'ldashev Firdavs",
#   "sender": "Firdavs"
# }
#
# response = requests.post(url, json=payload, headers=headers)
# print(response.json())