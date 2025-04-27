# Health Monitoring Tool

This Tool monitors the health of provided API's and generate domain availability percentage.

## Table of Contents

- [Installation](#Installation)
- [Problems with Solution](#Problems with Solution)
- [Limitation](#Limitation)


## Installation

1. **Fork and clone** this repository:

    ```bash
    git clone https://github.com/shrutinag04/sre-take-home-exercise-python.git
    cd <path>/sre-take-home-exercise-python
    ```

2. **Install Python** (if not already installed).

3. **Run the main file** with your `sample.yaml` configuration:

    ```bash
    python main.py sample.yaml
    ```

    - The `sample.yaml` file contains the API endpoints to test.

4. *(Optional)* **Set up debugging configuration** with `launch.json` in VS Code:

    Create a `.vscode/launch.json` file with the following content:

    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "name": "Python: Debug main.py",
          "type": "python",
          "request": "launch",
          "program": "${workspaceFolder}/main.py",
          "args": ["sample.yaml"],
          "console": "integratedTerminal"
        }
      ]
    }
    ```

    - This allows you to debug `main.py` directly with the `sample.yaml` file as an argument.


## Problems with Solution

1. **Error Encountered While Running the File:**

    ```bash
    AttributeError: 'NoneType' object has no attribute 'upper'
    ```

    - This error occurs in the `requests.request` method at **line 20**, when trying to handle the HTTP method argument.
    
    **Cause:**
    - `requests` expects the HTTP method (like `"GET"`, `"POST"`) to be a valid **string**.

    **Solution:**
    - Set a default value of `"GET"` when retrieving the method from the `endpoint` dictionary.
    - Modify the code at **line 15** as follows:

    ```python
    method = endpoint.get('method', 'GET')
    ```

    - This ensures that if no method is specified, it will default to `"GET"` and prevent the `AttributeError`.


2. **Endpoint Availability Check:**

   The endpoint should meet two criteria to be considered available:

   - The status code should be between **200** and **299** (already implemented).
   - The endpoint must respond within **500 milliseconds**.

   **Solution:**
   - Check the response time and convert it to milliseconds.
   - Update **line 22** with the following code:

   ```python
   if (response.elapsed.total_seconds() * 1000) <= 500:


3. **Ignore Port Numbers When Determining the Domain:**

   The domain should be extracted without considering the port number.

   **Solution:**
   - Split the domain string at the colon (`:`) to ignore the port number.
   - Update **line 55** as follows:

   ```python
   domain = domain.split(":")[0]


4. **Check Cycles Must Run and Log Availability Results Every 15 Seconds:**

   The availability check should run and log results every 15 seconds, regardless of the number of endpoints or their response times.

   **Initial Approach:**
   - Initially, I tried logging the start time in the `monitor` method, then logging the elapsed time after checking the health of each endpoint.
   - However, this approach fails when the health check takes a long time (e.g., due to a high number of endpoints), causing the 15-second logging interval to be skipped.

   **Solution:**
   - To ensure that the availability check runs independently of response times and logs every 15 seconds, I implemented **threads**.
   - For each endpoint, a separate thread is created and runs concurrently. This enables the availability check to proceed while ensuring the logging occurs every 15 seconds independently.

   **Enhancement:**
   - To handle this within threads, I added an additional argument to the `check_health(endpoint, result_dict)` method. This argument stores each thread's result and calculates domain stats for the "UP" status.
   
   ```python
   elapsed_time = time.time() - start_time
   if elapsed_time >= 15: 
       # Check if 15 seconds have passed and log availability results


## Limitation

   Currently, the code requires a 15-second wait before the first log appears after execution begins.
