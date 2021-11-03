import os

# default to local environment
# Production servers should set this env variable to 'production'
exec_env = os.getenv("EXECUTION_ENV", "local")

if exec_env == "local":
    DYNAMO_DB_ENDPOINT_URL = "http://localhost:9000"
elif exec_env == "production":
    DYNAMO_DB_ENDPOINT_URL = "https://dynamodb.us-west-1.amazonaws.com"

SHORT_URL_BASE = "https://tier.app/"
