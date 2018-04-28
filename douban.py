import requests
import random
import getpass
from  PIL import Image
from html.parser import HTMLParser
from lxml import html

'''
	豆瓣登录:首先去拿一个会话（没有登录）,接下来按照浏览器的格式去发送post请求来登录
	        如果登录成功，这个时候session是已经登录的状态，然后去请求其他的分类。
	form_email:user
	form_password:password
'''


class DoubanClient():
	def __init__(self):
		self.session = requests.session()
		self.headers = {
			'Host': 'www.douban.com',
			'Origin': 'https://www.douban.com',
			'Referer': 'https://www.douban.com/',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
			# random.choice(user_agent.USER_AGENTS)
		}

	def login(self, username, password,
			  source='index_nav',
			  redir='https://www.douban.com/',
			  login='登录'
			  ):

		login_url = 'https://www.douban.com/accounts/login'

		resopnse = self.session.get(login_url)
		(captcha_id, captcha_url) = _get_captcha(resopnse.content)
		print('captcha_id为:{}'.format(captcha_id))
		if captcha_id:
			r = self.session.get(captcha_url)
			with open('captcha.jpg', 'wb') as f:
				f.write(r.content)

			try:
				im = Image.open('captcha.jpg')
				im.show()
				im.close()
			except:
				print('请输入验证码')
			captcha_solution = input('please input solution for captcha[{}]'.format(captcha_url))

			data = {
				'form_email': username,
				'form_password': password,
				'source': source,
				'redir': redir,
				'login': login}
			if captcha_id:
				data['captcha-id'] = captcha_id
				data['captcha-solution'] = captcha_solution

			self.session.post(login_url, data=data, headers=self.headers)

			#print(self.session.get('https://www.douban.com/').text)
	def get_content(self,comment,ck='H7zE'):#发送消息
		data={
			'ck':ck,
			'comment':comment
		}
		url='https://www.douban.com/'
		self.session.post(url,data=data,headers=self.headers)



def _attr(attrs, attrname):
	for attr in attrs:
		if attr[0] == attrname:
			return attr[1]
	return None


def _get_captcha(content):
	class CaptchaParse(HTMLParser):  # 解析网页的类
		def __init__(self):
			HTMLParser.__init__(self)
			self.captcha_id = None
			self.captcha_url = None

		def handle_starttag(self, tag, attrs):  # 标签、属性 id class name
			if tag == 'img' and _attr(attrs, 'id') == 'captcha_image' and _attr(attrs, 'class') == 'captcha_image':
				self.captcha_url = _attr(attrs, 'src')

			if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha-id':
				self.captcha_id = _attr(attrs, 'value')

	p = CaptchaParse()  # 实例化类
	p.feed(str(content))  # 把需要解析的数据放到feed方法里
	return p.captcha_id, p.captcha_url  # 把匹配到的数据返回
1

if __name__ == '__main__':
	uesrname = input('please input your username:')
	password = input('please input your password:')  # getpass.getpass('please input your password:')
	D = DoubanClient()
	D.login(uesrname, password)
	comment=input('please input comment:')
	D.get_content(comment) #调用函数发送信息
	print('end')
