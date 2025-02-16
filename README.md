# Introduction
This repo contains artefacts for my amazonwebshark tech blog.  It was created to remove the need for multiple repos containing small collections of artefacts, and to reduce the volume of GitHub Gists.

## What This Repo Contains
The following list is not exhaustive:

- Architecture Diagrams, either as images and/or as the [Diagrams.Net](https://app.diagrams.net/) code used to generate them.
- Scripts of actual solutions, with redactions where needed.
- Scripts of hypothetical solutions within a post's context.
- Supporting content for posts that may not have been used in the final product.

## What This Repo Doesn't Contain
- Solutions, redacted or otherwise, where it makes sense for them to have their own repos (for instance, a Python module)
- Code snippets that have a good reason to be on GitHub Gists (for example, I want to embed them into the post instead of posting a link)

# Advisory
Artefacts within this repo have been created at various points along my learning journey.  They do not represent best practices, may be poorly optimised or include unexpected bugs, and may become obsolete.  Please keep this in mind when browsing.

# Contents
This list will start with the most recently dated entry, working backwards.

## 2025

Low-Code S3 Key Validation With AWS Step Functions & JSONata

### 2025-02-17-LowCodeS3KeyValidationWithAWSStepFunctionsAndJSONata
Related blog post: [Low-Code S3 Key Validation With AWS Step Functions & JSONata](https://amazonwebshark.com/low-code-s3-key-validation-with-aws-step-functions-jsonata/)

Contents:

- JSON Step Functions code for `Data-Ingestion-iTunes-All` state machine.
- JSON Step Functions code for `Data-Ingestion-iTunes` state machine.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Wolfie Lakehouse Ingestion Outline architectural diagram code.

## 2024

Gold Layer PySpark ETL With AWS Glue Studio

### 2024-11-15-GoldLayerPySparkETLWithAWSGlueStudio
Related blog post: [Gold Layer PySpark ETL With AWS Glue Studio](https://amazonwebshark.com/gold-layer-pyspark-etl-with-aws-glue-studio/)

Contents:

- Python script for Gold WordPress API ETL process.
- JSON Step Functions code for `Wordpress_Gold` state machine.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Glue Gold ETL Job architectural diagram code.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Step Function architectural diagram code.


### 2024-09-02-BespokeVeracityChecksWithAWSGlueDataQuality
Related blog post: [Bespoke Veracity Checks With AWS Glue Data Quality](https://amazonwebshark.com/bespoke-veracity-checks-with-aws-glue-data-quality/)

Contents:

- Glue Data Quality ruleset for `silver-posts` dataset.
- Glue Data Quality ruleset for `silver-statistics_pages` dataset.
- Updated JSON Step Functions code for `Wordpress_Raw_To_Bronze` state machine.


### 2024-08-12-SilverLayerPythonETLWithTheAWSGlueETLJobScriptEditor
Related blog post: [Silver Layer Python ETL With The AWS Glue ETL Job Script Editor](https://amazonwebshark.com/silver-layer-python-etl-with-the-aws-glue-etl-job-script-editor/)

Contents:

- Python script for Silver WordPress API ETL process.
- Updated JSON Step Functions code for `Wordpress_Raw_To_Bronze` state machine.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Glue Silver ETL Job architectural diagram code.
- Supporting [Diagrams.Net](https://app.diagrams.net/) updated Step Function architectural diagram code.


### 2024-05-30-DataDiscoveryWithAWSGlue
Related blog post: [Discovering Data With AWS Glue](https://amazonwebshark.com/discovering-data-with-aws-glue/)

Contents:

- Updated JSON Step Functions code for `Wordpress_Raw_To_Bronze` state machine.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Bronze Glue Crawler architectural diagram code.
- Supporting [Diagrams.Net](https://app.diagrams.net/) updated Step Function architectural diagram code.


### 2024-03-27-WordPressBronzeDataOrchestrationWithAWS
Related blog post: [WordPress Bronze Data Orchestration With AWS](https://amazonwebshark.com/wordpress-bronze-data-orchestration-with-aws/)

Contents:

- Python script for extracting WordPress API raw data with AWS SNS alerting.
- `requirements_raw.txt` file for Python raw virtual environment.
- Python script for extracting WordPress API bronze data with AWS SNS alerting.
- `requirements_bronze.txt` file for Python bronze virtual environment.
- JSON Step Functions code for `Wordpress_Raw_To_Bronze` state machine.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Bronze Lambda architectural diagram code.
- Supporting [Diagrams.Net](https://app.diagrams.net/) Step Function architectural diagram code.


### 2024-02-16-UsingPythonAndAWSToExtractWordPressAPIData
Related blog post: [WordPress Data Extraction Automation With AWS](https://amazonwebshark.com/wordpress-data-extraction-automation-with-aws/)

Contents:

- Python script for extracting WordPress API raw data with AWS SNS alerting.
- `requirements.txt` file for Python virtual environment.
- Supporting [Diagrams.Net](https://app.diagrams.net/) architectural diagram code.


### 2024-02-02-UsingPython&AWSToExtractWordPressAPIData&AWS
Related blog post: [Using Python & AWS To Extract WordPress API Data](https://amazonwebshark.com/using-python-aws-to-extract-wordpress-api-data/)

Contents:

- Python script for extracting WordPress API raw data.
- `requirements.txt` file for Python virtual environment.
- Supporting [Diagrams.Net](https://app.diagrams.net/) architectural diagram code.

<br>

## 2023

### 2023-07-11-EmotiveAmigaCode
Related blog post: [Emotive Amiga Code](https://amazonwebshark.com/emotive-amiga-code/)

Contents: 

- AMOS Solo Pong tutorial scripts.


### 2023-04-30-AutomatingApplicationManagementWithWinget
Related blog post: [Automating Application Management With Winget](https://amazonwebshark.com/automating-application-management-with-winget/)

Contents: 

- Redacted Powershell script showing Winget uses.

<br>

## 2022

### 2022-12-29-MigratingAmazonwebsharkToSiteGround
Related blog post: [Migrating amazonwebshark To SiteGround](https://amazonwebshark.com/migrating-amazonwebshark-to-siteground/)

Contents: 

- Architecture Diagram used in post.
- Supporting [Diagrams.Net](https://app.diagrams.net/) architectural diagram code.


### 2022-08-10-IngestingiTunesDataIntoAWSWithPythonAndAthena
Related blog post: [Ingesting iTunes Data Into AWS With Python And Athena](https://amazonwebshark.com/ingesting-itunes-data-into-aws-with-python-and-athena/)

Contents: 

- Architecture Diagram used in post.
- Supporting [Diagrams.Net](https://app.diagrams.net/) architectural diagram code.


### 2022-03-15-NextLevelS3NotificationsWithEventBridge
Related blog post: [Next-Level S3 Notifications With EventBridge](https://amazonwebshark.com/next-level-s3-notifications-with-eventbridge/)

Contents: 

- Architecture Diagram used in post.
- Supporting [Diagrams.Net](https://app.diagrams.net/) architectural diagram code.


### 2022-02-15-CreatingSecurityAlertsForAWSConsoleAccess
Related blog post: [Creating Security Alerts For AWS Console Access](https://amazonwebshark.com/creating-security-alerts-for-aws-console-access/)

Contents: 

- Architecture Diagram used in post.
- Supporting [Diagrams.Net](https://app.diagrams.net/) architectural diagram code.
