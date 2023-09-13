from modules.util import calculate_directory_hash
import pulumi
from pulumi_aws import ecr
import pulumi_docker as docker
from pulumi import StackReference
from modules.config import AppConfig

def build_and_push_ecr_image(config: AppConfig) -> any:
    ecr_repository = ecr.Repository(config.app_name, name=config.app_name)
    auth_token = ecr.get_authorization_token()

    new_tag_output = pulumi.Output.from_input(calculate_directory_hash(config.docker_config.app_src_path).hexdigest())
    previous_tag_key = "previousImageTag"
    previous_tag_output = StackReference(config.stack_name).get_output(previous_tag_key).apply(lambda tag: tag)

    image = docker.Image(
        config.app_name,
        build=docker.DockerBuildArgs(
            context=config.docker_config.docker_build_context,
            platform="linux/x86_64",
        ),
        image_name=pulumi.Output.all(ecr_repository.repository_url, new_tag_output).apply(
            lambda args: f"{args[0]}:{args[1]}"
        ),
        registry=docker.RegistryArgs(
            username=pulumi.Output.secret(auth_token.user_name),
            password=pulumi.Output.secret(auth_token.password),
            server=ecr_repository.repository_url,
        ),
    )
    pulumi.export(previous_tag_key, new_tag_output)
    return image
