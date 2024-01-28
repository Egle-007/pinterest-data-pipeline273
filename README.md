# pinterest-data-pipeline273

## About this project

Pinterest is the visual discovery engine where users can find ideas and inspiration in fashion, crafts, style, interior, creators and many other topics, personalised to their taste. From data perspective, Pinterest does everything from online data systems, to logging data, big data and stream processing platforms, analytics and more. It also is a massive ML machine generating recommendations for users home feed, search results, related productsand advertisement. Pinterest works with AWS for cloud infrastructure, Percona for MySQL support, along with a number of other companies.

In this project, two data piplines, similar to those which are used by Pinterest data engineers, were created. First one was built for **Batch Processing**, and used extract-load-transform (ELT) data integration processes. The second one was set up for **Data Streaming**, and differently to Batch Processing, implemented extract-transform-load (ETL) procedures. Various AWS tools (EC2, S3, MSK, API Gateway, etc) and Databricks platform were used to complete the project.

## Data

<!-- ![plug_conn](Pictures/p_c.png)
![plug_conn](Pictures/plugin.png) -->

## Configuration 

Create AWS, GitHub and Databrics accounts.

### Batch Processing configuration

1. Set up an **AWS EC2 Kafka client machine**. This creates three topics which is necessary for data loading and storage in AWS S3 bucket. 

    - Connect to EC2 instance.
    - Install Kafka on EC2 instance.
    - Install the IAM MSK authentication package on your client EC2 machine.
    - Get necessary permissions to authenticate to the MSK cluster.
    - Configure your Kafka client to use AWS IAM authentication to the cluster.
    - Create Kafka topics:

            1. <your_UserId>.pin for the Pinterest posts data,
            2. <your_UserId>.geo for the post geolocation data,
            3. <your_UserId>.user for the post user data.

1. Connect an **AWS MSK cluster** to an **AWS S3 bucket**. **AWS MSK Connect** connects an MSK cluster to an S3 bucket, so that the data going through the cluster is saved and stored in a dedicated S3 bucket. 

    S3 bucket, an IAM role that allows you to write to this bucket or a VPC Endpoint to S3 have been already configured in the AWS account.

    - Download Confluent.io Amazon S3 Connector on the EC2 client.
    - Copy it to the bucket with your user id.
    - Create your custom plugin with the following name: <your_UserId>-plugin in the MSK Connect console.
    - Create a connector: <your_UserId>-connector, and choose the IAM role used for authentication to the MSK cluster in the Access permissions tab: <your_UserId>-ec2-access-role. 

    Now that the plugin-connector pair was built, data passing through the IAM authenticated cluster, will be automatically stored in the designated S3 bucket.


1. Configure HTTP API in **AWS API Gateway**. This API is meant for sending the data to MSK cluster, which then is stored in an S3 bucket. 

    API have already been created for the user. 

    - Build a Kafka REST Proxy integration, which provides a RESTful interface to a Kafka cluster: 
        - Create a resource that allows you to build an HTTP PROXY integration for your API in API Gateway console.
        - Create an HTTP ANY method for this resource. For Endpoint URL use Kafka Client Amazon EC2 Instance PublicDNS.
        - Deploy the API and make a note of the Invoke URL.

    - Set up Kafka REST proxy on the EC2 client: 
        - Install the Confluent package for the Kafka REST Proxy on your EC2 client machine. 
        - Allow the REST proxy to perform IAM authentication to the MSK cluster by modifying the kafka-rest.properties file.
        - Start the REST proxy on the EC2 client machine.

    - Send data to your API:
        - Modify the user_posting_emulation.py to send data from the three tables to their corresponding Kafka topics using your API Invoke URL.
        - Check if data is getting stored in the S3 bucket.
    

1. Mount an **AWS S3 bucket** to **Databricks platform**. Databricks is built upon Apache Spark, a powerful open-source distributed computing system that enables parallel processing of large datasets. 

    - Mount the desired S3 bucket to the Databricks account, so that the batch data could be cleaned and queries made.
    - Create  three DataFrames:

        1. df_pin for the Pinterest post data,
        2. df_geo for the geolocation data,
        3. df_user for the user data.

1. After data transformation, create and upload **DAG** to **AWS MWAA** environment.

    AWS account has been already been provided with access to a MWAA environment Databricks-Airflow-env and to its S3 bucket mwaa-dags-bucket. 

    - Create an Airflow DAG that will trigger a Databricks Notebook to be run on a daily schedule.
    - Upload it to the dags folder in the mwaa-dags-bucket.
    - Manually trigger the DAG and check if it runs successfully.

### Streaming configuration

1. Create data streams using **AWS Kinesis** Data Streams. Kinesis Data Streams is a serverless streaming data service that makes it easy to capture, process, and store data streams.

    - Using Kinesis Data Streams create three data streams, one for each Pinterest table.

1. Configure previously created REST API to allow it to invoke Kinesis actions. AWS account has been granted the necessary permissions to invoke Kinesis actions.

1. Send data to Kinesis streams. 

    - Create a new script user_posting_emulation_streaming.py, that builds upon the initial user_posting_emulation.py you have been provided with.
    - Modify the script so that it can send requests to your API, which adds one record at a time to the streams you have created. The data should be sent from the three Pinterest tables to their corresponding Kinesis stream.

1. Read data from Kinesis sreams to Databricks.

    - Create a new Notebook in Databricks and read in your credentials.
    - Run your preferred method to ingest data into Kinesis Data Streams. In the Kinesis console, check your data streams are receiving the data.
    - Read the data from the three streams you have created in your Databricks Notebook.













    




## Cloning to your local device



## Other

### Main files



### Lisence

    This project is licensed under the MIT lisence.