"""Deterministic feature preparation shared by notebook and inference."""
import numpy as np
import pandas as pd

SCHEMAS = {
    'A': (['Distance_km', 'Courier_Experience_yrs'], ['Weather','Traffic_Level','Time_of_Day','Vehicle_Type']),
    'B': (['Straight_line_km','Delivery_person_Age'], ['Type_of_order','Type_of_vehicle']),
    'C': (['cost_of_the_order'], ['cuisine_type','day_of_the_week'])
}

def prepare_features(raw, dataset):
    d=raw.copy()
    for col in d.select_dtypes(include=['object','string']).columns:
        d[col]=d[col].str.strip().replace({'':np.nan,'NaN':np.nan,'nan':np.nan})
    if dataset=='B':
        cols=['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        coords=d[cols].apply(pd.to_numeric,errors='coerce')
        lat1,lon1,lat2,lon2=[np.radians(coords[c]) for c in cols]
        a=np.sin((lat2-lat1)/2)**2+np.cos(lat1)*np.cos(lat2)*np.sin((lon2-lon1)/2)**2
        distance=6371*2*np.arcsin(np.sqrt(np.clip(a,0,1)))
        valid=(coords.notna().all(axis=1)&coords.ne(0).all(axis=1)&
               coords.iloc[:,[0,2]].abs().le(90).all(axis=1)&
               coords.iloc[:,[1,3]].abs().le(180).all(axis=1)&distance.between(0,100))
        # Fixed food-delivery plausibility rule, not learned from targets.
        # Never flip coordinate signs to guess a corrected location.
        d['Straight_line_km']=distance.where(valid)
        age=pd.to_numeric(d['Delivery_person_Age'],errors='coerce')
        d['Delivery_person_Age']=age.where(age.between(18,80))
    nums,cats=SCHEMAS[dataset]
    for col in nums:d[col]=pd.to_numeric(d[col],errors='coerce')
    for col in cats:d[col]=d[col].astype(object).where(d[col].notna(),np.nan)
    return d[nums+cats]
