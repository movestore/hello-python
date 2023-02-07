import os
import logging


class MoveAppsIo:
    @staticmethod
    def create_artifacts_file(artifact_file_name: str) -> str:
        app_artifacts_dir = os.environ.get('APP_ARTIFACTS_DIR', './resources/output')
        return os.path.join(app_artifacts_dir, artifact_file_name)

    @staticmethod
    def get_app_file_path(appspec_local_file_setting_id: str, fallback_to_provided_files: bool = True) -> str:
        if appspec_local_file_setting_id:
            local_app_files_root = os.environ.get('LOCAL_APP_FILES_DIR', './resources/local_app_files')
            user_upload_dir = os.path.join(
                local_app_files_root,
                os.environ.get('LOCAL_APP_FILES_UPLOADED_SUB_DIR', 'uploaded-app-files'),
                appspec_local_file_setting_id
            )
            if os.path.exists(user_upload_dir) and len(os.listdir(user_upload_dir)) > 0:
                # directory exists and is not empty: user provided some files
                logging.info(f'Detected app-files provided by user for \'{appspec_local_file_setting_id}\'.')
                return user_upload_dir
            elif fallback_to_provided_files:
                # fallback to directory provided by app developer
                provided_dir = os.path.join(
                    local_app_files_root,
                    os.environ.get('LOCAL_APP_FILES_PROVIDED_SUB_DIR', 'provided-app-files'),
                    appspec_local_file_setting_id
                )
                if os.path.exists(provided_dir) and len(os.listdir(provided_dir)) > 0:
                    logging.info(
                        f'Using fallback files provided by app developer for \'{appspec_local_file_setting_id}\'.'
                    )
                    return provided_dir
        logging.warning(f'No files present for app-files \'{appspec_local_file_setting_id}\': User did not '
                        f'upload anything and the app did not provide fallback files.')
