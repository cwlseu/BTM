#!/bin/sh

K=100   # number of topics

alpha=`echo "scale=3;50/$K"|bc`
beta=0.005
niter=60
save_step=50
echo $alpha
input_dir=../sample-data
output_dir=../output
model_dir=$output_dir/model/
mkdir -p $output_dir/model 

# the input docs for training
doc_pt=$input_dir/segment_video_all

echo "=============== Index Docs ============="
# docs after indexing
dwid_pt=$output_dir/doc_wids.txt
# vocabulary file
voca_pt=$input_dir/vocab_map.txt
python preprocess_docs.py $doc_pt $voca_pt $dwid_pt

## learning parameters p(z) and p(w|z)
echo "=============== Topic Learning ============="
#W=`wc -l < $voca_pt` # vocabulary size
W=272373
make -C ../src
echo "../src/btm est $K $W $alpha $beta $niter $save_step $dwid_pt $model_dir"
../src/btm est $K $W $alpha $beta $niter $save_step $dwid_pt $model_dir

## infer p(z|d) for each doc
#echo "================ Infer P(z|d)==============="
#echo "../src/btm inf sum_b $K $dwid_pt $model_dir"
#../src/btm inf sum_b $K $dwid_pt $model_dir

## output top words of each topic
#echo "================ Topic Display ============="
#python topicDisplay.py $model_dir $K $voca_pt
