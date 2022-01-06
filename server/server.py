from flask import request
from flask import Flask
from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies

app = Flask(__name__)


@app.route("/")
def welcome():
    return


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


# T - terabytes
# G - gigabytes
# M - megabytes
# K - kilobytes
# B - bytes

# as a parameter use units, default = G


@app.route('/monitor/mem/used')
def memory_status():
    return {
        "used": 2.44,
        "units": "Gb",
    }


@app.route('/monitor/mem/used?unit=K')
def memory_used():
    return {
        "used": 2440000,
        "units": "Kb",
    }


# // same here


@app.route('/monitor/mem/total')
def memory():
    return {
        "mem": 16,
        "units": "Gb",
    }


# /monitor/mem/total?unit=K
# {
#     "mem": 16000000
#     "units": "Kb",
# }


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