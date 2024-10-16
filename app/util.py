import json
import joblib
import pandas as pd
import numpy as np

columns=[]
locations=[]
area_type=[]
pipe_model=None

def load_saved_artifacts():
    global columns,locations,area_type,pipe_model

    with open('model/columns.json') as file:
        data=json.load(file)
        columns=data['columns']

        locations=data['locations']
        locations.sort()
        locations.append('Other')

        area_type=data['area_type']
        area_type.sort()
   

    pipe_model=joblib.load('model/pipeline.pkl')



def get_location_names():
    return locations

def get_area_types():
    return area_type


def get_estimated_price(area_type:str,location:str,total_sqft:float,bhk:int,bath:int,balcony:int):
    '''
    Price return will be in Lakhs INR / 100k INR'''

    x=pd.DataFrame(columns=columns)
    x.loc[0]=np.zeros(len(columns))
    
    x['total_sqft'] = total_sqft
    x['bath'] = bath
    x['balcony'] = balcony
    x['bhk'] = bhk
    loc='location_'+location.lower()
    area='area_type_'+area_type.lower()

    if loc in x.columns:
        x[loc]=1
    if area in x.columns:
        x[area]=1

    return round(pipe_model.predict(x)[0],2) # NOte prices are in lakhs

if __name__=='__main__':
    load_saved_artifacts()
    print(locations)
    print(pipe_model['Linear_Regression'].coef_)
    print(get_estimated_price('built-up  area','Sarjapur',3854.5, 6,0, 4))
    print(get_estimated_price('Otherdcs','Sarjapur',3854.5, 6,0, 4))