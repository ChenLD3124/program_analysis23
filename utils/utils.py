from peft import PeftModel,get_peft_model,LoraConfig,TaskType
peft_config = LoraConfig(
        r=8, lora_alpha=16, lora_dropout=0.05, task_type=TaskType.SEQ_CLS
    )

def merge_adapter(model,*paths):
    model=get_peft_model(model,peft_config)
    for path in paths:
        model.load_adapter(path,adapter_name=path)
    model.add_weighted_adapter(paths,[1/len(paths)]*len(paths),'moe')
    model.set_adapter('moe')
    model.save_pretrained('moe')
    
def merge_adapter_with_weight(model,paths,weights,name):
    model=get_peft_model(model,peft_config)
    for path in paths:
        model.load_adapter(path,adapter_name=path)
    model.add_weighted_adapter(paths,weights,name)
    model.set_adapter(name)
    model.save_pretrained(name)