import subprocess
import os
from wson import parse_wson, WSONParseError

class PipiyError(Exception):
    pass

def install_package(package_name, version):
    package_with_version = f"{package_name}=={version}" if version else package_name
    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', package_with_version])
    except subprocess.CalledProcessError as e:
        raise PipiyError(f"Failed to install package {package_with_version}. Error: {str(e)}")

def read_wson_requirements(file_path):
    with open(file_path, 'r') as file:
        wson_str = file.read()
    return parse_wson(wson_str)

def install_requirements(file_path):
    try:
        requirements = read_wson_requirements(file_path)
        for module in requirements.get('module', {}):
            package_name, version = list(module.items())[0]
            install_package(package_name, version)
    except (WSONParseError, FileNotFoundError) as e:
        raise PipiyError(f"Error reading requirements: {str(e)}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install packages from a WSON requirements file.')
    parser.add_argument('file', type=str, help='Path to the WSON requirements file.')

    args = parser.parse_args()
    install_requirements(args.file)
