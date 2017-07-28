#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
TOPIC_NUM = 100

def get_topics(topics_file):
    topic = list()
    with open(topics_file, 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            topic.append(tuple(line.strip().split('\t', 3)))
    return topic
def show_topK_topics(predict_result, topics_file, K = 5, threshold=0.2):
    topic = get_topics(topics_file)
    with open(predict_result, 'r') as fd, open("result_", 'w') as fw:
        lines = fd.readlines()
        docid = 0
        print("----TopicID(p(z))\t\tp(z|d)\t\tKeywords-----")
        #fw.write("TopicID(p(z))\tp(z|d)\tKeywords\n")
        for doc in lines:
            doc_topics = [float(a) for a in doc.strip().split()]
            assert len(doc_topics) == TOPIC_NUM
            doc_topics_map = zip(xrange(TOPIC_NUM), doc_topics)
            top_K = sorted(doc_topics_map, key=lambda x: x[1], reverse=True)[:K]
            print "DOCID:%d" % docid
            #fw.write("DOCID:%d\n" % docid)
            print "\tTopicID:%d(%s)\t%.6f\t%s" % (top_K[0][0], topic[top_K[0][0]][1],\
                                                 top_K[0][1], topic[top_K[0][0]][2])
            #fw.write("TopicID:%d(%s)\t%.6f\t%s\n" % (top_K[0][0], topic[top_K[0][0]][1],\
            #                                     top_K[0][1], topic[top_K[0][0]][2]))
            for (k, v) in top_K[1:]:
                if v < threshold: break
                print "\tTopicID:%d(%s)\t%.6f\t%s" % (k, topic[k][1], v, topic[k][2].encode('utf-8'))
                #fw.write("TopicID:%d(%s)\t%.6f\t%s" % (k, topic[k][1], v, topic[k][2]))
            docid += 1

if __name__ == '__main__':
    if len(sys.argv) < 4: 
        print('Usage: python %s <predict_result> <topic_file> <TopicNumPerDoc>' % sys.argv[0])
        print('\predict_result    input:inference result')
        print('\ttopic_file    input:the topic list file')
        print('\tTopicNum   input:Topic num per document')
        exit(1)
    predict_file = sys.argv[1]
    topic_file = sys.argv[2]
    topicNum = int(sys.argv[3])
    show_topK_topics(predict_file, topic_file, topicNum)
