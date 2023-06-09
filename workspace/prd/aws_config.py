from os import getenv

from phidata.app.fastapi import FastApiServer
from phidata.aws.config import AwsConfig
from phidata.aws.resource.s3.bucket import AwsResourceGroup, S3Bucket

from workspace.prd.docker_config import prd_api_image
from workspace.settings import ws_settings

#
# -*- Production AWS Resources
#

# -*- Settings
launch_type = "FARGATE"
api_key = f"{ws_settings.prd_key}-api"

# -*- Define S3 bucket for prd data
prd_data_s3_bucket = S3Bucket(
    name=f"{ws_settings.prd_key}-data",
    acl="private",
)

# -*- FastApiServer running on ECS
prd_fastapi = FastApiServer(
    name=api_key,
    enabled=ws_settings.prd_api_enabled,
    image=prd_api_image,
    command=["api", "start"],
    ecs_task_cpu="512",
    ecs_task_memory="1024",
    aws_subnets=ws_settings.subnet_ids,
    # aws_security_groups=ws_settings.security_groups,
    # Get the OpenAI API key from the environment if available
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", "")},
    use_cache=ws_settings.use_cache,
    # Read secrets from a file
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/api_secrets.yml"),
)

#
# -*- Define AWS resources using the AwsConfig
#
prd_aws_config = AwsConfig(
    env=ws_settings.prd_env,
    apps=[prd_fastapi],
    resources=AwsResourceGroup(
        s3_buckets=[prd_data_s3_bucket],
    ),
)
