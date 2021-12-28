# -*-coding:utf-8 -*-
'''
从用户输入的词中爬取代表性数据集下载链接
'''
import requests
import re
import urlencode as ude
from bs4 import BeautifulSoup
import dataclasses
from typing import Tuple
from tqdm import tqdm
import json
import os

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
        self.GEO_papers_json_path="GEO_papers.json"
        '''
        TCGA规则：A%22%2C%22B + %22%5D%7D%7D%5D%7D, '%2C'=',','%22B'='"'
        '''
        self.TCGA_link="https://portal.gdc.cancer.gov/repository?facetTab=cases&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.primary_site%22%2C%22value%22%3A%5B"
        self.OMIM_link="https://www.omim.org/search?index=entry&start=1&limit=10&sort=score+desc%2C+prefix_sort+desc&search="
        self.OMIM_json_path="OMIM_intro.json"
        
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
        这个函数预处理用户输入的搜索词，返回访问用的URL
        '''
        if (self.is_chinese(input_text)==False):
            raise ValueError("Chinese search is not supported, try English instead.")
        
        # GEO处理
        search_str=ude.urlencoder(text=input_text)
        search_str.replace(',', '%2C')#这里有个不兼容','的bug22
        self.GEO_search_str=self.GEO_link+search_str
        
        # TCGA处理
        # segmentation & cleaning based on sites
        punctuation=',./?;:"\'|`~，。？!！@#¥%'
        self.TCGA_search_tags=re.sub(r'[{}]+'.format(punctuation),' ',input_text).strip().split()
        self.TCGA_search_tags.remove("and")
        self.TCGA_search_tags.remove("of")
        # expample:['breast','cancer']
        with open('primary_sites.txt','r') as f:
            sites=set(f.readlines())
        tokens=[]
        # 搜索标准词表
        self.TCGA_search_str=self.TCGA_link
        for site in sites:
            for tag in self.TCGA_search_tags:
                if re.search(tag,site)!=None:
                    tokens.append(site)
        if tokens==list():
            raise ValueError("No primary site is searched!")
        else:
            # 构建URL
            for token in tokens:
                token_encode=ude.urlencoder(text=token)
                token_encode.replace(',', '%2C')
                self.TCGA_search_str=self.TCGA_search_str+"\""+token_encode+"\""+"%2C"
        self.TCGA_search_str=self.TCGA_search_str[0:len(self.TCGA_search_str)-3]+"%5D%7D%7D%5D%7D"
        
        #OMIM处理
        punctuation=',./?;:"\'|`~，。？!！@#¥%'
        self.OMIM_search_str=re.sub(r'[{}]+'.format(punctuation),' ',input_text).strip().replace(" ", "+")
        self.OMIM_search_str=self.OMIM_link+self.OMIM_search_str
        
                
    # --------------------------------这部分处理GEO Parser--------------------------------
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

    def geo2json(self,geo_papers:list):
        '''
        TODO: json必须是一个对象，要一次性写完
        '''
        with open(self.GEO_papers_json_path,"a+") as f:
            f.write(json.dumps(geo_papers,ensure_ascii=False, indent=4, separators=(',', ':')))
            f.write("\n")
            
    def GEO_search(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
        sess = requests.Session()
        GEO_req = sess.get(url = self.GEO_search_str, headers=headers, verify=False) 
        GEO_req.encoding = 'utf'
        GEO_bf = BeautifulSoup(GEO_req.content, 'lxml')
        geo_papers=[] #list有s,别漏了
        for item in tqdm(GEO_bf.find_all(class_='rslt')):
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
            geo_papers.append(geo_paper2dict(geo_paper))
        self.geo2json(geo_papers)
        
    #--------------------------------这部分处理TCGA Parser--------------------------------
    def TCGA_search(self):
        '''
        TODO:TCGA会加载出来对应的4个
        Scriptgdc-ng-plugins.js	
        Scriptgdc-templates.js	
        Scriptgdc-app-modified.js	
        Scriptmain.368d15b4.js	
        需要共同执行才能load出用来抓取的html内容，这部分长度太长，不方便用爬虫复现，暂时不做了
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
        sess = requests.Session()
        TCGA_req = sess.get(url = self.TCGA_search_str, headers=headers, verify=False) 
        TCGA_req.encoding = 'utf'
        TCGA_bf = BeautifulSoup(TCGA_req.content, 'lxml')
        pass
    
    #--------------------------------这部分处理OMIM Parser--------------------------------
    def OMIM_search(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
        sess = requests.Session()
        OMIM_req = sess.get(url = self.OMIM_search_str, headers=headers, verify=False) 
        OMIM_req.encoding = 'utf'
        OMIM_bf = BeautifulSoup(OMIM_req.content, 'lxml')
        # 默认第一个搜索结果
        OMIM_entry_url="https://www.omim.org/"+re.findall(r'(?<=<a href=").*?(?=">)',str(OMIM_bf.find(class_="mim-result-font").find(['a'])))[0]
        # 2度搜索
        OMIM_req2 = sess.get(url = OMIM_entry_url, headers=headers, verify=False) 
        OMIM_req2.encoding = 'utf'
        OMIM_bf2 = BeautifulSoup(OMIM_req2.content, 'lxml')
        OMIM_entry={}
        OMIM_entry["source"]=OMIM_entry_url
        OMIM_entry["title"]=OMIM_bf2.find_all(class_="mim-font")[1].text.strip()
        OMIM_entry["description"]=OMIM_bf2.find_all(id="descriptionFold")[0].text.strip('\n')
        link_names=[]
        link_urls=[]
        for item in OMIM_bf2.find_all(class_='panel-body small mim-panel-body'):
            link_names+=str(item.text.strip()).split('\n')
            link_urls+=re.findall(r'(?<=href=").*?(?=" )',str(item))
        external_links={}
        for i in range(0,len(link_names)):
            external_links[link_names[i]]=link_urls[i]
        OMIM_entry["external_links"]=external_links
        with open(self.OMIM_json_path,"a+") as f:
            f.write(json.dumps(OMIM_entry,ensure_ascii=False, indent=4, separators=(',', ':')))
            f.write("\n")
        
    
    def md_former(self):
        '''
        TODO: 日后做markdown用
        '''
        pass
    
    '''
    还有一个Oncomine数据不错，但不方便做，需要ID登录
    '''
    def main_flow(self):
        input_text=input("Young researcher, input field you wonna know: ")
        self.search_parser(input_text)
        self.GEO_search()
        self.OMIM_search()
        # self.TCGA_search()
        print(f"Search is finished in {self.GEO_papers_json_path} and {self.OMIM_search}.")

if __name__ == '__main__':
    ms=Multi_Spider()
    Multi_Spider().main_flow()

