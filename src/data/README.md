# data
这里面主要是爬虫程序，由于甲方要求数据库，但未提供数据，故使用交互式爬虫进行爬取。由于甲方不提供后台，故爬虫皆非后台常驻。

## json格式
从用户输入的search string爬取的GEO papers，格式见根目录  
`GEO_papers.json`文件相关说明  
```js
{
        "title":"['string, 文章标题']",
        "gseid":"string, GSE号码，GEO+六位数字",
        "organism":"string, 物种名，可能有多个",
        "exp_type":"string, 实验类型",
        "platform":"string, 实验品台，GPL+5位数字",
        "n_sample":"int, 样本数"
}  
注：文章URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=+【GSE号】  
```
`OMIM_intro.json`文件相关说明  
```js
{
    "source": "string, OMIM源的链接，可以放在超链接里",
    "title":"string, 规范化的标题",
    "description":"string, 简介",
    "external_links":{
        "外链名":"外链URL",
        ...
    }
}
```

## primary_sites.txt
TCGA规范词表，由于TCGA的js过于复杂难以复现其中加载的部分，实际上未使用

## search_spider.py
这是整合爬虫，爬omim，GEO，TCGA(失败)，返回json

## [tcga_downloader]https://shiny.zd200572.com/tcga_downloader/
用户从这个web下载TCGA数据的manifest  

## tcga_downloader.py
这个从TCGA的manifest中下载数据，绝大部分code来自[chenwi](https://github.com/murphy-mtt/bio/blob/543c1d69dbec5a263e199c0d5c02baf8d5ec9a15/download_tcga.py)