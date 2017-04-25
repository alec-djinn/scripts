import sys  
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
from PyQt4.QtWebKit import *
from urllib import urlopen
from collections import OrderedDict
from pyensembl import EnsemblRelease
data = EnsemblRelease(75)

def get_first_transcript_by_gene_name(gene_name):
    gene = data.genes_by_name(gene_name)
    gene_id = str(gene[0]).split(',')[0].split('=')[-1]
    gene_location = str(gene[0]).split('=')[-1].strip(')')
    url = 'http://grch37.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g={};r={}'.format(gene_id,gene_location)
    for line in urlopen(url):
        if '<tbody><tr><td class="bold">' in line:
            return line.split('">')[2].split('</a>')[0]
        
class Render(QWebPage):  
    def __init__(self, url):  
        self.app = QApplication(sys.argv)  
        QWebPage.__init__(self)  
        self.loadFinished.connect(self._loadFinished)  
        self.mainFrame().load(QUrl(url))  
        self.app.exec_()  

    def _loadFinished(self, result):  
        self.frame = self.mainFrame()  
        self.app.quit()

def getHtml(str_url):
    r_html = Render(str_url)  
    html = r_html.frame.toHtml()

    return html

def get_exons_coord_by_gene_name(gene_name):
    gene = data.genes_by_name(gene_name)
    gene_id = str(gene[0]).split(',')[0].split('=')[-1]
    gene_location = str(gene[0]).split('=')[-1].strip(')')
    gene_transcript = get_first_transcript_by_gene_name(gene_name).split('.')[0]
    url = 'http://grch37.ensembl.org/Homo_sapiens/Transcript/Exons?db=core;g={};r={};t={}'.format(gene_id,gene_location,gene_transcript)
    str_html = getHtml(url)
    html = ''
    for line in str_html.split('\n'):
        try:
            #print line
            html += str(line)+'\n'
        except UnicodeEncodeError:
            pass
    blocks = html.split('\n')
    table = OrderedDict()
    for exon_id in data.exon_ids_of_gene_id(gene_id):
        for i,txt in enumerate(blocks):
            if exon_id in txt:
                if exon_id not in table:
                    table.update({exon_id:[]})
                for item in txt.split('<td style="width:10%;text-align:left">')[1:-1]:
                    table[exon_id].append(item.split('</td>')[0])
    return table

table = get_exons_coord_by_gene_name('TP53')
for k,v in table.iteritems():
    print k,v