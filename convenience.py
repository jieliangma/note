#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import pyqrcode
import base64
import re
import uuid
import os
import time


"""需要安装 pyqrcode """


class FreeShadowsocksQRCode(object):
  """docstring for FreeShadowsocksQRCode"""
  def __init__(self, cmd):
    super(FreeShadowsocksQRCode, self).__init__()
    self.cmd = cmd
    self.content = ''

  """获取执行命令后，得到的返回值"""
  def chart(self):
    if len(self.content) > 0:
      return self.content

    return_code, output = commands.getstatusoutput(self.cmd)

    if return_code != 0:
      print 'excute free-shadowsocks return ' + str(return_code)
      return ''

    self.content = output
    return output

  """获取一条记录"""
  def record(self):
    content = self.chart()

    if len(content) > 0:
      match = re.search(r'│\s*((\w*\.){2}\w*)\s*│\s*(\d+)+\s*│\s*(\d+)+\s*│\s*(\S+)\s*│', content)

      if match:
        host = match.group(1)
        port = match.group(3)
        password = match.group(4)
        method = match.group(5)
        return (host, port, password, method)
    return ('', '', '', '')

  """把记录转换成 URL """
  """https://github.com/shadowsocks/shadowsocks/wiki/Generate-QR-Code-for-Android-or-iOS-Clients"""
  def make_url(self):
    host, port, password, method = self.record()

    if len(host) == 0 or len(port) == 0 or len(password) == 0 or len(method) == 0:
      print 'no record!'
      return

    url = method + ':' + password + '@' + host + ':' + port
    base64_url = base64.b64encode(url)
    final_url = 'ss://' + base64_url
    return final_url

  """根据 URL 生成二维码，调用系统命令打开图片然后删除图片"""
  def show_url(self, url):
    if len(url) == 0:
      print 'Invalid url'
      return
    qrcode = pyqrcode.create(url)
    file_name = '/tmp/' + str(uuid.uuid1()) + '.eps'

    qrcode.eps(file_name, scale=8)
    return_code, _ = commands.getstatusoutput('open ' + file_name)

    """休眠1秒，确保图片被打开"""
    time.sleep(1)

    if return_code == 0:
      os.remove(file_name)

def main():
  qrcode = FreeShadowsocksQRCode('free-shadowsocks')
  qrcode.show_url(qrcode.make_url())

if __name__ == '__main__':
  main()