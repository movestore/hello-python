import os


class MoveAppsIo:
    @staticmethod
    def create_artifacts_file(artifact_file_name: str) -> str:
        dir = os.environ.get('APP_ARTIFACTS_DIR', './resources/output')
        return f'{dir}/{artifact_file_name}'
