#codeBERT
subset="bugtype_mixed"
for seed in 1 2 3
do
echo $seed
CUDA_VISIBLE_DEVICES=1 python models/CodeBERT/code/run2.py \
--output_folder_name=CODEBERT_$subset_$seed \
--output_dir=./saved_models_RQ1 \
--model_type=roberta \
--tokenizer_name=/data2/chenlida/model/codebert-base \
--model_name_or_path=/data2/chenlida/model/codebert-base \
--do_train \
--train_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/train.jsonl \
--eval_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/valid.jsonl \
--test_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/test.jsonl \
--epoch 5 \
--block_size 400 \
--train_batch_size 32 \
--eval_batch_size 64 \
--learning_rate 2e-5 \
--max_grad_norm 1.0 \
--evaluate_during_training \
--seed $seed 2>&1 | tee "train_CODEBERT_$(echo $subset | sed s@/@-@g)_$(echo $seed | sed s@/@-@g).log"
done
