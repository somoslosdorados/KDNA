# Logger Program

## Overview

This logger program provides a simple way to log messages with a timestamp, alert level, calling path, and the message itself. The logs are stored in the "kdna/logs/logs.log" file.

## Authors

- Sarah THEOULLE
- Théo TCHILINGUIRIAN

## Usage

To log messages using this program, follow these steps:

1. Import the module:

    ```python
    from logger import log
    ```

2. Use the `log` function:

    ```python
    log("INFO", "This is an informational message.")
    ```

   Make sure to replace "INFO" with the appropriate alert level and provide the desired message.

## Function Details

### `log(alert_level: str, msg: str) -> int`

Writes the given input to the logs file.

- `alert_level`: The importance or type of the logged message.
- `msg`: The message to print and log.
- Returns: Number of characters written.

## Example

```python
from logger import log

log("ERROR", "An error occurred in the application.")
