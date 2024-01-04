import os
import pandas as pd

def get_result(log_path):
    filenames = os.listdir(log_path)
    results = []
    for filename in filenames:
        filepath = os.path.join(log_path, filename)
        with open(filepath, 'r') as file:
            content = file.readlines()
            result = {}
            parts = filename.split('bugtype')
            result['training'] = parts[1].lstrip('_').rstrip('_')
            result['evaluation'] = parts[2].lstrip('_').rstrip('_').replace('.log','')
            if 'LINEVUL' in filename:
                result['Model']='LineVul'
                for line in content[-5:]:
                    if 'test_f1' in line:
                        result['f1'] = float(line.split('=')[-1])*100
            elif 'CODEBERT' in filename:
                result['Model']='CodeBert'
                for line in content[-5:]:
                    if 'F-measure' in line:
                        result['f1'] = float(line.split(':')[-1])*100
            results.append(result)
    return pd.DataFrame(results)

if __name__=="__main__":
    a=get_result('./log/')
    print(a)