
subset="bugtype_mixed"
for seed in 1 2 3
do
echo $seed
CUDA_VISIBLE_DEVICES=0 python models/LineVul/code/linevul/linevul_main.py \
  --model_name=model.bin\
  --output_dir=./saved_models_RQ1/LINEVUL_$subset \
  --model_type=roberta \
  --tokenizer_name=/data2/chenlida/model/codebert-base \
  --model_name_or_path=/data2/chenlida/model/codebert-base \
  --do_test \
  --train_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/train.jsonl \
  --eval_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/valid.jsonl \
  --test_data_file=/data2/chenlida/work/fx/data-package/cross_sections/bug_type/${subset}/test.jsonl \
  --block_size 512 \
  --eval_batch_size 512 \
  --seed $seed 2>&1 | tee "test_LINEVUL_$(echo $subset | sed s@/@-@g)_$(echo $seed | sed s@/@-@g).log"
done