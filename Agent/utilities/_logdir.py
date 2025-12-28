
import os
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn

def get_artifacts_folder_name() -> str:
    """Returns name of the folder where Robot logs/reports are generated."""
    variables = BuiltIn().get_variables()
    robot_output_dir = str(variables['${OUTPUTDIR}'])
    exec_dir = str(variables['${EXECDIR}'])

    if 'pabot_results' in robot_output_dir:
        robot_output_dir = robot_output_dir.split('pabot_results')[0]

    relative_path = str(robot_output_dir).replace(str(exec_dir), '').strip('/')
    output_folder = relative_path.split('/')[0]
    return output_folder

def get_artifacts_root_path() -> Path:
    """Full path to artifacts root dir. Example: /path/to/results"""
    variables = BuiltIn().get_variables()
    exec_dir = str(variables['${EXECDIR}'])
    artifacts_folder = get_artifacts_folder_name()
    return Path(exec_dir) / artifacts_folder

def set_artifacts_subdir(ArtifactsName) -> Path:
    """Returns full path to a subdir in artifacts root (creates if missing)."""
    artifacts_dir = get_artifacts_root_path() / ArtifactsName
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return artifacts_dir

