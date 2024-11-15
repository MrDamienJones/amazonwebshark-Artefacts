import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node S3 Silver statistics_pages
S3Silverstatistics_pages_node1724058965930 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://data-lakehouse-silver/wordpress_api/statistics_pages/"], "recurse": True}, transformation_ctx="S3Silverstatistics_pages_node1724058965930")

# Script generated for node S3 Silver posts
S3Silverposts_node1724058915313 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://data-lakehouse-silver/wordpress_api/posts/"], "recurse": True}, transformation_ctx="S3Silverposts_node1724058915313")

# Script generated for node Join
Join_node1724059035756 = Join.apply(frame1=S3Silverposts_node1724058915313, frame2=S3Silverstatistics_pages_node1724058965930, keys1=["ID"], keys2=["id"], transformation_ctx="Join_node1724059035756")

# Script generated for node Change Schema
ChangeSchema_node1724059144495 = ApplyMapping.apply(frame=Join_node1724059035756, mappings=[("ID", "bigint", "post_ID", "long"), ("post_title", "string", "post_title", "string"), ("post_status", "string", "post_status", "string"), ("post_parent", "bigint", "post_parent", "long"), ("post_type", "string", "post_type", "string"), ("post_date_todate", "timestamp", "post_date", "timestamp"), ("post_date_year", "bigint", "post_date_year", "long"), ("post_date_month", "bigint", "post_date_month", "long"), ("post_date_day", "bigint", "post_date_day", "long"), ("page_id", "bigint", "statistics_id", "long"), ("date", "timestamp", "statistics_date", "timestamp"), ("count", "bigint", "statistics_count", "long"), ("date_year", "bigint", "statistics_date_year", "long"), ("date_month", "bigint", "statistics_date_month", "long"), ("date_day", "bigint", "statistics_date_day", "long")], transformation_ctx="ChangeSchema_node1724059144495")

# Script generated for node Filter
Filter_node1724060106174 = Filter.apply(frame=ChangeSchema_node1724059144495, f=lambda row: (bool(re.match("post", row["post_type"]))), transformation_ctx="Filter_node1724060106174")

# Script generated for node S3 Gold
S3Gold_node1724060393283 = glueContext.write_dynamic_frame.from_options(frame=Filter_node1724060106174, connection_type="s3", format="glueparquet", connection_options={"path": "s3://data-lakehouse-gold/wordpress_api/statistics_postname/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="S3Gold_node1724060393283")

job.commit()