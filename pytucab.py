
#############################################################
#							Welcome							#
#	Tsinghua University Lib-reservation System in Python	#
#						 Version: v1.0 						#
#						Date: 2015/04/07					#
#			By: Haoyu hu	Email: im@huhaoyu.com			#
#				Address: Tsinghua University				#
#############################################################

import http.cookiejar, urllib.request, urllib.parse
import getpass, re, getopt
import time, sys, codecs, os

version = '1.0'
#########################################################
#					File I/O helper						#
#########################################################

def create_path(relative_path):
 	base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
 	return os.path.join(base_path, relative_path)

#########################################################
#					Assistance Function					#
#########################################################

def current_time():
	return str(int(time.time() * 1000))

def time_is_correct(s, e):
	sfront, sback = s.split(':')
	efront, eback = e.split(':')
	st = int(sfront) * 60 + int(sback)
	et = int(efront) * 60 + int(eback)
	if et - st <= 240 and et - st >= 30 and st >= 800 and et <= 2200:
		return True
	else:
		return False

def get_response(url):
	response = urllib.request.urlopen(url)
	return response.read().decode()

def is_leap(year):
	if year % 400 == 0 or year % 100 != 0 and year % 4 == 0:
		return 0
	else:
		return 1

def latest_date():
	m = [[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]
	date = time.strftime('%Y %m %d')
	year, month, day = date.split(' ')
	year, month, day = int(year), int(month), int(day)
	day += 2
	flag = is_leap(year)
	if day > m[flag][month]:
		day -= m[flag][month]
		month += 1
		if month > 12:
			month -= 12
			year += 1
	if month in range(1, 10):
		month = '0' + str(month)
	else:
		month = str(month)
	if day in range(1, 10):
		day = '0' + str(day)
	date = str(year) + month + day
	return date

#########################################################
#					Input Function						#
#########################################################

def input_room_id(delete_or_modify, use):
	room = ''
	is_correct = False
	str = ''
	if delete_or_modify:
		str = 'DELETE'
	else:
		str = 'MODIFY'

	while not is_correct:
		index = input('Which one do you want to %s, please input the INDEX(q to quit): ' %str)
		if index == 'q':
			print ('NOW QUIT THE CAB-SYSTEM...')
			cab_logout()
			sys.exit(0)
		index = int(index)
		if index in range(1, len(use) + 1):
			room = use[index]
			is_correct = True
		if (not is_correct):
			print ('INDEX INVALID, PLEASE INPUT AGAIN!\n')

	return room, index

def input_time(start_or_end):
	time = ''
	is_correct = False
	str = ''
	if start_or_end:
		str = 'START'
	else:
		str = 'END'

	while (not is_correct):
		time = input('Please input %s time(q to quit): ' %str)
		if time == 'q':
			print ('NOW QUIT THE CAB-SYSTEM...')
			cab_logout()
			sys.exit(0)
		if re.search('\d{2}:\d{2}', time) != None:
			break
		print ('INPUT INVALID, PLEASE INPUT AGAIN!\n')

	return time

#########################################################
#				Main Login/Logout Modules				#
#########################################################

def cab_login(username, password):
	front = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/pro/ajax/login.aspx?act=login&id='
	mid = '&pwd='
	rear = '&_='
	url = front + username + mid + password + rear + current_time()

	cookie = http.cookiejar.CookieJar()
	cookie_proc = urllib.request.HTTPCookieProcessor(cookie)
	urllib.request.install_opener(urllib.request.build_opener(cookie_proc))
	ret = get_response(url)
	
	if re.search('操作成功', ret) == None:
		print ('YOUR USERNAME OR PASSWORD IS INCORRECT, OR YOUR USER-ACCOUNT NEEDS ACTIVATION.')
		sys.exit(1)

	nm_dp = re.findall('[\u4e00-\u9fa5]+', ret)
	std_id = re.findall('\d{10}', ret)
	phone = re.findall('\d{11}', ret)
	email = re.findall('\w+@\w+\.\w+', ret)

	print ('**PERSONAL INFOMATION**')
	print ('Name:', nm_dp[0], '\tDepartment:', nm_dp[1], '\tStudent ID:', std_id[0], '\nPhone Number:', phone[0], '\tEmail:', email[0])
	print ()

def cab_logout():
	url = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/pro/ajax/login.aspx?act=logout&_='
	url = url + current_time()

	ret = get_response(url)

#########################################################
#					Main Query Modules					#
#########################################################

def cab_query(do_display, date):
	#query_url
	url = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/xcus/ic/my.aspx'
	raw = get_response(url)
	
	#data process
	match = re.findall('[\u4E00-\u9FA5]+|\d{6}|\d{4}-\d{2}-\d{2} \d{2}:\d{2}|\w\d-\d{2}', raw)
	use_group = {}
	info_group = {}
	room = ''
	infomation = ''
	username = ''
	count = 0
	index = 1

	for key in match:
		if key == '提前结束' or key == '预约违约':
			break
		elif re.search('F\d-\d{2}', key) != None:
			infomation += key + '\t\t'
			count += 1
		elif re.search('\d{6}', key) != None and count == 1:
			room = key
			use_group[index] = room
			count += 1
		elif re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', key) != None and count == 2:
			infomation += key + '\t'
			count += 1
		elif re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', key) != None and count == 3:
			infomation += key
			info_group[index] = infomation
			infomation = ''
			index += 1
			count = 0

	if do_display:
		#exception
		if (info_group == {}):
			print ('NO RESERVATION INFOMATION!')
			cab_logout()
			sys.exit(1)

		#print data
		print ('**RESERVATION INFOMATION**')
		print ('INDEX\tROOM ID\t\tSTART TIME\t\tEND TIME')
		for item in info_group:
			print (item, '\t', info_group[item])
		print ()
			
		#return index match roomID
		return use_group, info_group
	else:
		tdate = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
		for index in info_group:
			if re.search(tdate, info_group[index]) != None:
				return True, info_group[index]
		return False, ''

#########################################################
#				Main Application Modules				#
#########################################################

rooms = ['F2-18', 'F2-19', 'F2-15', 'F2-14', 'F2-22', 'F2-23', 'F2-24', 'F2-10', 'F2-16', 'F2-17', 'F2-20', 'F2-21', 'F2-13', 'F2-11', 'F2-29', 'F2-30']
rm_id = ['10384', '10388', '10366', '10360', '10400', '10404', '10408', '10344', '10370', '10380', '10392', '10396', '10352', '10348', '10412', '10416']

def read_post_data(room_id, date, start):
	url = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/xcus/ic/space_Resvset.aspx?'
	info = {'devkind': '10310', 'dev': room_id, 'date': date, 'time': start, 'labid': '10319'}
	url = url + urllib.parse.urlencode(info)
	ret = get_response(url)
	strlist = re.findall('__VIEWSTATE.+?/>', ret)
	ret = strlist[0]
	data = ''
	begin = False

	for i in range(0, len(ret) - 4):
		if ret[i] == '/':
			begin = True
			data += ret[i]
		elif begin:
			data += ret[i]

	return data

def cab_apply(s, e, date):
	is_found, rec = cab_query(False, date)
	if is_found:
		rec = re.sub('[\t]+', ' ', rec)
		print ('YOU HAVE A RESERVATION THAT DAY, YOUR RESERVATION IS:\n', rec)
		print ('YOU CAN MODIFY OR DELETE IT IF YOU WANT')
		return True
	print ('CAB-SYSTEM IS SEARCHING FOR THE BEST READING-ROOM, PLEASE WAIT A MOMENT...')
	for i in range(len(rooms)):
		#prepare url
		room_id = rm_id[i]
		info = {'devkind': '10310', 'dev': room_id, 'date': date, 'time': s, 'labid': '10319'}
		url = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/xcus/ic/space_Resvset.aspx?'
		url += urllib.parse.urlencode(info)

		start = re.sub(':', '', s)
		end = re.sub(':', '', e)

		#prepare post_data
		post = urllib.parse.urlencode({'__VIEWSTATE': read_post_data(room_id, date, s)})
		dpart1 = '__EVENTTARGET=Sub&__EVENTARGUMENT=&'
		dpart2 = '&__VIEWSTATEGENERATOR=09754CED&open_start=08%3A00&open_end=22%3A00&latest=0&earliest=2880&min=30&max=240&t_unit=10&need_file=&old_start=&old_end=&cls_time=&ddlHourStart='
		dpart3 = '&ddlHourEnd='
		dpart4 = '&tempHourEnd=&startDate=&endDate=&txtPerson=&groupIDHidden=&ic_file_name=&up_file=&txtMemo='
		post_data = dpart1 + post + dpart2 + start + dpart3 + end + dpart4

		#request
		request = urllib.request.Request(url, post_data.encode())
		response = urllib.request.urlopen(request)
		
		#found or not
		is_found, rec = cab_query(False, date)
		if is_found:
			rec = re.sub('[\t]+', ' ', rec)
			print ('APPLY SUCCESS, YOUR RESERVATION IS: ', rec)
			return True

	print ('LIBRARY IS FULL')
	return False

#########################################################
#			Main Modification/Delete Modules			#
#########################################################

def cab_modify():
	#prepare
	part1 = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/pro/ajax/reserve.aspx?resv_id='
	part2 = '&start='
	part3 = '&end='
	part4 = '&start_time='
	part5 = '&end_time='
	part6 = '&act=set_resv&_='
	use, info = cab_query(True, '')

	#get the roomID that user wants to modify
	room, index = input_room_id(False, use)

	#get the new start time and end time
	while (True):
		s = input_time(True)
		e = input_time(False)
		if time_is_correct(s, e):
			break
		print ('\nTIME INVALID!')
		print ('TIME MUST BE BETWEEN 8:00 ~ 22:00, AND TIME INTERVAL MUST BE BETWEEN 0.5 ~ 4 HOURS.\n')

	#data process
	match = re.search('\d{4}-\d{2}-\d{2}', info[index])
	date = match.group()
	start = date + '+' + re.sub(':', '%3A', s)
	end   = date + '+' + re.sub(':', '%3A', e)
	start_time = re.sub(':', '', s)
	end_time   = re.sub(':', '', e)

	#request
	url = part1 + room + part2 + start + part3 + end + part4 + start_time + part5 + end_time + part6 + current_time()
	ret = get_response(url)
	if re.search('操作成功', ret) != None:
		match = re.search('F\d-\d{2}', info[index])
		print ('\nYOU HAVE MODIFY THE RESERVATION OF ROOM: %s FROM %s --> %s' %(match.group(), s, e))
	else:
		print ('\nUNKNOWN ERROR LEAD TO MODIFICATION FAILURE, PLEASE TRY AGAIN')

def cab_delete():
	#prepare and query
	front = 'http://cab.hs.lib.tsinghua.edu.cn/ClientWeb/pro/ajax/reserve.aspx?act=del_resv&id='
	rear  = '&_='
	use, info = cab_query(True, '')

	#get the roomID that user wants to delete 
	room, index = input_room_id(True, use)

	#delete
	url = front + room + rear + current_time()
	ret = get_response(url)
	if re.search('操作成功', ret) != None:
		match = re.search('F\d-\d{2}', info[index])
		print ('YOU HAVE DELETED THE RESERVATION OF ROOM: ', match.group())
	else:
		print ('\nUNKNOWN ERROR LEAD TO DELETE FAILURE, PLEASE TRY AGAIN')

#########################################################
#						Ohter Function					#
#########################################################

def cab_help():
	print ('-h, --help   : show all options of Tsinghua University Library Reservation System')
	print ('-v, --version: show version of Tsinghua University Library Reservation System')
	print ('-a           : enter username and password later, you can login other account')
	print ('-q, --query  : query reservation details')
	print ('-d, --delete : delete your reservation later')
	print ('-m, --modify : modify your reservation later')
	print ('-t           : enter date and time later. default value: date(%s), start time(17:30), end time(21:30)' % time.strftime('%Y%m%d'))

def cab_version():
	print ('Tsinghua University Library Reservation System Version: %s' %version)

def cab_others():
	print ('UNKNOWN OPTIONS')
	print ('WHICH OPTION DO YOU WANT?')
	cab_help()
	print ('IF ANY ERROR, PLEASE CONTACT im@huhaoyu.com.')

#########################################################
#						Main Part						#
#########################################################

def pytucab():
	#get default username/password/date/start_time/end_time
	date = latest_date()
	relative_path = 'USERNAME_PASSWORD.txt'
	file_handler = open(create_path(relative_path), 'r')
	lines = file_handler.readlines()
	if len(lines) != 4:
		print('%s IS DAMAGED, PLEASE CHECK THE CONTENT FORMAT IN THE FILE:' %relative_path)
		print('CONTENT FORMAT AS FOLLOWS:')
		print('username=2014210130\npassword=123456\nstart_time=17:30\nend_time=21:30')
		sys.exit(1)
	username = re.sub('\s', '', lines[0])
	password = re.sub('\s', '', lines[1])
	s = re.sub('\s', '', lines[2])
	e = re.sub('\s', '', lines[3])
	_, username = username.split('=')
	_, password = password.split('=')
	_, s = s.split('=')
	_, e = e.split('=')
	file_handler.close()

	if not time_is_correct(s, e):
		print ('THE DEFAULT TIME SETTING IS INVALID, PLEASE CHANGE THE VALUE (FORMAT: 09:30, 21:40)')
		sys.exit(1)

	try:
		options, args = getopt.getopt(sys.argv[1:], 'adthmqv', ['help', 'version', 'query', 'modify', 'delete'])
	except getopt.GetoptError:
		cab_others()
		sys.exit(1)

	want_query = False
	input_user = False
	input_time = False
	want_modify = False
	want_delete = False
	name, value = None, None

	for name, value in options:
		if name in ('-h', '--help'):
			cab_help()
			sys.exit(0)
		elif name in ('-v', '--version'):
			cab_version()
			sys.exit(0)
		elif name == '-a':
			input_user = True
		elif name in ('-q', '--query'):
			want_query = True
		elif name in ('-m', '--modify'):
			want_modify = True
		elif name in ('-d', '--delete'):
			want_delete = True
		elif name == '-t':
			input_time = True

	if input_user:
		username = input('username: ')
		password = getpass.getpass('password: ')

	if input_time:
		is_correct = False
		while not is_correct:
			is_correct = True
			print ('PLEASE INPUT DATETIME AS FOLLOWS (ENTER USE DEFAULT VALUE):')
			print ('date: 0407 \nstart time: 17:30\nend time: 21:30')
			date = input('date: ')
			if date != '':
				date = time.strftime('%Y') + date
			st = input('start time: ')
			if st != '':
				s = st
			ed = input('end time: ')
			if ed != '':
				e = ed
			if not time_is_correct(s, e):
				is_correct = False
				print ('INPUT ERROR!\n')

	print('FETCHING DATA FROM http://cab.hs.lib.tsinghua.edu.cn, PLEASE WAIT A MOMENT...\n')
	#login
	cab_login(username, password)

	#operation
	if want_delete:
		cab_delete()
	elif want_query:
		cab_query(True, '')
	elif want_modify:
		cab_modify()
	else:		
		cab_apply(s, e, date)

	#logout
	cab_logout()

if __name__ == '__main__':
	pytucab()
