# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import torch
import torch.nn as nn
import torch
from peft import PeftModel,get_peft_model,LoraConfig,TaskType
peft_config = LoraConfig(
    r=8, lora_alpha=16, lora_dropout=0.05, task_type=TaskType.SEQ_CLS
)

    
    
class Model(nn.Module):   
    def __init__(self, encoder,config,tokenizer,args):
        super(Model, self).__init__()
        self.old_lora=args.old_lora
        model = get_peft_model(encoder,peft_config)
        if args.old_lora!="":
            model.load_adapter(args.old_lora,'prelora',is_trainable=True)
            model.set_adapter('prelora')
            
        self.encoder=model
        self.config=config
        self.tokenizer=tokenizer
        self.args=args
    
        
    def forward(self, input_ids=None,labels=None): 
        outputs=self.encoder(input_ids,attention_mask=input_ids.ne(1))[0]
        logits=outputs
        prob=torch.sigmoid(logits)
        if labels is not None:
            labels=labels.float()
            loss=torch.log(prob[:,0]+1e-10)*labels+torch.log((1-prob)[:,0]+1e-10)*(1-labels)
            loss=-loss.mean()
            
            if self.old_lora!="":
                orthogonal_loss = 0.
                for name, param in self.encoder.named_parameters():
                    if "lora_A" in name:
                        for name_, param_ in self.encoder.named_parameters():
                            if "lora_A.default" in name_ and name.split("lora_A")[0] == name_.split("lora_A")[0]:
                                orthogonal_loss += torch.abs(torch.mm(param, param_.T)).sum() # [r * dim] * [dim * r]
                                break # target modules have been matched
                print(orthogonal_loss)
                lamda_1 = self.args.lamda_1
                loss = loss + orthogonal_loss * lamda_1
            
            return loss,prob
        else:
            return prob
    
    def load_adapter(self,path):
        self.encoder.load_adapter(path,'infer')
        self.encoder.set_adapter('infer')
        
      
        
 
