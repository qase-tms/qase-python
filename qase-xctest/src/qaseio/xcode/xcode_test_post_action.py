import argparse
import os
import plistlib

from qaseio.xcode.qase_exporter import QaseExtractor


def find_report(project_folder):
    for i in range(3):
        project_folder, tail = os.path.split(project_folder)
        if tail == "Build":
            break

    test_folder = os.path.join(project_folder, "Logs/Test")
    manifest_file = os.path.join(test_folder, "LogStoreManifest.plist")

    with open(manifest_file, "rb") as fp:
        pl = plistlib.load(fp)

    time_start = 0.0
    for log_id, log in pl["logs"].items():
        if time_start < log["timeStartedRecording"]:
            time_start = log["timeStartedRecording"]
            last_log = log

    return os.path.join(test_folder, last_log["fileName"])


def main():
    parser = argparse.ArgumentParser(
        description="Xcode Post Action For Export Test Report"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--build", help="Build Root Folder. Use BUILD_ROOT env."
    )
    group.add_argument("--xcresults", help="Reports", nargs="+")

    parser.add_argument("--api_token", help="Qase API token", required=True)
    parser.add_argument(
        "--project_code", help="Qase Project Code", required=True
    )
    parser.add_argument(
        "--upload_attachments",
        action="store_true",
        help="Upload Attachments",
        default=False,
    )
    parser.add_argument("--run_name", help="Qase Test Run Name", default="Run")

    args = parser.parse_args()

    if args.build:
        report_file = find_report(args.build)
        reports = [report_file]
    else:
        reports = args.xcresults

    extractor = QaseExtractor(
        reports,
        args.api_token,
        args.project_code,
        args.upload_attachments,
        args.run_name,
    )
    extractor.process()
