# qase-python-commons@3.1.9

## What's new

Added configuration for Playwright framework. You can specify the `video`, `trace` and `output` options.

# qase-python-commons@3.1.7

## What's new

Fixed an issue with the `upload_attachment` method:

```log
"attachments": [attach.hash for attach in attached],
AttributeError: 'list' object has no attribute 'hash'
```

# qase-python-commons@3.1.7

## What's new

Show a test run link in end of log.

# qase-python-commons@3.1.6

## What's new

Change logic for uploading attachments. Now, the `upload_attachment` method won't return an error if the file is not
found.

# qase-python-commons@3.1.5

## What's new

Support `author` field in the test case model.
You can specify author name or email in fields.

# qase-python-commons@3.1.4

## What's new

- Add `clear` method to set the runtime to the base state.
- Make the `network` profiler thread safe.

# qase-python-commons@3.1.3

## What's new

Fix an issue with logging. The logger didn't write logs to the file if the OS used special encoding.

# qase-python-commons@3.1.2

## What's new

Support `suite` field in the test case model.

# qase-python-commons@3.1.0

## What's new

Minor release that includes all changes from beta versions 3.1.0b*.
Also added support for group parameters.

# qase-python-commons@3.1.0b7

## What's new

Fixed the following issue:

```log
HTTPSConnectionPool(host='api.qase.io', port=443): Max retries exceeded with url: /v1/plan/DEMO/1 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)')))
```

# qase-python-commons@3.1.0b6

## What's new

Reporters didn't send information about fields, like `title`, `description`, etc, to the Qase.
Now, the reporters will send all the information about the test case to the Qase.

# qase-python-commons@3.1.0b4

## What's new

Show a link to the test result in the Qase when the test has failed.

# qase-python-commons@3.1.0b3

## What's new

Fixed the problem [#176] with bool parameters. The config manager didn't get values in uppercase.

# qase-python-commons@3.1.0b2

## What's new

Fixed the following issues:

```log
AttributeError: 'QaseConfig' object has no attribute 'validate_config'
```

```log
'Run' object has no attribute 'to_json'
```

# qase-python-commons@3.1.0b1

## What's new

1. Change config type from `dict` to `object`
    - Add new config models.
    - Update retrieving data from the config in all dependencies.

2. Add a new configuration option `rootSuite` to specify a root suite.
   This option is available in the config file and the `QASE_ROOT_SUITE` env variable.

# qase-python-commons@3.0.3

## What's new

Fix an issue with getting bool parameters from the config when the parameter's value is `False`

# qase-python-commons@3.0.2

## What's new

First release in the 3.0.x series of the commons package.

# qase-python-commons@3.0.2b9

## What's new

Fixed an issue causing "Errno 22" error on Windows:

```log
[Errno 22] Invalid argument: .\\logs\\_20240101_00:00:00
```

# qase-python-commons@3.0.2b8

## What's new

Fixed the following issues:

- Return a correct default value from the config if the value was not found.
- Mark the `Field` model as exported.
- Fix the problem where the test run is completed before the results are sent.

# qase-python-commons@3.0.2b7

## What's new

Fixed the following issue:

```log
Creating instance failed: OSError: [ Errno 22 ] Invalid argument: './logs\file.log'
```

# qase-python-commons@3.0.2b6

## What's new

Fixed the following issue:

```log
[ ERROR ] Taking listener 'qaseio.robotframework.Listener' into use failed: 
    Importing listener 'qaseio.robotframework.Listener' failed: 
       ModuleNotFoundError: No module named 'pkg_resources'
```

# qase-python-commons@3.0.2b5

## What's new

A number of improvements in the network profiler:

- Ignoring requests to `qase.io` host.
- Checking that attributes `body` and `headers` are in the request.
- Fixed ignoring response for the `urllib3` package.
- Added a creation step for redirected requests

# qase-python-commons@3.0.2b4

## What's new

The sleep profiler was turned off until the test data collection was completed.
Now the profilers will turn off after the test is completed.

# qase-python-commons@3.0.2b3

## What's new

Added support for API V2. Specify the `useV2` option in the config file or the environment variable `QASE_TESTOPS_USEV2`

# qase-python-commons@3.0.2b2

## What's new

Migrate from old `qaseio` client to new `qase-api-clinet` client.  
