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



def async_detect_document(gcs_source_uri, gcs_destination_uri):
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    # With a file of 5 pages
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=90)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name=bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())

    # The actual response for the first page of the input file.
    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print(u'Full text:\n{}'.format(annotation.text))

sample1=pd.read_excel("VISION_API_G1.xlsx")
sample2=pd.read_excel("VISION_API_G2.xlsx")
sample3=pd.read_excel("VISION_API_G3.xlsx")
sample4=pd.read_excel("VISION_API_G4.xlsx")
sample5=pd.read_excel("VISION_API_G5.xlsx")

acc=pd.DataFrame()

def checking_sample(sample,file_id,start,end): 
    sample=sample.loc[start:end]
    acc = pd.DataFrame()
    error = pd.DataFrame()
    for i in range(start,end):
        print(i)
        name_list,percentage_list=run_quickstart(sample.loc[i,'URL'])
        df_name=pd.DataFrame(name_list)
        df_percentage=pd.DataFrame(percentage_list)
        df=pd.concat([df_name,df_percentage],axis=1)
        df['URL']=sample.loc[i,'URL']
        if len(df)>0:            
            acc=pd.concat([acc,df], axis= 0, sort=False)
        else:
            print("error!!!")
            df2=sample3.loc[i]
            error=pd.concat([error,df2], axis= 0, sort=False)
    print(acc)
    print(error)
    total=pd.merge(left=sample,right=acc,on="URL", how='outer')
    total.to_csv("sample"+file_id+".csv")
    error.to_csv("error.csv")
    
#checking_sample(sample1,"1_2000",1000,2000)
#checking_sample(sample2,"2_24500_25000",24500,25000)
#checking_sample(sample2,"2_25000_25330",25000,25330)
#checking_sample(sample3,"3_26000_26500",26000,26500)
#checking_sample(sample3,"3_26500_27069",26500,27069)
#checking_sample(sample4,"4_2000",1000,2000)
#checking_sample(sample5,"5_2000",1000,2000)
    

