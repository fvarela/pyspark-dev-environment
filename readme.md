# PySpark - Databricks Local Development Environment

This project provides a local development environment for working with PySpark and Databricks. It offers two development environments: one with a local Spark setup and another with Databricks Connect.

## Development Environments

The project includes two separate Python virtual environments:

1. Local Spark Environment: `~/.virtualenvs/.venv-spark`
2. Databricks Connect Environment: `~/.virtualenvs/.venv-databricks`

## Databricks Configuration

To use the Databricks Connect environment, you need to create a `databricks-cli-config` file using the following template:

```
[DEFAULT]
host = https://...
token = ...
cluster_id = ...
```

Replace the ellipses (...) with your specific Databricks information.

## Visual Studio Code Setup

This project is configured to be used with Visual Studio Code inside a Docker container. The necessary configuration files (Dockerfile, docker-compose, and .devcontainer) are provided.

To set up the development environment:

1. Open the project in Visual Studio Code.
2. Use the "Remote-Containers: Open Folder in Container" command to open the project inside the container.
3. Once inside the container, select the desired Python interpreter from the list:
   - For local Spark: `~/.virtualenvs/.venv-spark`
   - For Databricks Connect: `~/.virtualenvs/.venv-databricks`

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