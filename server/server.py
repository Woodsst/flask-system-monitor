from flask import Flask
from flask import request

from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from datatype import DataType
from memory_monitor import memory_info
from storage_monitor import storage_info

app = Flask(__name__)


@app.route("/")
def welcome():
    return "<p>Welcome</p>"


@app.route('/api')
def api_info() -> dict:
    return {
        'name': 'system monitor',
        'version': '0.0.1',
    }


@app.route('/monitor/cpu/load')
def processor_load() -> dict:
    interval = request.args.get('interval', 0)
    return {
        'load': cpu_load(float(interval)),
    }


@app.route('/monitor/cpu/info')
def cpu_cores() -> dict:
    physical = cpu_core_info(logical=False)
    logical = cpu_core_info(logical=True)
    frequency = cpu_frequencies()
    return {
        "physical cores count": physical,
        "logical cores count": logical,
        'cores frequency': frequency
    }


@app.route('/monitor/memory/info')
def memory_all_info() -> dict:
    units = request.args.get('units', DataType.Gigabyte.value)
    return memory_info(units)


@app.route('/monitor/memory/total')
def memory_total() -> dict:
    units = request.args.get('units', DataType.Gigabyte.value)
    storage_dict = memory_info(units)
    return {
        "mem": storage_dict['total'],
        "units": units,
    }


@app.route('/monitor/storage/info')
def storage_all_info() -> dict:
    units = request.args.get('units', DataType.Gigabyte.value)
    storage_dict = storage_info(units)
    return {
        "total": storage_dict['total'],
        'used': storage_dict['used'],
        'percent': storage_dict['percent'],
        'free': storage_dict['free'],
        "units": units,
    }


@app.route('/monitor/storage/total')
def storage_total() -> dict:
    units = request.args.get('units', DataType.Gigabyte.value)
    storage_dict = storage_info(units)
    return{
        'total': storage_dict['total'],
        'used': storage_dict['used'],
        'units': units,
    }
