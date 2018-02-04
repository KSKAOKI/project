#! /usr/bin/env python

import sys
import os
import re
from datetime import datetime

args = sys.argv
arg_date = '^\d{4}/\d{1,2}/\d{1,2}$'

#コマンドライン引数の処理
if len(args) == 1:
	pass
elif len(args) == 3 and re.match(arg_date, args[1]) and re.match(arg_date, args[2]):
	splt_from = args[1].split('/')
	splt_to = args[2].split('/')
	term_from = datetime(int(splt_from[0]), int(splt_from[1]), int(splt_from[2]))
	term_to = datetime(int(splt_to[0]), int(splt_to[1]), int(splt_to[2]))
	if term_from > term_to:
		sys.exit('期間の終了日は開始日より遅い日付を入力してください')
else:
	sys.exit('不正な引数があります')

#ログファイルを一覧表示
path = '/var/log/httpd/'
num = 1  #ファイル番号
files = {}  #{ファイル番号:ファイル名}
if not os.path.isdir(path):
	sys.exit('ディレクトリが存在しません')
elif os.listdir(path) == []:
	sys.exit('ファイルが存在しません')
print('/var/log/httpd/')
for file in os.listdir(path):
	if os.path.isfile(path + file):
		files[num] = file
		print('{}. {}'.format(num, file))
		num += 1
		
#読み込むログファイルを選択
access_log = []
print('アクセスログ(番号)を選択してください (end:入力終了)')
while True:
	i = input('>> ')
	if i == 'end':
		break
	elif i.isdigit() and int(i) in files:
		access_log.append(files[int(i)])
	else:
		print('番号が間違っています')
if access_log == []:
	sys.exit('ファイルが選択されませんでした')

#集計の方法を選択 time:時間帯別 host:リモートホスト別
print('集計の種類を選択してください　time/host')
while True:
	j = input('>> ')
	if j!='time' and j!='host':
		print('timeまたはhostを入力してください')
	else:
		break
		
#正規表現一覧 --ログから特定情報を抽出
date = re.compile('\d{2}/[a-zA-Z]{3}/\d{4}')  #日付(day/month/year)
time = re.compile(':\d{2}:\d{2}:\d{2}')	 #時刻(:hour:minute:second)
remote_host = re.compile('(\d{1,3}\.){3}\d{1,3}')  #リモートホスト

#時間帯及びリモートホストの辞書 {時間帯/ホスト:件数}
remote_host_dict = {}
hour_dict = {}
for hour in range(24):  #{'00':0 ~ '23':0}
	hour_str = '{0:02d}'.format(hour)
	hour_dict[hour_str] = 0
	
#月の英語-数字対応辞書
month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, \
		 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

num_of_access = 0 #アクセス数をカウント

for log_file in access_log:
	with open('/var/log/httpd/' + log_file, 'r', encoding='UTF-8') as f:		
		for line in f:			
			#日付チェック
			if len(args) == 1:  #引数なしの場合
				pass
			else:
				date_log = re.search(date, line).group()  #day/month/year
				splt_date = date_log.split('/')
				splt_date[1] = month[splt_date[1]] #月の英語を数字に変換
				date_log = datetime(int(splt_date[2]), splt_date[1], int(splt_date[0]))
			
			#時間帯毎のアクセス件数集計
			time_log = re.search(time, line).group()  #hour:minute:second
			splt_time = time_log.split(':')
			if len(args) == 1 or term_from <= date_log <= term_to:
				hour_dict[splt_time[1]] += 1
				num_of_access += 1
			else:
				pass
			
			#リモートホスト別のアクセス件数集計
			remote_host_log = re.search(remote_host, line).group()  #IPアドレス
			if len(args) == 1 or term_from <= date_log <= term_to:
				if remote_host_log not in remote_host_dict:
					remote_host_dict[remote_host_log] = 1
				else:
					remote_host_dict[remote_host_log] += 1
			else:
				pass

#辞書をソート
hour_dict = sorted(hour_dict.items())	 #時間帯昇順
remote_host_dict = sorted(remote_host_dict.items(), key=lambda x:-x[1])  #アクセス件数降順

#指定期間を表示
if len(args) == 3:
	print('\nーーー{}年{}月{}日〜{}年{}月{}日ーーー' \
	.format(splt_from[0], splt_from[1], splt_from[2], splt_to[0], splt_to[1], splt_to[2]))
		
#総アクセス件数を表示									  
print('\n総アクセス件数：{}件'.format(num_of_access))

#各時間帯毎のアクセス件数を表示
if j == 'time':
	print('\n各時間帯毎のアクセス件数')
	for k, v in hour_dict:
		v  = '{0:4d}'.format(v)
		k2 = '{0:02d}'.format(int(k)+1)
		bar='■' * int(v)
		if int(v) > 50:
			bar='■' * 50
		print('{}:00~{}:00 | {}件 {}'.format(k, k2, v, bar))

#リモートホスト別のアクセス件数を表示
if j == 'host':
	print('\nリモートホスト別のアクセス件数')
	n = 0
	for k, v in remote_host_dict:
		n  = '{0:4d}'.format(int(n)+1)
		v  = '{0:4d}'.format(v)
		k  = '{0:15s}'.format(k)
		bar='■' * int(v)
		if int(v) > 50:
			bar='■' * 50
		print('{}: {}|{}件 {}'.format(n, k, v, bar))
