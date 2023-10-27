# BigDataFlow-UserProfiling-Pipeline-Mastery

The project involves the development and deployment of a real-time data pipeline using PySpark, Kafka, Cassandra, and MongoDB. With a focus on user profile analysis from randomuser.me, the project emphasizes secure data handling, efficient transformation, and insightful data aggregation. The ultimate objective is to create a high-performance data pipeline that complies with GDPR regulations and facilitates informed decision-making through comprehensive data analysis and visualization.

### Project Summary

- Project planning with Jira (Scrum).
- Environment Setup and Dependencies: Ensured proper configuration and installation of PySpark, Kafka, Cassandra, and MongoDB, utilizing Docker images.
- Data Saving Functions Definition: Established functions for saving transformed user profile data into Cassandra tables and MongoDB collections.
- Spark Session Initialization: Created a Spark session with necessary configurations, including paths to dependency JARs.
- Kafka Data Ingestion: Read streaming data from the Kafka topic, "user_profiles".
- Data Transformation: Defined the schema for incoming data based on the structure of randomuser.me. Analyzed incoming Kafka messages, extracted relevant fields, and performed necessary transformations such as constructing full names, validating or recalculating age, and creating complete addresses.
- Data Storage in Cassandra: Saved transformed user profile data into a Cassandra table using the defined function.
- Data Aggregation: Aggregated data for deriving insights, such as the number of users by nationality, average user age, and most common email domains. Saved aggregated results into MongoDB collections.
- Debugging and Monitoring: Monitored console output for aggregated results and potential errors using the "logging" library and 'try-except' blocks. Verified data correctness in Cassandra tables and MongoDB collections.
- Data Visualization: Created dashboards using Python Dash to visualize aggregated data stored in MongoDB.
- GDPR Documentation: Drafted a register detailing all personal data processing, including stored data types, processing purposes, and implemented security measures.
- Access Updates: Adjusted access rights in data ingestion tools within Apache Kafka to reflect organizational changes. Used the script "kafka-acls.sh" to manage access control lists (ACLs).
