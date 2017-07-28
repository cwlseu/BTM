#! bin/sh
K=100 # number of topics
input_dir=../sample-data
output_dir=../output
model_dir=$output_dir/model/ # set model path
W=272373 # Because our word have word -> id selfdefined, so, we set W
wordnum_per_topic=20
topicnum_per_doc=5
if [ ! -n $1 ]; then
   doc_pt=$1
else
   doc_pt=$input_dir/test_file
fi
echo "=============== Index Docs ============="
dwid_pt=$output_dir/doc_wids.txt
vocab_pt=$input_dir/vocab_map.txt
topic=$output_dir/topics.txt
result=$output_dir/predict
python predict_process_docs.py $doc_pt $vocab_pt $dwid_pt 

# inference p(z|d) for each doc
echo "================ Inferernce P(z|d)==============="
echo "../src/btm inf sum_b $K $dwid_pt $model_dir"
../src/btm inf sum_b $K $dwid_pt $model_dir $result

echo "================ Persistence Topic:Word ==============="
python topicDisplay.py $model_dir $K $vocab_pt $topic $wordnum_per_topic 
# output top words of each topic
echo "================ Topic Display ============="	
python getTopKTopicsforDoc.py $result $topic $topicnum_per_doc 

