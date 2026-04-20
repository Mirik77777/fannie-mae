# Load Parquet data from S3 and register as SQL temporary view
df = spark.read.parquet("s3://fanniemaedataraw/individual_cw_parquet/") df.createOrReplaceTempView("raw_fannie")
 spark.sql("SELECT COUNT(*) AS total_records FROM raw_fannie").show()
