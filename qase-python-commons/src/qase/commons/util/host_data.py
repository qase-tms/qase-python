import os
import platform
import subprocess
import json
import re
import sys
from typing import Optional, Dict

HostData = Dict[str, str]


def exec_command(command: str, default_value: str = "") -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error executing command '{command}': {e}", file=sys.stderr)
        return default_value


def get_detailed_os_info() -> str:
    system = platform.system().lower()
    try:
        if system == "windows":
            return exec_command("ver")
        elif system == "darwin":
            return exec_command("sw_vers -productVersion")
        else:
            try:
                if os.path.exists("/etc/os-release"):
                    with open("/etc/os-release", "r") as f:
                        os_release = f.read()
                    match = re.search(r'PRETTY_NAME="(.+?)"', os_release)
                    if match:
                        return match.group(1)
            except Exception:
                pass
            return platform.release()
    except Exception as e:
        print(f"Error getting detailed OS info: {e}", file=sys.stderr)
        return platform.release()


def get_package_version(package_name: Optional[str]) -> Optional[str]:
    if not package_name:
        return ""
    try:
        pip_output = exec_command(f"pip show {package_name}")
        if pip_output:
            version_match = re.search(r'Version:\s*(\S+)', pip_output)
            if version_match:
                return version_match.group(1)
        pip_list_output = exec_command("pip list --format=json")
        if pip_list_output:
            packages = json.loads(pip_list_output)
            for pkg in packages:
                if pkg.get("name", "").lower() == package_name.lower():
                    return pkg.get("version")
        try:
            import importlib.metadata
            return importlib.metadata.version(package_name)
        except (ImportError, importlib.metadata.PackageNotFoundError):
            pass
        return ""
    except Exception as e:
        print(f"Error getting version for package {package_name}: {e}", file=sys.stderr)
        return ""


def find_package_in_requirements(package_name: Optional[str]) -> Optional[str]:
    if not package_name:
        return ""
    try:
        possible_req_files = ['requirements.txt', 'requirements/base.txt', 'requirements/dev.txt']
        for req_file in possible_req_files:
            if os.path.exists(req_file):
                with open(req_file, 'r') as f:
                    for line in f:
                        if line.startswith(package_name):
                            version_match = re.search(r'[=<>~]{1,2}([\d.]+)', line)
                            if version_match:
                                return version_match.group(1)
        return ""
    except Exception as e:
        print(f"Error reading requirements for {package_name}: {e}", file=sys.stderr)
        return ""


def get_host_info(framework: Optional[str], reporter_name: Optional[str]) -> HostData:
    try:
        python_version = platform.python_version()
        pip_version = exec_command("pip --version")
        if pip_version:
            pip_match = re.search(r'pip\s+(\S+)', pip_version)
            pip_version = pip_match.group(1) if pip_match else ""
        framework_version = get_package_version(framework) or find_package_in_requirements(framework) or ""
        reporter_version = get_package_version(reporter_name) or find_package_in_requirements(reporter_name) or ""
        commons_version = get_package_version("qase-python-commons") or find_package_in_requirements(
            "qase-python-commons") or ""
        api_client_version_1 = get_package_version("qase-api-client") or find_package_in_requirements(
            "qase-api-client") or ""
        api_client_version_2 = get_package_version("qase-api-v2-client") or find_package_in_requirements(
            "qase-api-v2-client") or ""
        return {
            "system": platform.system().lower(),
            "machineName": platform.node(),
            "release": platform.release(),
            "version": get_detailed_os_info(),
            "arch": platform.machine(),
            "python": python_version,
            "pip": pip_version,
            "framework": framework_version,
            "reporter": reporter_version,
            "commons": commons_version,
            "apiClientV1": api_client_version_1,
            "apiClientV2": api_client_version_2
        }
    except Exception as e:
        print(f"Error getting host info: {e}", file=sys.stderr)
        return {
            "system": platform.system().lower(),
            "machineName": platform.node(),
            "release": platform.release(),
            "version": "",
            "arch": platform.machine(),
            "python": "",
            "pip": "",
            "framework": "",
            "reporter": "",
            "commons": "",
            "apiClientV1": "",
            "apiClientV2": ""
        }
