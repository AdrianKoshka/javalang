import os
import argparse
import urllib.request
import tarfile
import configparser
from zipfile import ZipFile
import shutil


def make_project_dirs(operatingSystem: str, architecture: str):
    if os.path.exists(f"{operatingSystem}-{architecture}-javalang"):
        if os.path.exists(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src')):
            pass
        else:
            os.mkdir(os.path.join(f"{operatingSystem}-{architecture}-javalang", "src"))
    else:
        os.mkdir(f"{operatingSystem}-{architecture}-javalang")
        os.mkdir(os.path.join(f"{operatingSystem}-{architecture}-javalang", "src"))


def copy_templates(operatingSystem: str, architecture: str, javaVersion: str):
    shutil.copy("pyproject.template.toml",
                os.path.join(f'{operatingSystem}-{architecture}-javalang', 'pyproject.toml'))
    if operatingSystem == "linux" or "windows":
        shutil.copy("init_template.py",
                    os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'javalang', '__init__.py'))
        shutil.copy("manifest-template.in",
                    os.path.join(f'{operatingSystem}-{architecture}-javalang', 'MANIFEST.in'))
    elif operatingSystem == "mac":
        shutil.copy("init_template_macos.py",
                    os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'javalang', '__init__.py'))
        shutil.copy("manifest-template-macos.in",
                    os.path.join(f'{operatingSystem}-{architecture}-javalang', 'MANIFEST.in'))
    config = configparser.ConfigParser()
    config.read(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'pyproject.toml'))
    config['project']['version'] = f'"{javaVersion}"'
    with open(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'pyproject.toml'), 'w') as configfile:
        config.write(configfile)

def get_JDK_release(operatingSystem: str, architecture: str, javaVersion: str):
    if operatingSystem == 'windows':
        java_url = f'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-{javaVersion}/OpenJDK17U-jdk_{architecture}_{operatingSystem}_hotspot_17.0.3_7.zip'
        if os.path.exists(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.zip')):
            pass
        else:
            urllib.request.urlretrieve(java_url, os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.zip'))
            with ZipFile(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.zip'), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src'))
            os.remove(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.zip'))
            os.rename(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', f'jdk-{javaVersion}'),
                      os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'javalang'))
            
    else:
        java_url = f'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-{javaVersion}/OpenJDK17U-jdk_{architecture}_{operatingSystem}_hotspot_17.0.3_7.tar.gz'
        if os.path.exists(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.tar.gz')):
            pass
        else:
            urllib.request.urlretrieve(java_url, os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.tar.gz'))
            jdk_tar = tarfile.open(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.tar.gz'))
            jdk_tar.extractall(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src'))
            jdk_tar.close()
            os.remove(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'jdk.tar.gz'))
            os.rename(os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', f'jdk-{javaVersion}'),
                        os.path.join(f'{operatingSystem}-{architecture}-javalang', 'src', 'javalang'))

def main():
    parser = argparse.ArgumentParser(
        description="Toggle switch ports for link testing.")
    parser.add_argument("-o", "--operating-system", metavar='os',
                        type=str, help='Specify an operating system')
    parser.add_argument("-a", "--architecture", metavar='architecture',
                        type=str, help='Specify an architecture')
    parser.add_argument("-j", "--java-version", metavar='java_ver',
                        type=str, help='Specify a version of java', default='17.0.3+7')
    
    args = parser.parse_args()

    make_project_dirs(args.operating_system, args.architecture)
    get_JDK_release(args.operating_system, args.architecture, args.java_version)
    copy_templates(args.operating_system, args.architecture, args.java_version)

main()