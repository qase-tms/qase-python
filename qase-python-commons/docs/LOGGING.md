# Qase Python Logging Configuration

## Overview

The Qase Python logging system allows you to control how log messages are displayed and stored across all Qase Python reporters (pytest, behave, robotframework, tavern). You can independently control console output and file output.

## Configuration Options

### Console Output

Controls whether log messages appear in the terminal/console.

- **Default**: `true` (enabled)
- **Values**: `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`

### File Output

Controls whether log messages are written to log files.

- **Default**: `false` (disabled), `true` when `debug=true`
- **Values**: `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`

## Configuration Methods

### 1. Configuration File (`qase.config.json`)

```json
{
  "logging": {
    "console": true,
    "file": false
  }
}
```

### 2. Environment Variables

```bash
export QASE_LOGGING_CONSOLE=false
export QASE_LOGGING_FILE=true
export QASE_DEBUG=true  # Legacy option
```

### 3. Command Line Options

#### pytest

```bash
pytest --qase-logging-console=false --qase-logging-file=true
```

#### behave

```bash
behave --define qase-logging-console=false --define qase-logging-file=true
```

#### tavern

```bash
pytest --qase-logging-console=false --qase-logging-file=true
```

#### robotframework

```bash
# Only environment variables supported
QASE_LOGGING_CONSOLE=false QASE_LOGGING_FILE=true robot --listener qase.robotframework.Listener
```

## Configuration Priority

Settings are applied in this order (later overrides earlier):

1. **Default values**
2. **Configuration file** (`qase.config.json`)
3. **Environment variables**
4. **Command line options**

## Log Files

- **Directory**: `./logs/` (relative to your project)
- **File naming**: `_YYYYMMDD.log` (e.g., `_20241001.log`)
- **Format**: One file per day

### Custom Log Directory

Directory for log files is set when creating the Logger instance. Default is `./logs/`.

## Log Message Format

```
[Qase][HH:MM:SS][level] message
```

**Examples:**

```
[Qase][14:30:25][info] Test run completed successfully
[Qase][14:30:25][error] Failed to upload attachment
```

## Quick Reference

| Scenario | Console | File | Config |
|----------|---------|------|--------|
| Default | ✅ | ❌ | `{}` |
| Debug mode | ✅ | ✅ | `{"debug": true}` |
| File only | ❌ | ✅ | `{"logging": {"console": false, "file": true}}` |
| Silent | ❌ | ❌ | `{"logging": {"console": false, "file": false}}` |
| Both | ✅ | ✅ | `{"logging": {"console": true, "file": true}}` |
