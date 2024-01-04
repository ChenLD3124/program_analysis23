seed=1

for subset in "bugtype_buffer_overflow" "bugtype_input_validation" "bugtype_mixed" "bugtype_privilege_escalation_authorization" "bugtype_resource_allocation_free" "bugtype_value_propagation_errors"
do
echo $subset
CUDA_VISIBLE_DEVICES=4 python models/LineVul/code/linevul/linevul_main.py \
  --output_dir=./saved_models/LINEVUL_$subset \
  --model_type=roberta \
  --tokenizer_name=/data2/chenlida/model/codebert-base \
  --model_name_or_path=/data2/chenlida/model/codebert-base \
  --do_train \
  --do_test \
  --train_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/train.jsonl \
  --eval_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/valid.jsonl \
  --test_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/test.jsonl \
  --epochs 10 \
  --block_size 512 \
  --train_batch_size 16 \
  --eval_batch_size 16 \
  --learning_rate 2e-5 \
  --max_grad_norm 1.0 \
  --evaluate_during_training \
  --seed $seed 2>&1 | tee "train_LINEVUL_$(echo $subset | sed s@/@-@g).log"
done