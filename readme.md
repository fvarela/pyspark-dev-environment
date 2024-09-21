# PySpark Local Development Environment

This project provides a proof-of-concept setup for creating a local development environment with PySpark using Docker and Visual Studio Code's Remote - Containers extension.

## Project Overview

This setup allows you to develop and run PySpark applications in a containerized environment, ensuring consistency across different development machines and simplifying the setup process.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code

## Project Structure

```
.
├── .devcontainer/
│   └── devcontainer.json
├── app/
│   ├── delta_table_poc.py
│   └── spark_test_poc.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone this repository to your local machine.
2. Ensure Docker is running on your system.
3. Open the project folder in Visual Studio Code.
4. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command from the command palette (F1).

VS Code will build the Docker image and start the container. This process may take a few minutes the first time.

## Usage

Once the container is running and VS Code is connected:

1. You'll be in the `/workspace` directory inside the container, which is mapped to your project root.
2. Open a new terminal in VS Code (Terminal -> New Terminal) to interact with the container's shell.
3. You can now run PySpark scripts or start a PySpark shell:

   ```
   pyspark
   ```

4. To run a Python script that uses PySpark:

   ```
   python3 your_script.py
   ```

## Test Scripts

The project includes two test scripts to verify the functionality of the PySpark environment:

1. `app/delta_table_poc.py`: This script demonstrates the usage of Delta Lake with PySpark. It creates a Delta table, performs some operations, and showcases Delta Lake features.

   To run this script:
   ```
   python3 app/delta_table_poc.py
   ```

2. `app/spark_test_poc.py`: This script provides a basic test of the PySpark functionality. It creates a simple Spark DataFrame and performs some operations to ensure that PySpark is working correctly.

   To run this script:
   ```
   python3 app/spark_test_poc.py
   ```

These scripts serve as both examples of how to use PySpark in this environment and as functional tests to ensure your setup is working correctly.

## Customization

- To add more Python packages, update the `requirements.txt` file and rebuild the container.
- Modify the `Dockerfile` or `docker-compose.yml` to add more tools or change the configuration.

## Troubleshooting

- If you encounter issues with the container not starting, try rebuilding it using the "Remote-Containers: Rebuild Container" command in VS Code.
- Ensure your Docker daemon is running before attempting to start the container.
- If the test scripts fail, check that all required dependencies are correctly installed and that the PySpark configuration is correct.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or encounter any problems.

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 Francisco Varela

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


