"""
Function gets data from WordPress API and stores as JSON in S3.
"""
import logging
import json
import requests
import boto3
import botocore


#################
### FUNCTIONS ###
#################


def send_sns_message(sns_client, topic_arn: str, subject:str, message: str):
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


def get_parameter_from_ssm(ssm_client, parameter_name: str) -> str:
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


def get_filename_from_endpoint(endpoint: str) -> str:
    """
    Creates filename using API endpoint
    RETURNS: filename, or a blank string upon exception
    """
    try:
        # Get name from endpoint
        name_full = endpoint.rsplit('/')[-2]

        # Get final underscore instance
        name_full_last_underscore_index = name_full.rfind('_')

        # Extract string before final underscore
        name_partial = name_full[:name_full_last_underscore_index]
        return name_partial

    except Exception as e:
        logging.exception(e)
        return ""


def get_wordpress_api_json(requests_session, api_url: str, api_call_timeout: int) -> dict:
    """
    Gets JSON from WordPress API.
    RETURNS: JSON string, or an exception if the API call fails
    """
    try:
        logging.info(f"Sending request to {api_url} endpoint...")
        response = requests_session.get(api_url, timeout = api_call_timeout)

        if response.status_code == 200:
            json_raw = response.json()
            logging.info(f"API response: {response.status_code} {response.reason}")
            return json_raw

        else:
            logging.error(f"API response: {response.status_code} {response.reason} - {response.text}")
            raise ValueError (f"API response: {response.status_code} {response.reason} - {response.text}")

    except requests.exceptions.Timeout as et:
        logging.error(f"API call request timed out after {api_call_timeout} seconds!")
        raise Exception from et

    except requests.exceptions.RequestException as e:
        logging.exception(f"Error during API call to {api_url}: {e}")
        raise Exception from e


def put_s3_object(s3_client, bucket: str, name: str, json_data: str) -> bool:
    """
    Uploads API JSON data to S3.
    RETURNS True or False depending on outcome
    """
    try:
        logging.info(f"Attempting to put {name} data in {bucket} bucket...")
        s3_client.put_object(
            Body = json_data,
            Bucket = bucket,
            Key = f"wordpress-api/{name}.json"
        )
        logging.info(f"{name} API data S3 upload successful.")
        return True

    except botocore.exceptions.ClientError as e:
        logging.error(f"{name} API data S3 upload failed: {e}")
        return False


#############
### START ###
#############

def lambda_handler(event, context):
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
    client_s3 = session.client('s3')
    client_sns = session.client('sns')
    requests_session = requests.Session()

    # AWS Parameter Store Names
    parametername_s3bucket = '/s3/lakehouse/name/raw'
    parametername_snstopic = '/sns/pipeline/wordpressapi/raw'
    parametername_wordpressapi = '/wordpress/amazonwebshark/api/mysqlendpoints'

    # Lambda name for messages
    lambdaname = 'data_wordpressapi_raw'

    # Counters
    api_call_timeout = 30
    endpoint_count_all = 0
    endpoint_count_failure = 0
    endpoint_count_success = 0


    ##################
    ### PARAMETERS ###
    ##################

    # Get SNS topic from Parameter Store
    logging.info("Getting SNS parameter...")
    sns_topic = get_parameter_from_ssm(client_ssm, parametername_snstopic)

    # Check an SNS topic has been returned.
    if not sns_topic:
        message = "No SNS topic returned."
        logging.warning(message)
        raise ValueError(message)

    # Get the WordPress endpoints from Parameter Store and convert the string to a list
    logging.info("Getting WordPress parameter...")
    api_endpoints_list = get_parameter_from_ssm(client_ssm, parametername_wordpressapi).split(",")

    # Check the API list isn't empty
    if not any(api_endpoints_list):
        message = "No API endpoints returned."
        subject = f"{lambdaname}: Failed"

        logging.warning(message)
        send_sns_message(client_sns, sns_topic, subject, message)
        return

    # Count the endpoints and log the total
    endpoint_total = len(api_endpoints_list)
    logging.info(f"{endpoint_total} API endpoints returned.")

    # Get S3 bucket name from Parameter Store
    logging.info("Getting S3 parameter...")
    s3_bucket = get_parameter_from_ssm(client_ssm, parametername_s3bucket)

    # Check an S3 bucket has been returned.
    if not s3_bucket:
        message = "No S3 bucket returned."
        subject = f"{lambdaname}: Failed"

        logging.warning(message)
        send_sns_message(client_sns, sns_topic, subject, message)
        return


    #################
    ### ENDPOINTS ###
    #################

    for api_endpoint in api_endpoints_list:

        # Increment & log counter
        endpoint_count_all += 1
        logging.info(f"Processing endpoint {endpoint_count_all} of {endpoint_total}")

        # Get filename from endpoint
        object_name = get_filename_from_endpoint(api_endpoint)

        # If no name returned, record failure & end current iteration
        if not object_name.strip():
            logging.warning(f"Unable to parse name from {api_endpoint}.")
            endpoint_count_failure += 1
            continue

        # Get data using the endpoint
        logging.info(f"Attempting API query for {object_name}...")
        api_json = get_wordpress_api_json(requests_session, api_endpoint, api_call_timeout)

        # If no data returned, record failure & end current iteration
        if not api_json:
            logging.warning("Skipping attempt due to API call failure.")
            endpoint_count_failure += 1
            continue

        # If API does return data, transform to a json string and upload this to S3.
        api_json_string = json.dumps(api_json)

        logging.info("Attempting API data S3 upload...")
        ok = put_s3_object(client_s3, s3_bucket, object_name, api_json_string)

        # Iteration summaries
        if not ok:
            logging.warning("S3 Upload failed!")
            endpoint_count_failure += 1

        else:
            logging.info("S3 Upload complete.")
            endpoint_count_success += 1


    ###############
    ### SUMMARY ###
    ###############
    logging.info("WordPress API Raw process complete: " \
                 f"{endpoint_count_success} Successful | {endpoint_count_failure} Failed.")

    # Send SNS notification if any failures found
    if endpoint_count_failure > 0:
        message = f"{lambdaname} ran with {endpoint_count_failure} errors.  Please check logs."
        subject = f"{lambdaname}: Ran With Failures"

        logging.warning(message)
        send_sns_message(client_sns, sns_topic, subject, message)
