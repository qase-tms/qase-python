# Upgrade guides

## From 5.x to 6.x

### Import from `qase`

Import paths have slightly changed:

```diff
- from qaseio.pytest import qase
+ from qase.pytest import qase
```

### Bulk uploading results has changed

In v5, two configuration options defined how the reporter was uploading results to Qase:
`testops.bulk` and `testops.chunk`.

In v6, reporter always sends results in portions, called batches.
Default batch size is 200, and can be set to anything from 1 to 2000.
Update the config in the following way:

```diff
{
  "testops": {
-   "bulk": true, 
-   "chunk": 100
+   "batch": {
+     "size": 100
+   }
  }
}
```

## From 4.x to 5.x

### Configuration
In the latest version of `qase-pytest` reporter, we have changed the way of configuration. The primary source of truth from now is a config file `qase.config.json` that should be located in the same directory from where you run tests. This change will allow us to add more configuration options in the future and make the configuration process more flexible. This config structure will be used for all other reporters.

Also, we have changed the names of ENV variables and CLI options. You can find the list of all available options in the [configuration](../README.md#configuration) section.

### New context decorators
We have added new context decorators for fields to make them more flexible and reduce the amount of manual work. Instead of using `@qase.priority()`, `@qase.severity()`, `@qase.layer()` decorators, you can use `@qase.field("priority", "high")`, `@qase.field("severity", "critical")`, `@qase.field("layer", "unit")` decorators. Also, you can use `@qase.field("custom_field", "value")` to add custom fields to your test case.

Old decorators will be removed in the next major release.

### Selective execution
Starting with `5.0` version, we have added a new feature that allows you to run only tests that are linked to test cases in Qase TestOps. That changes the behavior of `test_plan_id` parameter. Now, if you specify one of these parameters, the reporter will run only tests that are linked to test cases in the specified test plan.