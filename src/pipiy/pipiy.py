import subprocess
import os
from wson import parse_wson, WSONParseError

class PipiyError(Exception):
    pass

def init_project():
    default_wson_content = """{
        "module": {}
}
"""

    with open("pypackage.ws", "w") as f:
        f.write(default_wson_content.strip())

    print("Initialized pipiy project with default pypackage.ws.")

def install_package(package_name, version):
    package_with_version = f"{package_name}=={version}" if version else package_name
    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', package_with_version])
        # WSON 파일에 패키지 추가
        add_package_to_wson(package_name, version)
    except subprocess.CalledProcessError as e:
        raise PipiyError(f"Failed to install package {package_with_version}. Error: {str(e)}")

def add_package_to_wson(package_name, version):
    # 현재 WSON 파일 읽기
    try:
        requirements = read_wson_requirements("pypackage.ws")
    except WSONParseError:
        requirements = {"module": {}}

    # 모듈 추가
    if "module" not in requirements:
        requirements["module"] = {}

    # 모듈 이름과 버전 추가
    requirements["module"][package_name] = version

    # 업데이트된 WSON 파일 작성
    with open("pypackage.ws", 'w') as file:
        file.write(str(requirements))

def read_wson_requirements(file_path):
    with open(file_path, 'r') as file:
        wson_str = file.read()
    return parse_wson(wson_str)

def install_requirements(file_path):
    try:
        requirements = read_wson_requirements(file_path)
        for module in requirements.get('module', {}).items():
            package_name, version = module
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
    install_parser.add_argument('version', nargs='?', help='Version of the module to install.')
    install_parser.add_argument('file', nargs='?', default='pypackage.ws', help='WSON requirements file.')

    args = parser.parse_args()

    if args.command == 'init':
        init_project()
    elif args.command == 'install':
        if args.module_name:
            install_package(args.module_name, args.version)
        else:
            install_requirements(args.file)

if __name__ == "__main__":
    main()
