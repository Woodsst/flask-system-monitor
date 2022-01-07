from flask import Flask
from flask import request

from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from memory_monitor import memory_info
from storage_monitor import storage_info

app = Flask(__name__)


@app.route("/")
def welcome():
    return "<p>Welcome</p>"


@app.route('/api')
def api_info():
    return {
        'name': 'system monitor',
        'version': '0.0.1',
    }


@app.route('/monitor/cpu/load')
def processor_load():
    interval = request.args.get('interval', 0)
    return {
        'load': cpu_load(float(interval)),
    }


@app.route('/monitor/cpu/info')
def cpu_cores():
    physical = cpu_core_info(logical=False)
    logical = cpu_core_info(logical=True)
    frequency = cpu_frequencies()
    return {
        "physical cores count": physical,
        "logical cores count": logical,
        'cores frequency': frequency
    }


@app.route('/monitor/memory/info')
def memory_all_info():
    units = request.args.get('units')
    if units is None:
        return memory_info()
    if units == 'K':
        return memory_info(Kb=True)
    if units == 'G':
        return memory_info(Gb=True)
    if units == 'M':
        return memory_info(Mb=True)
    if units == 'T':
        return memory_info(Tb=True)


@app.route('/monitor/memory/total')
def memory_total():
    units = request.args.get('units')
    storage_dict = memory_info()
    if units is None:
        storage_dict = memory_info()
        units = 'B'
    if units == 'T':
        storage_dict = memory_info(Tb=True)
    if units == 'G':
        storage_dict = memory_info(Gb=True)
    if units == 'M':
        storage_dict = memory_info(Mb=True)
    if units == 'K':
        storage_dict = memory_info(Kb=True)
    return {
        "mem": storage_dict['total'],
        "units": units,
    }


@app.route('/monitor/storage/info')
def storage_all_info():
    units = request.args.get('units')
    storage_dict = storage_info()
    if units is None:
        storage_dict = storage_info()
        units = 'B'
    if units == 'T':
        storage_dict = storage_info(Tb=True)
    if units == 'G':
        storage_dict = storage_info(Gb=True)
    if units == 'M':
        storage_dict = storage_info(Mb=True)
    if units == 'K':
        storage_dict = storage_info(Kb=True)
    return {
        "total": storage_dict['total'],
        'used': storage_dict['used'],
        'percent': storage_dict['percent'],
        'free': storage_dict['free'],
        "units": units,
    }


@app.route('/monitor/storage/total')
def storage_total():
    units = request.args.get('units')
    storage_dict = storage_info()
    if units is None:
        storage_dict = storage_info()
        units = 'B'
    if units == 'T':
        storage_dict = storage_info(Tb=True)
    if units == 'G':
        storage_dict = storage_info(Gb=True)
    if units == 'M':
        storage_dict = storage_info(Mb=True)
    if units == 'K':
        storage_dict = storage_info(Kb=True)
    return{
        'total': storage_dict['total'],
        'used': storage_dict['used'],
        'units': units,
    }
