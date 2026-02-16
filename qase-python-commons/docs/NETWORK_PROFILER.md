# Network Profiler

## Overview

The Network Profiler automatically tracks and logs all HTTP requests during test execution. It captures request method, URL, headers, body, and response status, then sends this data as steps to Qase TestOps for detailed analysis and debugging.

## Supported Libraries

The profiler supports the following HTTP libraries:

- **requests** — Via `requests.Session.send`
- **urllib3** — Via `urllib3.PoolManager.request`

## Configuration

### Enable Network Profiler

Add `"network"` to the `profilers` array in your `qase.config.json`:

```json
{
  "profilers": ["network"]
}
```

Or via environment variable:

```bash
export QASE_PROFILERS="network"
```

### Exclude Hosts

By default, the Qase API host is always excluded from tracking. You can exclude additional hosts using the `excludeHosts` option or the `QASE_PROFILER_NETWORK_EXCLUDE_HOSTS` environment variable.

Hosts are matched using substring matching — if any excluded host string is found within the request URL, the request will be skipped.

#### Config file

Use the object format in the `profilers` array:

```json
{
  "profilers": [
    {
      "name": "network",
      "excludeHosts": ["telemetry.local", "monitoring.internal"]
    }
  ]
}
```

#### Environment variable

```bash
export QASE_PROFILER_NETWORK_EXCLUDE_HOSTS="telemetry.local,monitoring.internal"
```

#### Combining both

The environment variable and config file values are independent — the environment variable sets the exclude list directly (it does not merge with the config file). The Qase API host (`testops.api.host`) is always excluded automatically regardless of this setting.

### Multiple Profilers

You can enable multiple profilers simultaneously, mixing string and object formats:

```json
{
  "profilers": [
    {
      "name": "network",
      "excludeHosts": ["telemetry.local"]
    },
    "db",
    "sleep"
  ]
}
```

## Collected Data

For each HTTP request, the profiler collects the following information:

### Request Information

- **method** — HTTP method (GET, POST, PUT, DELETE, etc.)
- **url** — Full request URL
- **body** — Request body (when available)
- **headers** — Request headers (when available)

### Response Information

- **status_code** — HTTP response status code
- **response_body** — Response body (only for failed requests with status >= 400)
- **response_headers** — Response headers (only for failed requests with status >= 400)

## Data Format in Qase TestOps

When sent to Qase TestOps, HTTP requests appear as test steps with:

- **Step type**: `request`
- **Status**: `passed` for status < 400, `failed` for status >= 400

## Automatic Integration

The network profiler works automatically once enabled in the configuration. No additional code changes are required — it intercepts HTTP operations transparently using monkey patching.

## Notes

- The Qase API host is always excluded from tracking to avoid recursive logging
- The profiler only tracks operations that occur after it's enabled
- Failed responses (status >= 400) include response body and headers for debugging
- The profiler handles errors gracefully and won't break your HTTP operations
