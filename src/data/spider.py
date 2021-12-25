# -*-coding:utf-8 -*-
'''
从用户输入的词中爬取代表性数据集下载链接
'''
import requests
import time,re,types
import urlencode as ude
from bs4 import BeautifulSoup




class GEO_Spider():
    def __init__(self) -> None:
        self.GEO_link="https://www.ncbi.nlm.nih.gov/gds/?term="
        
    def is_chinese(string)->bool:
        '''
        检查整个字符串是否包含中文，若有中文，返回True
        :param string: 需要检查的字符串
        :return: bool
        '''
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
    
    def search_parser(self,input_text:str):
        '''
        这个函数预处理用户输入的搜索词，返回访问GEO用的URL
        '''
        if (self.is_chinese(input_text)==False):
            raise ValueError("Chinese search is not supported, try English instead.")
        search_str=ude.urlencoder(text=input_text)
        self.search_str=self.GEO_link+search_str
        
    def search(self):
        sess = requests.Session()
        