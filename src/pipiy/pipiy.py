import subprocess
import os
import argparse
from wson import parse_wson, WSONParseError

VERSION = "pipiy=0.2.5"

class PipiyError(Exception):
    pass

def init_project():
    default_wson_content = """
{
    module = [
    ]
}
""".strip()
    with open("pypackage.ws", "w") as f:
        f.write(default_wson_content)
    print("Initialized pipiy project with default pypackage.ws.")

def install_package(package_spec):
    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', package_spec])
        add_to_requirements(package_spec)
    except subprocess.CalledProcessError as e:
        raise PipiyError(f"Failed to install package {package_spec}. Error: {str(e)}")

def add_to_requirements(package_spec):
    try:
        requirements = read_wson_requirements("pypackage.ws")
        module_list = requirements.get('module', [])

        if '==' in package_spec:
            package_name, version = package_spec.split('==')
            entry = f'{package_name} = "{version}"'
        else:
            entry = package_spec

        if entry not in module_list:
            module_list.append(entry)

        with open("pypackage.ws", "w") as f:
            f.write("{\n    module = [\n")
            for item in module_list:
                f.write(f"        {item},\n")
            f.write("    ]\n}")

    except (WSONParseError, FileNotFoundError):
        raise PipiyError("Error updating requirements.")

def read_wson_requirements(file_path):
    with open(file_path, 'r') as file:
        wson_str = file.read()
    return parse_wson(wson_str)

def install_requirements(file_path):
    try:
        requirements = read_wson_requirements(file_path)
        for module in requirements.get('module', []):
            if ' = ' in module:
                package_name, version = module.split(' = ')
                version = version.strip('"')
                install_package(f"{package_name}=={version}")
            else:
                install_package(module.strip())
    except (WSONParseError, FileNotFoundError) as e:
        raise PipiyError(f"Error reading requirements: {str(e)}")

def show_version():
    print(VERSION)

def main():
    parser = argparse.ArgumentParser(description='Pipiy - WSON package manager')
    subparsers = parser.add_subparsers(dest='command')

    init_parser = subparsers.add_parser('init', help='Initialize a new pipiy project.')
    install_parser = subparsers.add_parser('install', help='Install modules from a WSON file or a specific module.')
    install_parser.add_argument('module_name', nargs='?', help='Name of the module to install.')
    install_parser.add_argument('file', nargs='?', default='pypackage.ws', help='WSON requirements file.')
    install_parser.add_argument('--pyproject', action='store_true', help='Install from pyproject.ws')
    version_parser = subparsers.add_parser('version', help='Show the version of pipiy.')

    args = parser.parse_args()

    if args.command == 'init':
        init_project()
    elif args.command == 'install':
        if args.pyproject:
            install_requirements('pyproject.ws')
        elif args.module_name:
            install_package(args.module_name)
        else:
            install_requirements(args.file)
    elif args.command == 'version':
        show_version()

if __name__ == "__main__":
    main()