#!/usr/bin/env python
#coding=utf-8
# translate word into id in documents
import sys

w2id = {}
 
def get_word2id(source):
    w2iid = dict()
    with open(source, 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            try:
                [word, iid] = line.split('\t', 2)
            except ValueError as e:
                pass
                #print line
                #w2iid['\t'] = int(line.strip())
            w2iid[word] = int(iid)
    return w2iid

def preprocess_corpus_w2iid(corpus_file, target_file, doc2iid="dociid.txt"):
    print('corpus file:' + corpus_file)
    doc_id = 0
    with open(target_file, 'w') as fw, open(corpus_file) as fr, open(doc2iid, 'w') as fwdoc:
        line = fr.readline()
        while line:
            [pacid, content] = line.split('\t', 2)
            wids = [str(w2id[w]) for w in content.strip().split()]
            fw.write("%s\n" % (' '.join(wids)))
            fwdoc.write("%s\t%d\n" % (pacid, doc_id))
            line = fr.readline()
            doc_id += 1

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python %s <doc_pt> <voca_pt> <dwid_pt> ' % sys.argv[0])
        print('\tdoc_pt    input docs to be indexed, each line is a doc with the format "word word ..."')
        print('\tvoca_pt   input vocabulary file, each line is a word with the format "word   wordId"')
        print('\tdwid_pt   output docs after indexing, each line is a doc with the format "wordId wordId..."')
        exit(1)
    
    doc_pt = sys.argv[1]
    voca_pt = sys.argv[2]
    dwid_pt = sys.argv[3]
    w2id = get_word2id(voca_pt)
    print('n(w)='+str(len(w2id)))
    preprocess_corpus_w2iid(doc_pt, dwid_pt)
