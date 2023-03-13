from phidata.app.server import AppServer, ApiServer
from phidata.docker.config import DockerConfig, DockerImage

from workspace.dev.jupyter.docker_resources import dev_jupyter_lab
from workspace.settings import ws_settings

#
# -*- Dev Docker resources
#

# -*- Dev Api Image
dev_api_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}",
    tag=ws_settings.dev_env,
    enabled=(ws_settings.build_images and ws_settings.dev_api_enabled),
    path=str(ws_settings.ws_root),
    # platform="linux/amd64",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
    use_cache=ws_settings.use_cache,
)

# -*- Api Server running FastAPI on port 9090
dev_api_server = ApiServer(
    name=f"{ws_settings.ws_name}-api",
    enabled=ws_settings.dev_api_enabled,
    image=dev_api_image,
    mount_workspace=True,
    use_cache=ws_settings.use_cache,
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/api_secrets.yml"),
)

#
# -*- Define dev Docker resources using the DockerConfig
#
dev_docker_config = DockerConfig(
    env=ws_settings.dev_env,
    network=ws_settings.ws_name,
    apps=[dev_api_server, dev_jupyter_lab],
)
