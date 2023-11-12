# Import necessary packages
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_json, col, to_timestamp, date_format, concat_ws, udf
from cassandra.cluster import Cluster
import logging
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from pymongo import MongoClient
from datetime import datetime

# Function to encrypt a value (UDF)
def encrypt_value(value):
    key = b'YourPassword123@'  # Replace with a secure key
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Use PKCS7 padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(value.encode()) + padder.finalize()

    encrypted_value = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_value

encrypt_udf = udf(lambda value: encrypt_value(value), StringType())

# Define a topic name
TOPIC_NAME = 'user_profiles'

print('Connecting to Kafka: ')
try:
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers='localhost:9092')
    print('Connection done !')
except NoBrokersAvailable as ne:
    logging.error('No brokers available: %s', ne)
    sys.exit(1)

# Create a Spark session
spark = SparkSession.builder.appName("KafkaCassandraIntegration").getOrCreate()

# Define the schema
schema = StructType([
    StructField("gender", StringType(), True),
    StructField("name", StructType([
        StructField("title", StringType(), True),
        StructField("first", StringType(), True),
        StructField("last", StringType(), True)
    ]), True),
    StructField("location", StructType([
        StructField("street", StructType([
            StructField("number", IntegerType(), True),
            StructField("name", StringType(), True)
        ]), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True),
        StructField("postcode", StringType(), True),
        StructField("coordinates", StructType([
            StructField("latitude", StringType(), True),
            StructField("longitude", StringType(), True)
        ]), True),
        StructField("timezone", StructType([
            StructField("offset", StringType(), True),
            StructField("description", StringType(), True)
        ]), True)
    ]), True),
    StructField("email", StringType(), True),
    StructField("login", StructType([
        StructField("uuid", StringType(), True),
        StructField("username", StringType(), True),
        StructField("password", StringType(), True),
        StructField("salt", StringType(), True),
        StructField("md5", StringType(), True),
        StructField("sha1", StringType(), True),
        StructField("sha256", StringType(), True)
    ]), True),
    StructField("dob", StructType([
        StructField("date", StringType(), True),
        StructField("age", IntegerType(), True)
    ]), True),
    StructField("registered", StructType([
        StructField("date", StringType(), True),
        StructField("age", IntegerType(), True)
    ]), True),
    StructField("phone", StringType(), True),
    StructField("cell", StringType(), True),
    StructField("id", StructType([
        StructField("name", StringType(), True),
        StructField("value", StringType(), True)
    ]), True),
    StructField("picture", StructType([
        StructField("large", StringType(), True),
        StructField("medium", StringType(), True),
        StructField("thumbnail", StringType(), True)
    ]), True),
    StructField("nat", StringType(), True)
])

# Connect to Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect()
cassandra_keyspace = 'user_profiles'

# Create keyspace and table if they don't exist
session.execute(f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor':1}}")
session.execute(f"USE {cassandra_keyspace}")

# Create the table if it does not exist
session.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        gender text,
        complete_name text,
        complete_address text,
        timezone_offset text,
        timezone_description text,
        email text,
        dob_date timestamp,
        dob_year text,
        dob_month text,
        dob_day text,
        dob_hours text,
        dob_minutes text,
        registration_date timestamp,
        phone text,
        cell text,
        id_name text,
        id_value text,
        picture_thumbnail text,
        nat text,
        insertion_timestamp timestamp,
        PRIMARY KEY (email, insertion_timestamp)
    ) WITH CLUSTERING ORDER BY (insertion_timestamp DESC);
    """
)

# Create the index if not exists
session.execute(
    """
        CREATE INDEX IF NOT EXISTS idx_insertion_timestamp ON users (insertion_timestamp);
    """
)

# Prepare the insert statement
insert_statement = session.prepare(
    """
    INSERT INTO users 
    (gender, complete_name, complete_address, timezone_offset, 
    timezone_description, email, dob_date, dob_year, dob_month, dob_day,
    dob_hours, dob_minutes, registration_date, phone, cell, id_name, 
    id_value, picture_thumbnail, nat, insertion_timestamp) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, toUnixTimestamp(now()))
    """
)


# Mongo code -------------------------
# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["user_profiles"]
mongo_collection = mongo_db["users"]

users_count = 0
for message in consumer:
    # Convert the bytes object to a string
    message_str = message.value.decode('utf-8')
    # Create a dataframe
    df = spark.createDataFrame([message_str], StringType())

    # Parse the JSON data
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", schema).alias("data")) \
        .select("data.*")
    
    transformed_df = parsed_df.withColumn(
        "complete_name",
        concat_ws(" ", col("name.first"), col("name.last"))
    ).withColumn(
        "complete_address",
        concat_ws(", ",
            col("location.street.number").cast("string"),
            col("location.street.name"),
            col("location.city"),
            col("location.state"),
            col("location.country"),
            col("location.postcode")
        )
    ).withColumn(
        "dob_date", to_timestamp(col("dob.date"), "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
    ).withColumn(
        "dob_day", date_format(col("dob_date"), "d")
    ).withColumn(
        "dob_month", date_format(col("dob_date"), "M")
    ).withColumn(
        "dob_year", date_format(col("dob_date"), "y")
    ).withColumn(
        "dob_hours", date_format(col("dob_date"), "H")
    ).withColumn(
        "dob_minutes", date_format(col("dob_date"), "m")
    ).withColumn(
        "registration_date",
        to_timestamp(col("registered.date"), "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
    ).withColumn(
        'email', encrypt_udf("email")
    ).withColumn(
        'phone', encrypt_udf("phone")
    ).withColumn(
        'cell', encrypt_udf("cell")
    ).withColumn(
        'complete_name', encrypt_udf("complete_name")
    ).withColumn(
        'complete_address', encrypt_udf("complete_address")
    )

    # Select the required columns
    transformed_df = transformed_df.select(
        "gender", "complete_name", "complete_address", "location.timezone.offset",
        "location.timezone.description", "email", "dob_date","dob_year", "dob_month",
        "dob_day", "dob_hours", "dob_minutes", "registration_date", "phone", "cell",
        "id.name", "id.value", "picture.thumbnail", "nat"
    )

    try:

        # Convert the DataFrame to a list of values
        values = transformed_df.rdd.map(list).collect()
        # Insert the data into the Cassandra table
        session.execute(insert_statement, values[0])


        # Create a document with the specified fields
        age = datetime.now().year - int(values[0][7])
        document = {
            "gender": values[0][0],
            "age": age,
            "complete_name": encrypt_value(values[0][1]),
            "complete_address": encrypt_value(values[0][2]),
            "timezone_offset": values[0][3],
            "timezone_description": values[0][4],
            "dob_date": values[0][6],
            "dob_year": values[0][7],
            "dob_month": values[0][8],
            "dob_day": values[0][9],
            "dob_hours": values[0][10],
            "dob_minutes": values[0][11],
            "registration_date": values[0][12],
            "id_name": values[0][15],
            "id_value": values[0][16],
            "picture_thumbnail": values[0][17],
            "nat": values[0][18],
            "insertion_timestamp": datetime.now()
        }
        # Insert the document into the collection
        mongo_collection.insert_one(document)

        users_count += 1
        print(f"User {users_count} inserted successfully in Cassandra and MongoDB.")        

    except Exception as e:
        print('Error: ',e)

    