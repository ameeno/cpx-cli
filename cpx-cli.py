import os
import time

import click
import pandas as pd
import requests
from tabulate import tabulate

# to change server via env variable
CPX_URL = os.getenv("CPX_SERVER", "http://localhost:1234")


def connection_error():
    print(
        "Connection Error: Please check if CPX server is running on: "
        + CPX_URL
        + " or set env variable CPX_SERVER to the correct server"
    )
    exit(1)


def get_services():
    try:
        response = requests.get(f"{CPX_URL}/servers")
    except:
        connection_error()
    return response.json()


def get_service_info(ip):
    try:
        response = requests.get(f"{CPX_URL}/{ip}")
    except:
        connection_error()
    return response.json()


def get_services_status():
    services = get_services()
    data = []
    for service in services:
        info = get_service_info(service)
        # append to list of dicts
        data.append(
            {
                "IP": service,
                "Service": info["service"],
                # set status healthy if cpu and memory are less than 80% else unhealthy
                "Status": "Healthy"
                if int(info["cpu"].strip("%")) <= 80
                and int(info["memory"].strip("%")) <= 80
                else "Unhealthy",
                "CPU": info["cpu"],
                "Memory": info["memory"],
            }
        )
    return data


def get_average_cpu_memory():
    services = get_services_status()
    df = pd.DataFrame(services)
    # convert cpu and memory to float
    df["CPU"] = [float(c.strip("%")) for c in df["CPU"]]
    df["Memory"] = [float(m.strip("%")) for m in df["Memory"]]
    # group by service and get average cpu and memory
    grouped = df.groupby(["Service"]).agg({"CPU": "mean", "Memory": "mean"})
    # convert cpu and memory back to string with % sign - round to 1 decimal place
    grouped["CPU"] = [str(round(c, 1)) + "%" for c in grouped["CPU"]]
    grouped["Memory"] = [str(round(m, 1)) + "%" for m in grouped["Memory"]]
    return grouped.reset_index()


def get_unhealthy_services():
    services = get_services_status()
    unhealthy = [s for s in services if s["Status"] == "Unhealthy"]
    return unhealthy


def get_healthy_services():
    services = get_services_status()
    healthy = [s for s in services if s["Status"] == "Healthy"]
    return healthy


def get_flagged_services():
    services = get_healthy_services()
    service_counts = {}
    flagged = []
    # get count of healthy instances for each service that is healthy
    for service in services:
        service_counts[service["Service"]] = (
            service_counts.get(service["Service"], 0) + 1
        )
    # loop through to find services with count less than 2 healthy instances
    for service, count in service_counts.items():
        [flagged.append(s) for s in services if s["Service"] == service and count < 2]
    return flagged


def monitor_service(service_name):
    # monitor service until user exits
    while True:
        services = get_services_status()
        service_instances = [s for s in services if s["Service"] == service_name]
        print(tabulate(service_instances, headers="keys"))
        # sleep for 1 second
        time.sleep(1)


@click.group()
def cli():
    pass


@cli.command()
def list_services():
    services = get_services_status()
    print(tabulate(services, headers="keys"))


@cli.command()
def avg_cpu_memory():
    services = get_average_cpu_memory()
    print(
        "Average CPU and Memory usage for each service Type:"
        + "\n"
        + tabulate(services, headers="keys")
    )


@cli.command()
def unhealthy_services():
    services = get_unhealthy_services()
    print(
        "Unhealthy services: (>80% CPU or >80% Memory usage)"
        + "\n"
        + tabulate(services, headers="keys")
    )

    services = get_flagged_services()
    print(
        "Flagged services: (less than 2 healthy instances)"
        + "\n"
        + tabulate(services, headers="keys")
    )


@cli.command()
@click.argument("service_name")
def monitor(service_name):
    monitor_service(service_name)


if __name__ == "__main__":
    cli()
