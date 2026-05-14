# Upgrade guides

## From 5.x to 6.x

### Suite hierarchy is preserved

Prior to v6, the reporter registered each test under only the deepest (leaf) suite of its Robot Framework hierarchy. A test located in `Tests > Account > Login` ended up in a flat `Login` suite in Qase, with `Tests` and `Account` discarded.

Starting with v6, the reporter sends the full nested suite path, so the same test now lands in `Tests / Account / Login` in Qase.

Impact:

- If you are starting from a clean Qase project, no action is required.
- If your Qase project already has cases created against the old flattened layout (or you reorganised the tree manually), the next run will create cases in a new nested location, which can result in duplicates.

To avoid duplicates, either:

- accept the new hierarchy and remove or archive the old flat suites in Qase, or
- pin annotated tests to the existing cases by setting the Qase ID on each `*** Test Cases ***` entry (see [usage docs](usage.md)).

## From 2.x to 3.x

### Execution

In v3, we have renamed the internal package name.
To run the reporter, you need to add the listener to the command line:

```diff
- robot --listener qaseio.robotframework.qase_listener someTest.robot
+ robot --listener qase.robotframework.Listener someTest.robot
```

```sh
robot --listener qaseio.robotframework.qase_listener someTest.robot
```

### Bulk uploading results has changed

In v3, two configuration options defined how the reporter was uploading results to Qase:
`testops.bulk` and `testops.chunk`.

In v3, reporter always sends results in portions, called batches.
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

### Configuration
In the latest version of `qase-robotframework` reporter, we have changed the way of configuration. 
The primary source of truth from now is a config file `qase.config.json` 
that should be located in the same directory from where you run tests. 
This change will allow us to add more configuration options in the future 
and make the configuration process more flexible. 
This config structure will be used for all other reporters.

Also, the names of ENV variables have changed. 
You can find the list of all available options in the [configuration](../README.md#configuration) section.
