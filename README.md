# Cloud Provider X (CPX) Command Line Tool

This command line tool queries the Cloud Provider X (CPX) API to get information about running services. It has the following commands:

* `list-services`: Lists the running services and their status, CPU, and memory usage.
* `avg-cpu-memory`: Calculates the average CPU and memory usage of services of the same type.
* `unhealthy-services`: Flags services that have fewer than 2 healthy instances running.
* `monitor`: Tracks and prints the CPU/Memory usage of all instances of a given service over time.

## Installation

1. Clone the repository: git clone <https://github.com/ameeno/cpx-cli.git>
2. Navigate to the repository directory: `cd cpx-cli` and create a virtual environment: `python3 -m venv venv` - this project has been tested on python 3.11.2.
3. Activate the virtual environment: `source venv/bin/activate`
4. Install the required libraries: `pip install -r requirements.txt`
5. Set the CPX_SERVER environment variable to your CPX server and port url for example `export CPX_SERVER='http://localhost:5000'`. this tool uses that environment variable to determine the location and port of the CPX server.

## Usage

To run the tool, use the following command:

```code
python cpx-cli.py [command] [arguments]
```

Replace [command] with one of the commands listed above, and [arguments] with any arguments required by the command.

### List Services

The list_services command lists the running services and their status, CPU, and memory usage.

```code
python cpx-cli.py list-services
```

### Average CPU/Memory

The avg-cpu-memory command calculates the average CPU and memory usage of services of the same type (using mean).

```code
python cpx-cli.py avg-cpu-memory
```

### Unhealthy Services

The unhealthy-services command prints all unhealthy services and also those that have fewer than 2 healthy instances running (flagged).

```code
python cpx-cli.py unhealthy-services
```

### Monitor

The monitor command tracks and prints the CPU/Memory usage of all instances of a given service over time.

```code
python cpx-cli.py monitor [service_name]
```

Replace [service_name] with the name of the service to monitor.

### Requirements

And here's the requirements.txt file:

```makefile
click==8.1.3
pandas==1.5.3
tabulate==0.9.0
requests==2.28.2
```

## Design Choices

* Tool is designed as a CLI with four commands.
* click, requests, pandas, and tabulate libraries are used.
* monitor command continuously updates CPU/Memory usage.
* Tool queries CPX API to get information about running services.
* Tool uses pandas library to calculate averages.
* Relies upon environment variable to set server location and port.

## Trade-offs

* Assumes CPX API is available and accessible.
* Uses pandas library for calculating averages, which may not be necessary for smaller datasets.
* Assumes unique service names without spaces.
* prints error if not connectable to CPX API.
* has not been tested against SSL/TLS enabled CPX API endpoints.

## Future Improvements

* Add support for other cloud providers.
* Add filters for services.
* Add support for multiple authentication methods.
* Add ability to output data in different formats.
* Improve error handling and user feedback.
* Add commands for detailed information, scaling services, scheduling tasks, and triggering alerts.
* Add support for multiple regions or availability zones.
* Add ability to save and load configurations.
* Add ability to run the tool in a web interface.
* Ability to store configurations and preferences in a config file.
* Ability to cache and monitor data over time.
