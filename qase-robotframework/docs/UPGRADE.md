# Upgrade guides

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
