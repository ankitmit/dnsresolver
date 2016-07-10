import sys
import re

class UtilFunctions:
	def __init__(self):
		pass
	def log2Screen(self, msg):
		print msg

	#This function removes unwanted spaces and tabs from a line
	def remove_unwanted_white(self, str):
		str = re.sub("\s\s+" , " ", str)
		str = str.rstrip()
		str = str.lstrip()
		return str