from flask import request
from flask import Flask
from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from memory_monitor import memory_info

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


@app.route('/monitor/mem/used')
def memory_all_info():
    unit = request.args.get('unit')
    if unit is None:
        return memory_info()
    if unit == 'K':
        return memory_info(Kb=True)
    if unit == 'G':
        return memory_info(Gb=True)
    if unit == 'M':
        return memory_info(Mb=True)
    if unit == 'T':
        return memory_info(Tb=True)


@app.route('/monitor/mem/total')
def memory_total():
    unit = request.args.get('unit')
    memory_dict = memory_info()
    if unit is None:
        memory_dict = memory_info()
        unit = 'B'
    if unit == 'Tb':
        memory_dict = memory_info(Tb=True)
    if unit == 'Gb':
        memory_dict = memory_info(Gb=True)
    if unit == 'Mb':
        memory_dict = memory_info(Mb=True)
    if unit == 'Kb':
        memory_dict = memory_info(Kb=True)
    return {
        "mem": memory_dict['total'],
        "units": unit,
    }


@app.route('/monitor/storage/info')
def memory_size():
    return {
        "awailable": 320,
        "total": 2000,
        "units": "Gb",
    }

# /monitor/storage/info?units=B
# {
#     "awailable": 320000000000
#     "total": 2000000000000
#     "units": "b",
# }