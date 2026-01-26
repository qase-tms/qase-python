### Behave Example

This is a sample project demonstrating how to write and execute tests using the Behave framework with integration to
Qase Test Management.

---

## Prerequisites

Ensure that the following tools are installed on your machine:

1. [Python](https://www.python.org/) (version 3.7 or higher is recommended)
2. [pip](https://pip.pypa.io/en/stable/)

---

## Setup Instructions

1. Clone this repository by running the following commands:
   ```bash
   git clone https://github.com/qase-tms/qase-python.git
   cd qase-python/examples/single/behave
   ```

2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `qase.config.json` file in the root of the project. Follow the instructions on  
   [how to configure the file](https://github.com/qase-tms/qase-python/blob/main/qase-behave/docs/CONFIGURATION.md).

4. To run tests and upload the results to Qase Test Management, use the following command:
   ```bash
   behave --format=qase.behave.formatter:QaseFormatter
   ```
   This will execute the tests and display the results in the terminal.

---

## Additional Resources

For more details on how to use this integration with Qase Test Management, visit  
the [Qase Behave documentation](https://github.com/qase-tms/qase-python/tree/main/qase-behave).
