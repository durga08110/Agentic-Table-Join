
from langchain.tools import tool
from src.sparkSession import getSparkSession


@tool
def dataProfiling(filePath:str)->str:
    '''Generates a data profile for a given file. Outputs list of columns, data type, few sample values'''
    spark=getSparkSession()
    profile=[] #store profile information as a list of string
    df = spark.read.csv(
        filePath,
        sep="\t",
        inferSchema=True        
        )
    
    for col in df.columns:

        #select 5 samples of that column and add it as a list
        #can improve sampling strategy based on earlier papers
        samples=[str(row[0]) for row in df.select(col).dropna().distinct().limit(5).collect()]
        samples=",".join(samples)

        #profile would have ["Column:city|Type:str|Samples:Jersey City,Brooklyn"]
        profile.append(f"Column:`{col}`|Type:`{df.schema[col].dataType}`|Samples:[{samples}]")
        
    return "\n".join(profile)