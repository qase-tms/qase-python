# [Qase TestOps](https://qase.io) Reporters for Python

Monorepo containing [Qase TestOps](https://qase.io) integration tools for Python testing frameworks. This repository includes reporters and API clients designed to streamline the process of reporting test results to Qase TestOps.

## Projects Overview

### Reporters

- **[qase-pytest](/qase-pytest)**  
  Reporter for Pytest, including built-in support for Playwright-based tests.
  
- **[qase-robotframework](/qase-robotframework)**  
  Reporter for Robot Framework, enabling seamless integration with Qase TestOps.

### Libraries

- **[qase-python-commons](/qase-python-commons/)**  
  Shared library containing common components and utilities used by Qase reporters.

### API Clients

- **[qase-api-client](/qase-api-client)**  
  Official client for interacting with the Qase TestOps API (v1). Recommended for most use cases.
  
- **[qase-api-v2-client](/qase-api-v2-client)**  
  API client supporting the new Qase TestOps API (v2). Use this client for projects leveraging the latest API features.

### Deprecated

- **[qaseio](/qaseio)**  
  Legacy client for the Qase TestOps API (v1). Deprecated in favor of `qase-api-client` and should not be used in new projects.
