import psutil


def cpu_load(interval):
    return psutil.cpu_percent(interval)


def cpu_core_info(logical: bool):
    if logical is True:
        return psutil.cpu_count()
    else:
        return psutil.cpu_count(logical=False)


def cpu_frequencies():
    return psutil.cpu_freq(percpu=False)
