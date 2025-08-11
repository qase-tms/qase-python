# Status Filtering for Test Results

This document describes the status filtering functionality that allows you to exclude test results with specific statuses from being sent to Qase TestOps.

## Overview

The status filter feature enables you to configure which test result statuses should be excluded from reporting. This is useful when you want to:

- Skip reporting of passed tests to reduce noise
- Exclude certain statuses from specific test runs
- Focus on specific types of test results (e.g., only failures and errors)

## Configuration

### Configuration File

You can configure status filtering in your `qase.config.json` file:

```json
{
  "testops": {
    "statusFilter": ["passed", "skipped"]
  }
}
```

### Environment Variables

You can also use environment variables:

```bash
export QASE_TESTOPS_STATUS_FILTER="passed,skipped"
```

### Command Line Options

For frameworks that support CLI options:

```bash
# Pytest
pytest --qase-testops-status-filter="passed,skipped"

# Tavern
pytest --qase-testops-status-filter="passed,skipped"
```

## Supported Statuses

The following statuses can be used in the filter:

- `passed` - Test passed successfully
- `failed` - Test failed
- `skipped` - Test was skipped
- `blocked` - Test was blocked
- `untested` - Test was not executed

## Examples

### Filter Out Passed Tests

```json
{
  "testops": {
    "statusFilter": ["passed"]
  }
}
```

This configuration will exclude all passed tests from being sent to Qase TestOps.

### Filter Out Multiple Statuses

```json
{
  "testops": {
    "statusFilter": ["passed", "skipped"]
  }
}
```

This configuration will exclude both passed and skipped tests.

### No Filtering

```json
{
  "testops": {
    "statusFilter": []
  }
}
```

Or simply omit the `statusFilter` field to disable filtering.

## Behavior

- **Filtering Logic**: Results with statuses listed in `statusFilter` are excluded from sending
- **Batch Processing**: Filtering is applied when results are sent in batches
- **Logging**: Filtered results are logged at debug level, and the count of filtered results is logged at info level
- **Performance**: Filtering occurs before sending, so no network requests are made for filtered results

## Use Cases

### CI/CD Pipelines

In continuous integration, you might want to only report failures and errors:

```json
{
  "testops": {
    "statusFilter": ["passed", "skipped"]
  }
}
```

### Development Testing

During development, you might want to see all results:

```json
{
  "testops": {
    "statusFilter": []
  }
}
```

### Production Monitoring

In production, you might want to focus on critical issues:

```json
{
  "testops": {
    "statusFilter": ["passed", "skipped", "blocked"]
  }
}
```

## Framework Support

Status filtering is supported across all Qase Python frameworks:

- **qase-pytest**: Via config file, environment variables, and CLI options
- **qase-behave**: Via config file, environment variables, and behave userdata
- **qase-robotframework**: Via config file and environment variables
- **qase-tavern**: Via config file, environment variables, and CLI options

## Notes

- Filtering is applied at the result level, not at the step level
- Results with `None` status are not filtered (they are always sent)
- The filter is case-sensitive and must match the exact status strings
- Empty or invalid filter configurations are treated as no filtering
