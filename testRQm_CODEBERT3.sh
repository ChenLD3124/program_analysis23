#!/bin/bash

for trainset in "bugtype_buffer_overflow" "bugtype_input_validation" "bugtype_mixed" "bugtype_privilege_escalation_authorization" "bugtype_resource_allocation_free" "bugtype_value_propagation_errors"
do
echo $trainset
CUDA_VISIBLE_DEVICES=1 python ./utils/runlora.py \
--output_folder_name=$trainset \
--output_dir=. \
--model_type=roberta \
--tokenizer_name=/data2/chenlida/model/codebert-base \
--model_name_or_path=/data2/chenlida/model/codebert-base \
--do_test \
--test_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${trainset}/test.jsonl \
--epoch 5 \
--block_size 400 \
--train_batch_size 32 \
--eval_batch_size 64 \
--learning_rate 2e-5 \
--max_grad_norm 1.0 \
--evaluate_during_training \
--seed 1 2>&1 | tee "testRQl_CODEBERT_$(echo $trainset | sed s@/@-@g)_$(echo $trainset | sed s@/@-@g).log"
done