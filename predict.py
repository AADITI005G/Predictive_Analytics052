"""Predict with either dataset's saved pipeline. Run from any directory."""
from pathlib import Path
import argparse
import joblib
import numpy as np
import pandas as pd
from features import prepare_features
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--dataset',required=True,choices=['A','B','C'])
    parser.add_argument('--input',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    data=pd.read_csv(args.input)
    try:X=prepare_features(data,args.dataset)
    except KeyError as err:parser.error(f'Missing required input column: {err}')
    model=joblib.load(root/f'models/model_{args.dataset}.joblib')
    result=pd.DataFrame({'predicted_delivery_minutes':np.maximum(0,model.predict(X))})
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);result.to_csv(out,index=False)
    print(result.to_string(index=False))
if __name__=='__main__':main()
