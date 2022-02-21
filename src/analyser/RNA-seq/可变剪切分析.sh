# 可变剪切分析

# 可变剪切分析，这里使用SUPPA2 来进行。据作者说，这是一个又快，准确度又高，对样本测序深度要求还低的软件。  
# PSI（proportion spliced-in）作为可变剪切中常见的评估指标，用于衡量可变剪切发生率。在不同软件中，计算可能有所不同。举一个skipping exon的例子，若F1 表示那些包含某个exon (这里研究local AS events, 指特定的一个exon)的转录本，F2 表示那些不包含那个exon 的转录本。则PSI。  
# 箱型图绘制，查看某个AS event的psi value.（Python  


wget https://raw.githubusercontent.com/comprna/SUPPA/master/scripts/generate_boxplot_event.py
python generate_boxplot_event.py -i HMDM_as_event.psi -e "ENSG00000004866.22;AF:chr7:116953327:116953691-117099762:117014888:117015014-117099762:+" -g 1-3,4-6 -c M0,M1 -o .

