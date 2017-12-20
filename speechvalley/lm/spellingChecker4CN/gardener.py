# encoding: utf-8
# ******************************************************
# Author       : zzw922cn
# Last modified: 2017-12-20 11:00
# Email        : zzw922cn@gmail.com
# Filename     : gardener.py
# Description  : Spelling Corrector for Chinese
# ******************************************************

import os
import json
import numpy as np
from hanziconv import HanziConv
from pypinyin import pinyin
from speechvalley.lm.spellingChecker4CN.utils import filter_punctuation
from speechvalley.utils.taskUtils import check_path_exists

class CorpusGardener(object):
    """
    Preprocessing multiple language corpuses, and gathering
    them into batches
    """
  
    def __init__(self, remove_duplicate_space=True):
        self.remove_dubplicate_space = remove_duplicate_space
        self.save_dir = '/home/pony/github/data/spellingChecker/raw'

    def process_poetry(self, data_dir='/media/pony/DLdigest/data/languageModel/chinese-poetry/json'):
        save_dir = os.path.join(self.save_dir, 'poem')
        check_path_exists(save_dir)
        count = 0
        for entry in os.scandir(data_dir):
            if entry.name.startswith('poet'):
                with open(entry.path, 'r') as json_file:
                    poems = json.load(json_file)
                    for p in poems: 
                        paras = HanziConv.toSimplified(''.join(p['paragraphs']).replace('\n', ''))
                        paras = filter_punctuation(paras)
                        for para in paras.split(' '):
                            if len(para.strip())!=0:
                                pys = ' '.join(np.array(pinyin(para)).flatten())
                                with open(os.path.join(save_dir, str(count//400000+1)+'.txt'), 'a') as f:
                                    f.write(para+','+pys+'\n')
                                count += 1
        
    def process_dureader(self, data_dir='/media/pony/DLdigest/data/languageModel/dureader-raw/'): 
        save_dir = os.path.join(self.save_dir, 'poem')
        check_path_exists(save_dir)
        count = 0
        for entry in os.scandir(data_dir):
            if entry.name.endswith('json'):
                print(entry.path)
                with open(entry.path, 'r') as f:
                    for line in f:
                        contents = json.loads(line)
                        for doc in contents['documents']:
                            paragraphs = filter_punctuation(''.join(doc['paragraphs']))
                            title = doc['title']
                            print(paragraphs)
            
    def process_sogou(self, data_dir): 
        pass

if __name__ == '__main__':
    cg = CorpusGardener()
    cg.process_dureader()
