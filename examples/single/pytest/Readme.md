# How to run these examples

1. Clone the repository

    ```bash
    git clone https://github.com/qase-tms/qase-python.git
    ```

2. Move to the directory with the examples

    ```bash
    cd qase-python/examples/single/pytest
    ```

3. Install the required packages

    ```bash
    pip install -r requirements.txt
    ```

4. Add the Qase token and project code to the ENV variables

    ```bash
    export QASE_TESTOPS_API_TOKEN=your_token
    export QASE_TESTOPS_PROJECT=your_project_code
    ```

5. Run the tests

    ```bash
    pytest
    ```
