from pyspark.sql import SparkSession

def getSparkSession() -> SparkSession:
     spark = SparkSession.builder \
    .appName("FrequentItems") \
    .master("yarn") \
    .config("spark.submit.deployMode", "client") \
    .config("spark.driver.memory", "16g") \
    .config("spark.driver.maxResultSize", "4g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.instances", "10") \
    .config("spark.sql.shuffle.partitions","10")\
    .getOrCreate()

    return spark