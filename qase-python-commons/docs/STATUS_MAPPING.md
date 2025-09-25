# Status Mapping for Test Results

This document describes the status mapping functionality that allows you to transform test result statuses from one value to another based on configuration. This is useful for standardizing status values across different testing frameworks or for custom status transformations.

## Overview

The status mapping feature enables you to configure which test result statuses should be transformed before being sent to Qase TestOps. This is useful when you want to:

- Map framework-specific statuses to standard Qase statuses
- Transform statuses based on business requirements
- Standardize status values across different testing tools
- Handle legacy status values

## Configuration

### Configuration File

You can configure status mapping in your `qase.config.json` file:

```json
{
  "statusMapping": {
    "invalid": "failed",
    "skipped": "passed"
  }
}
```

### Environment Variables

You can also use environment variables:

```bash
export QASE_STATUS_MAPPING="invalid=failed,skipped=passed"
```

### Command Line Options

For frameworks that support CLI options, you can use the CLI parameter:

```bash
# Pytest
pytest --qase-status-mapping="invalid=failed,skipped=passed"

# Tavern
pytest --qase-status-mapping="invalid=failed,skipped=passed"

# Behave
behave --define qase-status-mapping="invalid=failed,skipped=passed"
```

You can also use environment variables:

```bash
# Pytest
QASE_STATUS_MAPPING="invalid=failed,skipped=passed" pytest

# Tavern
QASE_STATUS_MAPPING="invalid=failed,skipped=passed" pytest

# Behave
QASE_STATUS_MAPPING="invalid=failed,skipped=passed" behave

# Robot Framework
QASE_STATUS_MAPPING="invalid=failed,skipped=passed" robot tests/
```

## Supported Statuses

The following statuses can be used in the mapping:

- `passed` - Test passed successfully
- `failed` - Test failed
- `skipped` - Test was skipped
- `blocked` - Test was blocked
- `invalid` - Test failed due to non-assertion errors (network issues, syntax errors)

## Examples

### Map Invalid Tests to Failed

```json
{
  "statusMapping": {
    "invalid": "failed"
  }
}
```

This configuration will map all tests with `invalid` status to `failed` status.

### Map Skipped Tests to Passed

```json
{
  "statusMapping": {
    "skipped": "passed"
  }
}
```

This configuration will map all tests with `skipped` status to `passed` status.

### Multiple Mappings

```json
{
  "statusMapping": {
    "invalid": "failed",
    "skipped": "passed"
  }
}
```

This configuration applies multiple status mappings.

### Environment Variable Example

```bash
export QASE_STATUS_MAPPING="invalid=failed,skipped=passed"
```

## Behavior

- **Mapping Logic**: Status mapping is applied **before** status filtering
- **Centralized Application**: Mapping is applied in the core reporter for all frameworks
- **Logging**: Status changes are logged at debug level
- **Validation**: Invalid mappings are ignored with warnings
- **Case Sensitivity**: Status mapping is case-sensitive
- **No Chaining**: Only direct mappings are applied (no chaining of mappings)

## Integration with Status Filtering

Status mapping is applied **before** status filtering. This means:

1. Original status → Mapped status (via status mapping)
2. Mapped status → Filtered out or sent (via status filter)

Example:
```json
{
  "statusMapping": {
    "invalid": "failed"
  },
  "testops": {
    "statusFilter": ["passed"]
  }
}
```

In this case:
- Tests with `invalid` status are mapped to `failed`
- Tests with `failed` status are **not** filtered out (only `passed` tests are filtered)
- Tests with `invalid` status will be sent as `failed` status

## Framework-Specific Examples

### Pytest

```json
{
  "statusMapping": {
    "invalid": "failed"
  },
  "testops": {
    "project": "MYPROJECT",
    "api": {
      "token": "your-token"
    }
  }
}
```

### Behave

```json
{
  "statusMapping": {
    "skipped": "passed"
  },
  "testops": {
    "project": "MYPROJECT",
    "api": {
      "token": "your-token"
    }
  }
}
```

### Robot Framework

```json
{
  "statusMapping": {
    "disabled": "skipped"
  },
  "testops": {
    "project": "MYPROJECT",
    "api": {
      "token": "your-token"
    }
  }
}
```

### Tavern

```json
{
  "statusMapping": {
    "invalid": "failed",
    "skipped": "passed"
  },
  "testops": {
    "project": "MYPROJECT",
    "api": {
      "token": "your-token"
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Status not being mapped**: Check that the source status exactly matches the configured mapping key (case-sensitive)

2. **Invalid status error**: Ensure both source and target statuses are from the valid list: `passed`, `failed`, `skipped`, `disabled`, `blocked`, `invalid`

3. **Environment variable not working**: Make sure the environment variable is set before running the tests

4. **Mapping not applied**: Check that the status mapping is configured at the top level of the configuration, not inside `testops` or `report` sections

### Debug Logging

Enable debug logging to see status mapping in action:

```json
{
  "debug": true,
  "statusMapping": {
    "invalid": "failed"
  }
}
```

This will log messages like:
```
Status mapped for 'Test Name': invalid -> failed
```

### Validation

The status mapping configuration is validated when the reporter is initialized. Invalid mappings will cause warnings but will not prevent the reporter from working.

## Migration Guide

### From Status Filtering

If you were previously using status filtering to exclude certain statuses, you can now use status mapping to transform them instead:

**Before (filtering out invalid tests):**
```json
{
  "testops": {
    "statusFilter": ["invalid"]
  }
}
```

**After (mapping invalid to failed):**
```json
{
  "statusMapping": {
    "invalid": "failed"
  }
}
```

This approach is better because:
- Tests are still reported (not excluded)
- You can see the original status in logs
- More flexible for different reporting needs

## Best Practices

1. **Use descriptive mappings**: Choose target statuses that clearly indicate the transformation
2. **Document your mappings**: Keep a record of why certain mappings are needed
3. **Test your configuration**: Verify that mappings work as expected in your environment
4. **Consider framework differences**: Different testing frameworks may have different status semantics
5. **Use environment variables for CI/CD**: Set mappings via environment variables in your CI/CD pipeline

## API Reference

### StatusMapping Class

The `StatusMapping` class provides the core functionality for status mapping:

```python
from qase.commons.utils.status_mapping import StatusMapping

# Create from dictionary
mapping = StatusMapping.from_dict({"invalid": "failed"})

# Create from environment string
mapping = StatusMapping.from_env_string("invalid=failed,skipped=passed")

# Apply mapping
result_status = mapping.apply_mapping("invalid")  # Returns "failed"
```

### Configuration Methods

```python
from qase.commons.models.config.qaseconfig import QaseConfig

config = QaseConfig()
config.set_status_mapping({"invalid": "failed"})
```
