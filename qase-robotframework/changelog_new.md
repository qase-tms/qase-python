# qase-robotframework 3.4.5

## What's new

- Improved test failure status handling
- Enhanced error classification to distinguish assertion errors from other failures
- Assertion errors (containing keywords like 'assert', 'AssertionError', 'expect', 'should', 'must', 'equal', 'not equal') now map to `failed` status
- Non-assertion errors (setup failures, exceptions, etc.) now map to `invalid` status
- Updated dependency on qase-python-commons to version 3.5.5

## Migration Guide

The listener now provides more accurate test result reporting by distinguishing between:
- `failed`: Test failed due to assertion error (test logic issue)
- `invalid`: Test failed due to non-assertion error (infrastructure/setup issue)

This change provides better insights into test failures and helps identify whether issues are related to test logic or infrastructure problems.

