import subprocess
import os
from wson import parse_wson, WSONParseError

class PipiyError(Exception):
    pass

def init_project():
    default_wson_content = """
    {
        module = [
            "numpy = \"1.24.0\"",
            "discord.py = \"2.2.2\""
        ]
    }
    """

    with open("pypackage.ws", "w") as f:
        f.write(default_wson_content.strip())

    print("Initialized pipiy project with default pypackage.ws.")

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

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pipiy - WSON package manager')
    subparsers = parser.add_subparsers(dest='command')

    # init 명령어 추가
    init_parser = subparsers.add_parser('init', help='Initialize a new pipiy project.')

    # install 명령어 추가
    install_parser = subparsers.add_parser('install', help='Install modules from a WSON file or a specific module.')
    install_parser.add_argument('module_name', nargs='?', help='Name of the module to install.')
    install_parser.add_argument('file', nargs='?', default='pypackage.ws', help='WSON requirements file.')

    args = parser.parse_args()

    if args.command == 'init':
        init_project()
    elif args.command == 'install':
        if args.module_name:
            install_package(args.module_name, None)
        else:
            install_requirements(args.file)

if __name__ == "__main__":
    main()
