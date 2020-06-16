import argparse
import os
import plistlib

from qaseio.xcode.qase_exporter import QaseExtractor


def main():
    parser = argparse.ArgumentParser(description='Xcode Post Action For Export Test Report')
    parser.add_argument('--build', help='Build Root Folder. Use BUILD_ROOT env.', required=True)
    parser.add_argument('--api_token',help='Qase API token', required=True)
    parser.add_argument('--project_code', help='Qase Project Code', required=True)
    parser.add_argument('--upload_attachments', action="store_true", help='Upload Attachments', default=False)
    parser.add_argument('--run_name', help='Qase Test Run Name', default="Run")

    args = parser.parse_args()

    project_folder = args.build

    for i in range(3):
        project_folder, tail = os.path.split(project_folder)
        if tail == "Build":
            break

    test_folder = os.path.join(project_folder, "Logs/Test")
    manifest_file = os.path.join(test_folder, "LogStoreManifest.plist")

    with open(manifest_file, 'rb') as fp:
        pl = plistlib.load(fp)

    time_start = 0.0
    for log_id, log in pl["logs"].items():
        if time_start < log["timeStartedRecording"]:
            time_start = log["timeStartedRecording"]
            last_log = log

    report_file = os.path.join(test_folder, last_log["fileName"])

    extractor = QaseExtractor(
        report_file,
        args.api_token,
        args.project_code,
        args.upload_attachments,
        args.run_name
    )
    extractor.process()


main()