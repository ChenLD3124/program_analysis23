#codeBERT
seed=1
subset="bugtype_mixed"
CUDA_VISIBLE_DEVICES=3 python ./utils/runlora.py \
--output_folder_name=CODEBERTRQl_$subset \
--output_dir=./saved_models \
--model_type=roberta \
--tokenizer_name=/data2/chenlida/model/codebert-base \
--model_name_or_path=/data2/chenlida/model/codebert-base \
--do_train \
--train_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/train.jsonl \
--eval_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/valid.jsonl \
--test_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/test.jsonl \
--epoch 10 \
--block_size 400 \
--train_batch_size 64 \
--eval_batch_size 64 \
--learning_rate 1e-4 \
--max_grad_norm 1.0 \
--evaluate_during_training \
--old_lora="moe" \
--seed $seed 2>&1 | tee "trainRQl_CODEBERT_$(echo $subset | sed s@/@-@g).log"
