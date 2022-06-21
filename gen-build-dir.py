import os
import argparse
import urllib.request
import tarfile
import configparser
from zipfile import ZipFile
import shutil


def make_project_dirs(operatingSystem: str, architecture: str) -> None:
    template_dir = os.path.join(f"{operatingSystem}-{architecture}-javalang")
    src_dir = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src')
    if os.path.exists(template_dir):
        if os.path.exists(src_dir):
            print(f"{template_dir} and {src_dir} exist, skipping creation")
        else:
            print(f"Making directory {src_dir}")
            os.mkdir(src_dir)
    else:
        print(f"Making directory {template_dir}")
        os.mkdir(template_dir)
        print(f"Making directory {src_dir}")
        os.mkdir(src_dir)


def copy_templates(operatingSystem: str, architecture: str, javaVersion: str) -> None:
    init_destination = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'javalang', '__init__.py')
    pyproject_destination = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'pyproject.toml')
    manifest_destination = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'MANIFEST.in')
    print(f"Copying pyproject.template.toml to {pyproject_destination}")
    shutil.copy("pyproject.template.toml", pyproject_destination)
    match operatingSystem:
        case 'mac':
            print(f"Copying init_template_macos.py to {init_destination}")
            shutil.copy("init_template_macos.py", init_destination)
            print(f"Copying manifest-template-macos.in to {manifest_destination}")
            shutil.copy("manifest-template-macos.in", manifest_destination)
        case _:
            print(f"Copying init_template_macos.py to {init_destination}")
            shutil.copy("init_template.py", init_destination)
            print(f"Copying manifest-template-macos.in to {manifest_destination}")
            shutil.copy("manifest-template.in", manifest_destination)
    config = configparser.ConfigParser()
    config.read(pyproject_destination)
    config['project']['version'] = f'"{javaVersion}"'
    with open(pyproject_destination, 'w') as configfile:
        print(f"Setting {javaVersion} as package version in {pyproject_destination}")
        config.write(configfile)

def get_JDK_release(operatingSystem: str, architecture: str, java_version: str, jre_or_jdk: bool) -> None:
    match java_version:
        case '17.0.3+7':
            github_url = 'https://github.com/adoptium/temurin17-binaries'
            open_jdk_slug = 'OpenJDK17U'
            open_jdk_ver_slug = '17.0.3_7'
        case '18.0.1+10':
            github_url = 'https://github.com/adoptium/temurin18-binaries'
            open_jdk_slug = 'OpenJDK18U'
            open_jdk_ver_slug = '18.0.1_10'
        case _:
            print(
                "Unsupported version of java, supported versions are 17.0.3+7 and 18.0.1+10")
            exit(1)
    if jre_or_jdk:
        open_jdk_edition = 'jre'
        jdk_extract_dir = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', f'jdk-{java_version}-jre')
    else:
        open_jdk_edition = 'jdk'
        jdk_extract_dir = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', f'jdk-{java_version}')
    src_dir = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src')
    javalang_dir = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'javalang')
    match operatingSystem:
        case "windows":
            java_url = f'{github_url}/releases/download/jdk-{java_version}/{open_jdk_slug}-{open_jdk_edition}_{architecture}_{operatingSystem}_hotspot_{open_jdk_ver_slug}.zip'
            win_zip_location = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.zip')
            if os.path.exists(win_zip_location):
                if jre_or_jdk:
                    print("JRE already downloaded, skipping download step")
                else:
                    print("JDK already downloaded, skipping download step")
            else:
                if jre_or_jdk:
                    print(f"Downloading JRE to {win_zip_location}")
                else:
                    print(f"Downloading JRE to {win_zip_location}")
                urllib.request.urlretrieve(java_url, win_zip_location)
                with ZipFile(win_zip_location, 'r') as zip_ref:
                    print(f"Extracting {win_zip_location} to {jdk_extract_dir}")
                    zip_ref.extractall(src_dir)
                print(f"Deleting {win_zip_location}")
                os.remove(win_zip_location)
                print(f"Renaming {jdk_extract_dir} to {javalang_dir}")
                os.rename(jdk_extract_dir, javalang_dir)
        case _:
            java_url = f'{github_url}/releases/download/jdk-{java_version}/{open_jdk_slug}-{open_jdk_edition}_{architecture}_{operatingSystem}_hotspot_{open_jdk_ver_slug}.tar.gz'
            tar_gz_location = os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.tar.gz')
            if os.path.exists(tar_gz_location):
                if jre_or_jdk:
                    print("JRE already downloaded, skipping download step")
                else:
                    print("JDK already downloaded, skipping download step")
            else:
                if jre_or_jdk:
                    print(f"Downloading JRE to {tar_gz_location}")
                else:
                    print(f"Downloading JDK to {tar_gz_location}")
                urllib.request.urlretrieve(java_url, tar_gz_location)
                print("Download Finished")
                with tarfile.open(tar_gz_location, 'r') as jdk_tar:
                    print(f"Extracting {tar_gz_location} to {jdk_extract_dir}")
                    jdk_tar.extractall(src_dir)
                print(f"Deleting {tar_gz_location}")
                os.remove(tar_gz_location)
                print(f"Renaming {jdk_extract_dir} to {javalang_dir}")
                os.rename(jdk_extract_dir, javalang_dir)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Toggle switch ports for link testing.")
    parser.add_argument("-o", "--operating-system", metavar='os',
                        type=str, help='Specify an operating system')
    parser.add_argument("-a", "--architecture", metavar='architecture',
                        type=str, help='Specify an architecture')
    parser.add_argument("-j", "--java-version", metavar='java_ver',
                        type=str, help='Specify a version of java (17.0.3+7 or 18.0.1+10)', default='17.0.3+7')
    parser.add_argument("-r", "--jre", action='store_true', help="Specify you want the JRE instead of the JDK")
    
    args = parser.parse_args()

    make_project_dirs(args.operating_system, args.architecture)
    get_JDK_release(args.operating_system, args.architecture, args.java_version, args.jre)
    copy_templates(args.operating_system, args.architecture, args.java_version)

main()