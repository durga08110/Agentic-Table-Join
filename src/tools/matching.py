from src.sparkSession import getSparkSession
from langchain.tools import tool
import re
import numpy as np

@tool
def cosineSimilarity(listA,listB)-> float:
    """Schema Matching 1: Computes cosine similarity between two column embeddings"""
    a,b=np.array(listA),np.array(listB)
    norm=np.linalg.norm(a)*np.linalg.norm(b)
    return float(np.dot(a,b)/norm) if norm!=0 else 0.0


@tool
def stringMatch(source,target)->float:
    """Schema Matching 2: Computes column name similarity using Jaccard similarty and character trigrams"""
    sourceCleanVersion=re.sub(r'[^a-zA-Z0-9]',' ',source.lower()).strip()
    targetCleanVersion=re.sub(r'[^a-zA-Z0-9]',' ',target.lower()).strip()
    if sourceCleanVersion==targetCleanVersion:
        return 1.0
    
    # jacquard similarity
    sourceTokens=set(sourceCleanVersion.split())
    targetTokens=set(targetCleanVersion.split())
    jacSimilarity=len(sourceTokens & targetTokens)/max(len(sourceTokens|targetTokens),1)

    #trigram similarity
    def getTrigrams(text)->str:
        return ({text[i:i+3] for i in range(len(text)-2)} 
		if len(text)>=3
		else set())
    
    sourceTrigrams=getTrigrams(sourceCleanVersion)
    targetTrigrams=getTrigrams(targetCleanVersion)
    trigSimilarity=len(sourceTrigrams & targetTrigrams)/max(len(sourceTrigrams|targetTrigrams),1)

    return round(float(max(jacSimilarity,trigSimilarity)),4)



@tool
def editDistance(source,Target)-> float:
    """Schema Matching 3: Computes normalized edit distance similarity between two column names"""
	spark=getSparkSession()
	sourceCleanVersion,targetCleanVersion=source.lower().strip(), target.lower().strip()
	maxLength=max((len(sourceCleanVersion),len(targetCleanVersion))
	if maxLength==0:
		return 1.0
	df=spark.createDataFrame(([sourceCleanVersion,targetCleanVersion],["source","target"])
	distance=df.select(F.levenshtein(F.col("source"),F.col("target"))).collect()
	return round(float(1.0-(distance/maxLength)),4)



