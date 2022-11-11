import time

from flask import Blueprint, request, make_response, Response

from monitoring_utilities.cpu_monitor import (
    cpu_load,
    cpu_core_info,
    cpu_frequencies,
)
from monitoring_utilities.datatype import DataType
from monitoring_utilities.memory_monitor import memory_info
from monitoring_utilities.storage_monitor import storage_info
from server_state import service_time

self_server = Blueprint("server", __name__, url_prefix="/api")


@self_server.route("/")
def api_info() -> dict:
    """api version route"""

    return {
        "name": "system monitor",
        "version": "0.0.1",
    }


@self_server.route("/monitor/cpu/load")
def processor_load() -> dict:
    """Route to return the server cpu loading"""

    interval = request.args.get("interval", 0)
    return {
        "load": cpu_load(float(interval)),
    }


@self_server.route("/monitor/cpu/info")
def cpu_cores() -> dict:
    """Route to return the server cpu core info"""

    physical = cpu_core_info(logical=False)
    logical = cpu_core_info(logical=True)
    frequency = cpu_frequencies()
    return {
        "physical cores count": physical,
        "logical cores count": logical,
        "cores frequency": frequency,
    }


@self_server.route("/monitor/memory/info")
def memory_all_info() -> Response or dict:
    """Route to return the server load memory info"""

    raw_units = request.args.get("units", "GB")
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return memory_info(units)


@self_server.route("/monitor/memory/total")
def memory_total() -> Response or dict:
    """Route to return the server all memory info"""

    raw_units = request.args.get("units", "GB")
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return {
        "total": memory_info(units)["total"],
        "units": units.value,
    }


@self_server.route("/monitor/storage/info")
def storage_all_info() -> Response or dict:
    """Route to return the server load storage info"""

    raw_units = request.args.get("units", "GB")
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return {
        "total": storage_info(units)["total"],
        "used": storage_info(units)["used"],
        "percent": storage_info(units)["percent"],
        "free": storage_info(units)["free"],
        "units": units.value,
    }


@self_server.route("/monitor/storage/total")
def storage_total() -> Response or dict:
    """Route to return the server all storage info"""

    raw_units = request.args.get("units", "GB")
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return {
        "total": storage_info(units)["total"],
        "used": storage_info(units)["used"],
        "units": units.value,
    }


@self_server.route("/start_time")
def start_time() -> Response or dict:
    """Route ro return the server work time"""
    server_start = time.strftime("%a, %d %b %Y %H:%M:%S")
    return service_time(server_start)
