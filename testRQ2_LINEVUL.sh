
for trainset in "bugtype_buffer_overflow" "bugtype_input_validation" "bugtype_mixed" "bugtype_privilege_escalation_authorization" "bugtype_resource_allocation_free" "bugtype_value_propagation_errors"
do
for testset in "bugtype_buffer_overflow" "bugtype_input_validation" "bugtype_mixed" "bugtype_privilege_escalation_authorization" "bugtype_resource_allocation_free" "bugtype_value_propagation_errors"
do
echo $trainset
echo $testset
CUDA_VISIBLE_DEVICES=1 python models/LineVul/code/linevul/linevul_main.py \
  --model_name=model.bin\
  --output_dir=./saved_models/LINEVUL_$trainset \
  --model_type=roberta \
  --tokenizer_name=/data2/chenlida/model/codebert-base \
  --model_name_or_path=/data2/chenlida/model/codebert-base \
  --do_test \
  --train_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${testset}/train.jsonl \
  --eval_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${testset}/valid.jsonl \
  --test_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${testset}/test.jsonl \
  --block_size 512 \
  --eval_batch_size 512 \
  --seed 1 2>&1 | tee "test_LINEVUL_$(echo $trainset | sed s@/@-@g)_$(echo $testset | sed s@/@-@g).log"
done
done