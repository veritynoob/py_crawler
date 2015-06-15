#coding=utf8

import logging
import requests
import pdb
import lxml.html
import re
import time

class base_crawler:
    def __init__(self, log_name, out_path):
        self._count = 0
        self._rep_queue = set()
        self._wait_urls = []
        self._out_path = out_path
        self._out_file = None
        logging.basicConfig(filename=log_name, level=logging.ERROR, filemode='w', format='%(asctime)s:%(lineno)d:%(funcName)s:%(message)s')

    #not really crawl,but push to queue or stack
    def crawl(self, url, callback=None):
        if url not in self._rep_queue:
            self._rep_queue.add(url)
            self._wait_urls.append((url, callback))

    def on_start(self):
        pass

    def run(self):
        #pdb.set_trace()
        self._out_file = open(self._out_path, mode='w')
        self.on_start()
        while self._wait_urls:
            if self._count > 60:
                time.sleep(10)
                self._count = 0

            self._count += 1
            url, callback = self._wait_urls.pop()
            response =  None
            
            try:
                response = requests.get(url, timeout=5)
            except:
                if response:
                    logging.error('base\t%s\t%s\t%s'%(reponse.status_code, url, callback))
                else:
                    logging.error('base\t%s\t%s\t%s'%('none', url, callback))

            if response and response.status_code==200:
                result = callback(response)
                if result:
                    self._out_file.write('!@#$'.join(result).replace('\n','')+'\n')
            elif response:
                logging.error('base\t%s\t%s\t%s'%(reponse.status_code, url, callback))
        self._out_file.close()


class spider(base_crawler):

    def __init__(self, log_name, out_path):
        base_crawler.__init__(self, log_name, out_path)

    def on_start(self):
        self.crawl('http://www.baidu.com', callback=self.index_page)
    def index_page(self, response):
        #self.crawl('http://www.baidu.com', callback=self.index_page)
        return (response.url,)


if __name__ == '__main__':
    sp = spider('log_name', 'result')
    sp.run()
