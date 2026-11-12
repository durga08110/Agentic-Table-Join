from langchain.tools import tool
from sentence_transformers import SentenceTransform
from pyspark.sql.functions import pandas_udf
from src.sparkSession import getSparkSession

import pandas as pd
import numpy as np


@tool
@pandas_udf(ArrayType(FloatType()))
#use pandas udf for bulk processing, output is array - each element is array of floats
def computeEmbeddings(textInput:pd.series)->pd.series:
    '''Computes embeddings for text containing column name,data type,sample values'''
    model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings=model.encode(textInput.tolist(),batch_size=32,show_progress_bar=False)
    return pd.Series(embeddings.tolist())
    #returns [
    #           [for col 1: 0.1,0.2,0.4],  [for col 2: 0.1,0.2,0.4]
    #       ]


def generateEmbeddings(listOfString):
	spark=getSparkSession()
	df=spark.createDataFrame(listOfString,StringType()).toDF("profile")
	df_embeddings=df.withColumn("embedding",computeEmbeddings(col("profile")))
	return [row["embedding"] for row in df_embeddings.collect()]