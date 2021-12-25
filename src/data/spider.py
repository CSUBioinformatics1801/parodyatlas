# -*-coding:utf-8 -*-
'''
从用户输入的词中爬取代表性数据集下载链接
'''
import requests
import re
import urlencode as ude
from bs4 import BeautifulSoup
import dataclasses
from typing import Any, Mapping, Optional, Sequence, Tuple
from tqdm import tqdm
import json

#TODO: import markdown
'''
日后再说，有机会直接转化成markdown，链上wiki
'''
@dataclasses.dataclass(frozen=True)
class GEO_paper:
    title: str
    gseid: str
    organism: str
    exp_type:str
    platform:str
    n_sample: int

def geo_paper2dict(geo_paper:GEO_paper)->dict:
    return {"title":geo_paper.title,
            "gseid":geo_paper.gseid,
            "organism": geo_paper.organism,
            "exp_type":geo_paper.exp_type,
            "platform":geo_paper.platform,
            "n_sample":geo_paper.n_sample       
            }
class Multi_Spider():
    def __init__(self) -> None:
        self.GEO_link="https://www.ncbi.nlm.nih.gov/gds/?term="
        self.json_path="test.json"
        
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
        self.GEO_search_str=self.GEO_link+search_str
        
    def get_title(self,paper_item)->str:
        title=str(re.findall(r'(?<=<a href="/geo/query/acc.cgi\?acc=GSE\d{6}" ref="ordinalpos=\d{1}&amp;ncbi_uid=\d{9}&amp;link_uid=\d{9}">).*?(?=</a></p>)',str(paper_item.find_all('p',class_='title')))).replace('</b>','').replace('<b>','')
        if len(title)==2:
            '''
            paper_item:bs4.element.Tag，为了少import一次，不加上了
            正则里的‘ordinalpos=’存在一个待解决的漏洞，匹配正则中出现的字符，无法用非转译的"?",","，len(title)==2即为空，改进可以简洁代码
            '''
            title=str(re.findall(r'(?<=<a href="/geo/query/acc.cgi\?acc=GSE\d{6}" ref="ordinalpos=\d{2}&amp;ncbi_uid=\d{9}&amp;link_uid=\d{9}">).*?(?=</a></p>)',str(paper_item.find_all('p',class_='title')))).replace('</b>','').replace('<b>','')
        return title
    
    def get_gseid(self,paper_item)->str:
        return(re.findall(r'GSE\d{6}',str(paper_item))[0])
    
    def get_organism_and_exp_type(self,paper_item)->Tuple[str,str]:
        '''
        发现这两个在一起，放在一个方法里
        '''
        organism,exp_type,_=re.findall(r'(?<=<dd class="lng_ln">).*?(?=</dd>)',str(paper_item))
        
        return(organism,exp_type)
    
    def get_platform(self,paper_item)->str:
        return(re.findall(r'GPL\d{5}',str(paper_item))[0])
    
    def get_n_sample(self,paper_item)->int:
        return(re.findall(r'(?<=[ETYP]]">).*?(?= Sample)',str(paper_item))[0])

    def geo2json(self,geo_paper:GEO_paper):
        '''
        这里把geo的paper逐一写到json里
        '''
        with open(self.json_path,"a+") as f:
            f.write(json.json.dumps(geo_paper2dict(geo_paper),ensure_ascii=False, indent=4, separators=(',', ':')))
            f.write("\n")
            
    def GEO_search(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
        sess = requests.Session()
        req = sess.get(url = self.GEO_search_str, headers=headers, verify=False) 
        req.encoding = 'utf'
        bf = BeautifulSoup(req.content, 'lxml')
        for item in tqdm(bf.find_all(class_='rslt')):
            organism,exp_type=self.get_organism_and_exp_type(item)
            geo_paper=GEO_paper(
                title=self.get_title(item),
                gseid=self.get_gseid(item),
                organism=organism,
                exp_type=exp_type,
                platform=self.get_platform(item),
                n_sample=self.get_n_sample(item)
            )
            del organism,exp_type
            self.geo2json(geo_paper)

    
    def md_former(self):
        '''
        TODO: 日后做markdown用
        '''
        pass
        
    def main_flow(self):
        input_text=input("Young researcher, input field you wonna know: ")
        self.search_parser(input_text)
        self.GEO_search()
        print(f"Search is finished in {self.json_path}.")

if __name__ == '__main__':
    ms=Multi_Spider()
    Multi_Spider().main_flow()

