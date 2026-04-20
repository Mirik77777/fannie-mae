#Verify Spark session is active and confirm version
 print(f"Spark version: {spark.version}") 
print(f"App name: {spark.sparkContext.appName}")
