import psutil


def cpu_load(interval: int) -> float:
    return psutil.cpu_percent(interval)


def cpu_core_info(logical: bool) -> float:
    if logical is True:
        return psutil.cpu_count()
    return psutil.cpu_count(logical=False)


def cpu_frequencies() -> tuple:
    return psutil.cpu_freq(percpu=False)
