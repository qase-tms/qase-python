# Qase XCTest Utils

## How to install

`pip install qase-xctest`

## How to use

### For XCode

`--api_token YOUR_API_TOKEN` - Api token for qase api. Get api token [here](https://app.qase.io/user/api/token).

`--project_code YOUR_PROJECT_CODE` - You can find project code [here](https://app.qase.io/projects).

`--build $BUILD_ROOT` - Xcode build folder. Xcode setup `$BUILD_ROOT` enviroment automatically.
Always using this enviroment for `--build` arg.

`--run_name From_Xcode` - Arbitrary run name. You can detect your run result from all results.

`--upload_attachments` - Send attachments from report.

```bash
qasexcode --build $BUILD_ROOT \
  --api_token YOUR_API_TOKEN \
  --project_code YOUR_PROJECT_CODE \
  --run_name From_Xcode \
  --upload_attachments
```

### For CI

`--xcresults` - Paths to reports. If your reports will be contains one test result multiple times, enable settings `Allow to add results for cases in closed runs.` in your project.


```base
qasexcode --xcresults PathToReport/1.xcresult PathToReport/2.xcresult \
  --api_token YOUR_API_TOKEN \
  --project_code YOUR_PROJECT_CODE \
  --run_name From_ci \
  --upload_attachments
```
