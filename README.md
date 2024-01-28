# pinterest-data-pipeline273

## About this project

Pinterest is the visual discovery engine where users can find ideas and inspiration in fashion, crafts, style, interior, creators and many other topics, personalised to their taste. From data perspective, Pinterest does everything from online data systems, to logging data, big data and stream processing platforms, analytics and more. It also is a massive ML machine generating recommendations for users home feed, search results, related productsand advertisement. Pinterest works with AWS for cloud infrastructure, Percona for MySQL support, along with a number of other companies.

In this project, two data piplines, similar to those which are used by Pinterest data engineers, were created. First one was built for **Batch Processing**, and used extract-load-transform (ELT) data integration processes. The second one was set up for **Data Streaming**, and differently to Batch Processing, implemented extract-transform-load (ETL) procedures. Various AWS tools (EC2, S3, MSK, API Gateway, etc) and Databricks platform were used to complete the project.

## Data

## Configuration 

Create AWS, GitHub and Databrics accounts.

### Batch Processing 

1. Set up an **AWS EC2 Kafka client machine**. This creates three topics which is necessary for data loading and storage in AWS S3 bucket. 

    - Connect to EC2 instance.
    - Install Kafka on EC2 instance.
    - Install the IAM MSK authentication package on your client EC2 machine.
    - Get necessary permissions to authenticate to the MSK cluster.
    - Configure your Kafka client to use AWS IAM authentication to the cluster.
    - Create Kafka topics:

            1. <your_UserId>.pin for the Pinterest posts data.
            2. <your_UserId>.geo for the post geolocation data.
            3. <your_UserId>.user for the post user data.

1. Connect an **AWS MSK cluster** to an **AWS S3 bucket**. **AWS MSK Connect** connects an MSK cluster to an S3 bucket, so that the data going through the cluster is saved and stored in a dedicated S3 bucket. 

    (S3 bucket, an IAM role that allows you to write to this bucket or a VPC Endpoint to S3 have been already configured in the AWS account.)

    - Download Confluent.io Amazon S3 Connector on the EC2 client.
    - Copy it to the bucket with your user id.
    - Create your custom plugin with the following name: <your_UserId>-plugin in the MSK Connect console.
    - Create a connector: <your_UserId>-connector, and choose the IAM role used for authentication to the MSK cluster in the Access permissions tab: <your_UserId>-ec2-access-role. 

    Now that the plugin-connector pair was built, data passing through the IAM authenticated cluster, will be automatically stored in the designated S3 bucket.

    ![image](/Users/eglute/Desktop/p_c.png)

1. 










    




## Cloning to your local device



## Other

### Main files



### Lisence

    This project is licensed under the MIT lisence.