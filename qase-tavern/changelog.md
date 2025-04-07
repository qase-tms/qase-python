# qase-tavern 1.1.0

## What's new

- Updated core package to the latest supported versions.
- Improved logic for handling multiple QaseID values in test results.
- Removed `useV2` configuration option. The reporter now always uses API v2 for sending results.

# qase-tavern 1.0.3

## What's new

- Logging of host system details to improve debugging and traceability.  
- Output of installed packages in logs for better environment visibility.  

# qase-tavern 1.0.2

## What's new

Added support for specifying multiple test case IDs for a single automated test, improving test case association and
traceability.

```yaml
test_name: QaseID=2,3,4 Test with QaseID
stages:
  - name: Step 1
...
```

# qase-tavern 1.0.0

## What's new

The first release in the 1.0.x series of the Tavern reporter.
