# pylint: disable=W1203
"""
Function gets data from WordPress API and stores as JSON in S3.
"""
import logging
import boto3
import botocore
import awswrangler as wr
import pandas as pd
from botocore.client import BaseClient


#################
### FUNCTIONS ###
#################


def send_sns_message(sns_client: BaseClient, topic_arn: str, subject: str, message: str) -> None:
    """
    Sends messages via AWS SNS.
    """
    try:
        logging.info(f"Attempting to send SNS message: {subject}...")
        sns_client.publish(
            TopicArn = topic_arn,
            Message = message,
            Subject = subject
            )
        logging.info(f"SNS message [{subject}] sent.")

    except botocore.exceptions.ClientError as ec:
        logging.error(f"SNS message [{subject}] not sent: {ec}")


def get_parameter_from_ssm(ssm_client: BaseClient, parameter_name: str) -> str:
    """
    Gets parameter from AWS Parameter Store.
    RETURNS: Parameter, Value, or a blank string to allow graceful fail.
    """
    try:
        logging.info(f"Attempting to get parameter {parameter_name}...")
        response = ssm_client.get_parameter(Name = parameter_name)

        logging.info("Parameter found.")
        return response['Parameter']['Value']

    except ssm_client.exceptions.ParameterNotFound as pnf:
        logging.warning(f"Parameter {parameter_name} not found: {pnf}")
        return ""

    except botocore.exceptions.ParamValidationError as epv:
        logging.error(f"Error getting parameter {parameter_name}: {epv}")
        return ""

    except botocore.exceptions.ClientError as ec:
        logging.error(f"Error getting parameter {parameter_name}: {ec}")
        return ""


def get_objectname_from_s3_path(path: str) -> str:
    """
    Gets object name from S3 path.
    RETURNS: Object name, or a blank string upon exception
    """
    try:
        # Get name from endpoint
        name_full = path.rsplit('/')[-1]

        # Get final period instance
        name_full_last_period_index = name_full.rfind('.')

        # Extract string before final underscore
        name_partial = name_full[:name_full_last_period_index]
        return name_partial

    except Exception as e:
        logging.exception(e)
        return ""


def get_data_from_s3_object(boto3_session: BaseClient, s3_object: str, name: str) -> pd.DataFrame:
    """
    Get data from S3 object.
    RETURNS: DataFrame (populated or empty)
    """
    try:
        logging.info(f"Attempting to read {name} data at {s3_object}...")
        df = wr.s3.read_parquet(path = s3_object,
                             boto3_session = boto3_session)
        return df

    except wr.exceptions.NoFilesFound as e:
        logging.warning(f"No files found for {name} at {s3_object}: {e}")
        return pd.DataFrame()

    except botocore.exceptions.ClientError as e:
        logging.error(f"{name} data S3 read failed: {e}")
        return pd.DataFrame()



def transform_data(object_name: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms DataFrame based on object name
    RETURNS: transformed pandas DataFrame
    """
    # posts transformations
    if object_name == 'posts':

        # Drop unneeded columns
        df = df.drop(columns=['post_date_gmt', 'post_excerpt',
            'comment_status', 'ping_status', 'post_name', 'to_ping',
            'pinged', 'post_modified_gmt', 'post_content_filtered',
            'guid', 'menu_order', 'post_mime_type', 'comment_count'])

        # Partition dates
        df['post_date_todate'] = pd.to_datetime(df['post_date'])

        df['post_date_year'] = df['post_date_todate'].dt.year
        df['post_date_month'] = df['post_date_todate'].dt.month
        df['post_date_day'] = df['post_date_todate'].dt.day

        df['post_modified_todate'] = pd.to_datetime(df['post_modified'])

        df['post_modified_year'] = df['post_modified_todate'].dt.year
        df['post_modified_month'] = df['post_modified_todate'].dt.month
        df['post_modified_day'] = df['post_modified_todate'].dt.day

    # statistics_pages transformations
    elif object_name == 'statistics_pages':

        # Partition dates
        df['date_todate'] = pd.to_datetime(df['date'])

        df['date_year'] = df['date_todate'].dt.year
        df['date_month'] = df['date_todate'].dt.month
        df['date_day'] = df['date_todate'].dt.day

    # term_relationship transformations
    elif object_name == 'term_relationship':

        # Drop unneeded columns
        df = df.drop(columns=['term_order'])

    # term_taxonomy transformations
    elif object_name == 'term_taxonomy':

        # Drop unneeded columns
        df = df.drop(columns=['description', 'parent'])

    # terms transformations
    elif object_name == 'terms':

        # Drop unneeded columns
        df = df.drop(columns=['term_group'])

        # Amend column to swap '&amp;' for '&'
        df['name'] = df['name'].str.replace('&amp;', '&')

    return df


def put_s3_parquet_object(df: pd.DataFrame, name: str, s3_object_silver: str, session: BaseClient) -> bool:
    """
    Uploads pandas DataFrame to S3 as Parquet.
    RETURNS: True or False depending on outcome
    """
    try:
        logging.info(f"Attempting to put {name} data in {s3_object_silver}...")
        wr.s3.to_parquet(df = df, path = s3_object_silver, boto3_session = session)
        logging.info(f"{name} data S3 upload successful.")
        return True

    except botocore.exceptions.ClientError as e:
        logging.error(f"{name} data S3 upload failed: {e}")
        return False


#############
### START ###
#############

def wordpress_api_silver_handler():
    """
    Main handler for AWS Lambda service.
    """

    ###############
    ### LOGGING ###
    ###############

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s]: %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        force = True
        )


    #################
    ### VARIABLES ###
    #################

    # AWS sessions and clients
    session = boto3.Session()
    client_ssm = session.client('ssm')
    client_sns = session.client('sns')
    client_sts = session.client('sts')

    # AWS Parameter Store Names
    parametername_s3bucket_bronze: str = '/s3/lakehouse/name/bronze'
    parametername_s3bucket_silver: str = '/s3/lakehouse/name/silver'
    parametername_snstopic: str = '/sns/data/lakehouse/silver'

    # Lambda name for messages
    data_source: str = 'wordpress_api'
    function_name: str = f'data_{data_source}_silver'

    # Counters
    object_count_all: int = 0
    object_count_failure: int = 0
    object_count_success: int = 0


    ##################
    ### PARAMETERS ###
    ##################

    # Get & display AWS AccountID
    identity = client_sts.get_caller_identity()
    account_id = identity['Account']
    logging.info(f"Starting in AWS Account ID {account_id}")

    # Get SNS topic from Parameter Store
    logging.info("Getting SNS parameter...")
    sns_topic = get_parameter_from_ssm(client_ssm, parametername_snstopic)

    # Check an SNS topic has been returned.
    if not sns_topic:
        message = "No SNS topic returned."
        logging.warning(message)
        raise ValueError(message)

    # Get S3 bucket name from Parameter Store
    logging.info("Getting S3 Bronze parameter...")
    s3_bucket_bronze = get_parameter_from_ssm(client_ssm, parametername_s3bucket_bronze)

    # Check an S3 bucket has been returned.
    if not s3_bucket_bronze:
        message = f"{function_name}: No S3 Bronze bucket returned."
        subject = f"{function_name}: Failed"

        logging.warning(message)
        send_sns_message(client_sns, sns_topic, subject, message)
        return

    # Get S3 bucket name from Parameter Store
    logging.info("Getting S3 Silver parameter...")
    s3_bucket_silver = get_parameter_from_ssm(client_ssm, parametername_s3bucket_silver)

    # Check an S3 bucket has been returned.
    if not s3_bucket_silver:
        message = f"{function_name}: No S3 silver bucket returned."
        subject = f"{function_name}: Failed"

        logging.warning(message)
        send_sns_message(client_sns, sns_topic, subject, message)
        return

    # Capture all s3 paths in s3_objects and total them in endpoint_total
    s3_objects_bronze = wr.s3.list_objects(path = f's3://{s3_bucket_bronze}/{data_source}',
                                        suffix = 'parquet',
                                        boto3_session = session
                                        )

    # Count the endpoints and log the total
    object_total = len(s3_objects_bronze)
    logging.info(f"{object_total} S3 objects returned.")


    ###############
    ### OBJECTS ###
    ###############

    for s3_object_bronze in s3_objects_bronze:

        # Increment & log counter
        object_count_all += 1
        logging.info(f"Processing object {object_count_all} of {object_total}.")

        # Get filename from endpoint
        object_name = get_objectname_from_s3_path(s3_object_bronze)

        # If no name returned, record failure & end current iteration
        if not object_name:
            logging.warning(f"Unable to parse name from {s3_object_bronze}.")
            endpoint_count_failure += 1
            continue

        # Get data from S3 Bronze object
        logging.info(f"Attempting to read {object_name} data...")
        df = get_data_from_s3_object(session, s3_object_bronze, object_name)

        # Check DataFrame is populated
        if df.empty:
            logging.warning(f"{object_name} DataFrame is empty!")
            endpoint_count_failure += 1
            continue

        logging.info(f'{object_name} DataFrame has {len(df.columns)} columns and {len(df)} rows.')

        ##################
        ### TRANSFORMS ###
        ##################

        logging.info(f'Beginning {object_name} transformations...')


        # Check if object is mapped and bypass if not.
        if object_name not in {
            'posts', 'statistics_pages', 'term_relationship', 'term_taxonomy', 'terms'
            }:
            logging.warning(f'{object_name} is not currently mapped.  Skipping transform...')
            object_count_failure += 1
            continue

        df = transform_data(object_name, df)

        logging.info(f'{object_name} DataFrame now has {len(df.columns)} columns and {len(df)} rows.')

        # Create S3 Silver object path
        s3_object_silver = f's3://{s3_bucket_silver}/{data_source}/{object_name}/{object_name}.parquet'

        logging.info(f"Attempting {object_name} S3 Silver upload...")
        ok = put_s3_parquet_object(df, object_name, s3_object_silver, session)

        # Iteration summaries
        if not ok:
            logging.warning("S3 Silver upload failed!")
            object_count_failure += 1

        else:
            logging.info("S3 Silver upload complete.")
            object_count_success += 1


    ###############
    ### SUMMARY ###
    ###############

    logging.info("WordPress API Silver process complete: " \
                 f"{object_count_success} Successful | {object_count_failure} Failed.")

    # Send SNS notification if any failures found
    if object_count_failure > 0:
        message = f"{function_name} ran with {object_count_failure} errors.  Please check logs."
        subject = f"{function_name}: Ran With Failures"

        logging.warning(message)
        send_sns_message(client_sns, sns_topic, subject, message)

# Run Silver handler
wordpress_api_silver_handler()
