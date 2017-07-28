#!/usr/bin/env python
# -*-encoding=utf-8-*-
import sys

# return:    {wid:w, ...}
def read_vocab(pt):
    vocab = {}
    for l in open(pt):
        try:
            [w, wid]  = l.split('\t', 2)
            vocab[int(wid)] = w
        except ValueError as e:
            pass
            #vocab[int(l.strip())] = '\t'
    return vocab

def read_pz(pt):
    return [float(p) for p in open(pt).readline().split()]
    
# voca = {wid:w,...}
def dispTopics(pt, voca, pz):
    """按照topic的概率从大到小排序进行显示
    """
    k = 0
    topics = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs)
        wvs = sorted(wvs, key=lambda d:d[1], reverse=True)
        #tmps = ' '.join(['%s' % voca[w] for w,v in wvs[:10]])
        tmps = ' '.join(['%s:%f' % (voca[w],v) for w,v in wvs[:10]])
        topics.append((pz[k], tmps))
        k += 1
        
    print('p(z)\t\tTop words')
    for pz, s in sorted(topics, reverse=True):
        print('%f\t%s' % (pz, s))

def persist_topics(pt, vocab, pz, target_file, TopK = 10):
    k = 0
    topics = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs)
        wvs = sorted(wvs, key=lambda d:d[1], reverse=True)
        tmps = ' '.join(['%s:%f' % (vocab[w],v) for w,v in wvs[:TopK]])
        topics.append((pz[k], tmps))
        k += 1
        
    print('p(z)\t\tTop words')
    k = 0
    with open(target_file, 'w') as fd:
        for pz, s in topics:
            fd.write('%d\t%f\t%s\n' % (k, pz, s))
            k += 1

            
if __name__ == '__main__':
    if len(sys.argv) < 6: 
        print('Usage: python %s <model_dir> <K> <vocab_pt> <topic_file> <word_per_topics>' % sys.argv[0])
        print('\tmodel_dir    input:the output dir of BTM')
        print('\tK    input:the number of topics')
        print('\tvocab_pt    input:the vocabulary file')
        print('\ttopic_file	input:the topics file')
        print('\tword_per_topic	input:the word number of each topic')
        exit(1)
        
    model_dir = sys.argv[1]
    K = int(sys.argv[2])
    vocab_pt = sys.argv[3]
    vocab = read_vocab(vocab_pt)    

    pz_pt = model_dir + 'k%d.pz' % K
    pz = read_pz(pz_pt)
    
    zw_pt = model_dir + 'k%d.pw_z' %  K
    # dispTopics(zw_pt, vocab, pz)
    target_file = sys.argv[4]#"topics.txt"
    K = int(sys.argv[5])
    persist_topics(zw_pt, vocab, pz, target_file, K)
