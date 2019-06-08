#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/env python
# [START vision_quickstart]
import io
import os
import pandas as pd
import numpy as np
# Imports the Google Cloud client library
# [START vision_python_migration_import]
from google.cloud import vision
from google.cloud.vision import types
# [END vision_python_migration_import]



def run_quickstart(uri):

    #Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    #print('Labels:')
    name_list=list()
    percentage_list=list()
    for label in labels:
        name_list.append(label.description)
        percentage_list.append(label.score)
    return name_list, percentage_list

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    text_list=list()
    mark_list=list()   
    sentence=""
    count=0
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        text2='\n"{}"'.format(text.description)
        print('bounds: {}'.format(','.join(vertices)))
        print(text2)
        text_list.append(text2)
        if count==0:
            mark_list.append(1)
        else:
            mark_list.append(0)
        count+=1
        #sentence+=text2
    #text_list.append(sentence)
    #mark_list.append(1)
    return text_list, mark_list

sample1=pd.read_excel("VISION_API_G1.xlsx")
sample2=pd.read_excel("VISION_API_G2.xlsx")
sample3=pd.read_excel("VISION_API_G3.xlsx")
sample4=pd.read_excel("VISION_API_G4.xlsx")
sample5=pd.read_excel("VISION_API_G5.xlsx")

acc=pd.DataFrame()

def checking_sample(sample,file_id,start,end): 
    sample=sample.loc[start:end]
    acc = pd.DataFrame()
    acc_text=pd.DataFrame()
    error = pd.DataFrame()
    for i in range(start,end):
        print(i)
        name_list,percentage_list=run_quickstart(sample.loc[i,'URL'])
        df_name=pd.DataFrame(name_list)
        df_percentage=pd.DataFrame(percentage_list)
        df=pd.concat([df_name,df_percentage],axis=1)
        df['URL']=sample.loc[i,'URL']
        
        text_list,mark_list= detect_text_uri(sample.loc[i,'URL'])
        df_text=pd.DataFrame(text_list)
        df_mark=pd.DataFrame(mark_list)
        df2=pd.concat([df_text,df_mark],axis=1)
        df2['URL']=sample.loc[i,'URL']

        if len(df)>0:            
            acc=pd.concat([acc,df], axis= 0, sort=False)
        else:
            print("error!!!")
            df2=sample1.loc[i]
            error=pd.concat([error,df2], axis= 0, sort=False)
        
        if len(df2)>0:            
            acc_text=pd.concat([acc_text,df2], axis= 0, sort=False)
        else:
            print("error!!!")
    print(acc)
    print(error)
    total=pd.merge(left=sample,right=acc,on="URL", how='outer')
    total.to_csv("sample"+file_id+".csv")
    total_text=pd.merge(left=sample,right=acc_text,on="URL", how='outer')
    total_text["mark"]=0 
    total_text.to_csv("sample"+file_id+"_text.csv")
    error.to_csv("error.csv")
    #acc_text.to_csv("text.csv")
    print(text_list)
    print(acc_text)    

checking_sample(sample1,"1_2000",10,20)
#checking_sample(sample2,"2_2000",1000,2000)
#checking_sample(sample3,"3_2000",1000,2000)
#checking_sample(sample4,"4_2000",1000,2000)
#checking_sample(sample5,"5_2000",1000,2000)

