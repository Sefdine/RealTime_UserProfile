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

### RandomUser API

The data in the randomuser.me API is structured as follows:

1. **Gender**: A string indicating the gender of the individual.
2. **Name**:
   - **Title**: A string representing the person's title.
   - **First Name**: A string representing the person's first name.
   - **Last Name**: A string representing the person's last name.
3. **Location**:
   - **Street**:
     - **Number**: An integer representing the street number.
     - **Name**: A string representing the street name.
   - **City**: A string representing the city.
   - **State**: A string representing the state.
   - **Country**: A string representing the country.
   - **Postcode**: A string representing the postal code.
   - **Coordinates**:
     - **Latitude**: A string representing the latitude.
     - **Longitude**: A string representing the longitude.
   - **Timezone**:
     - **Offset**: A string representing the UTC offset.
     - **Description**: A string describing the timezone.
4. **Email**: A string representing the email address.
5. **Login**:
   - **UUID**: A string representing the universally unique identifier.
   - **Username**: A string representing the username.
   - **Password**: A string representing the password.
   - **Salt**: A string used in password hashing.
   - **MD5**: A string representing the MD5 hash.
   - **SHA1**: A string representing the SHA1 hash.
   - **SHA256**: A string representing the SHA256 hash.
6. **Date of Birth (DOB)**:
   - **Date**: A string representing the date of birth.
   - **Age**: An integer representing the age.
7. **Registered**:
   - **Date**: A string representing the registration date.
   - **Age**: An integer representing the registration age.
8. **Phone**: A string representing the phone number.
9. **Cell**: A string representing the cell phone number.
10. **ID**:
    - **Name**: A string representing the identifier's name.
    - **Value**: A string representing the identifier's value.
11. **Picture URLs**:
    - **Large**: A string representing the URL of the large picture.
    - **Medium**: A string representing the URL of the medium-sized picture.
    - **Thumbnail**: A string representing the URL of the thumbnail picture.
12. **Nationality (Nat)**: A string representing the nationality.

### Transformation

The transformation performed aligns with GDPR compliance, and here is a breakdown of the steps:

- Concatenation of the first name and last name to create an encrypted complete name.
- Creation of an encrypted full address.
- Conversion of dates into a standardized date format.
- Removal of the age field since the date of birth is available for age calculation.
- Establishment of a hierarchy for date-related fields.
- Encryption of sensitive information such as email, phone, and cell numbers.