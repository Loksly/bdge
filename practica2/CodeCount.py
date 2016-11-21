from HTMLParser import HTMLParser

class CodeCount(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.nocode_length = 0
		self.code_length = 0
		self.inCode = 0

	def run(self, string):
		self.feed(string)

	def handle_starttag(self, tag, attrs):
		if tag == 'code':
			self.inCode = self.inCode + 1

	def handle_endtag(self, tag):
		if tag == 'code':
			self.inCode = self.inCode - 1

	def handle_data(self, data):
		if self.inCode > 0:
			self.code_length = self.code_length + len(data)
		else:
			self.nocode_length = self.nocode_length + len(data)
