import time
import random

from prometheus_client import start_http_server, Gauge, Counter
from prometheus_summary import Summary


# latency
request_latency_ms_metric = Summary(
    'request_latency_ms',
    'Time spent processing request',
    invariants=((0.50, 0.05), (0.75, 0.02), (0.90, 0.01), (0.95, 0.005), (0.99, 0.001)),
)
MIN_LATENCY_MS = 100

# traffic and errors
responses_metric = Counter('responses', 'Responses', labelnames=['code', 'path', 'method'])

# saturation
MEM_TOTAL_MB = 4 * 1024  # 4 gb
MEM_FAKE_USAGE_MB = 2.5 * 1024  # 2.5 gb in use

mem_used_mb_metric = Gauge('mem_used_mb', 'Used memory in megabytes')
mem_free_mb_metric = Gauge('mem_free_mb', 'Free memory in megabytes')
mem_total_mb_metric = Gauge('mem_total_mb', 'Total memory in megabytes')

CPU_TOTAL_MS = 2 * 1000  # 2 cores
CPU_FAKE_USAGE_MS = 1.5 * 1000  # 1.5 core in use

cpu_work_time_ms_metric = Gauge('cpu_work_time_ms', 'CPU work time in milliseconds')
cpu_idle_time_ms_metric = Gauge('cpu_idle_time_ms', 'CPU idle time in milliseconds')
cpu_total_time_ms_metric = Gauge('cpu_total_time_ms', 'CPU time in milliseconds')

mem_total_mb_metric.set(MEM_TOTAL_MB)
cpu_total_time_ms_metric.set(CPU_TOTAL_MS)
paths = ['order', 'client']
methods = ['get', 'post', 'put', 'delete']

MIN_RPS = 90
MAX_RPS = 150

FIVE_MINS = 5 * 60
TEN_MINS = 10 * 60


def simulate_traffic():
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > TEN_MINS:
            start_time = time.time()
            continue

        if elapsed_time <= FIVE_MINS:  # Рост числа запросов
            num_requests = int(MIN_RPS + ((MAX_RPS - MIN_RPS) * (elapsed_time / FIVE_MINS)))
        else:  # Падение числа запросов
            num_requests = int(MAX_RPS - ((MAX_RPS - MIN_RPS) * ((elapsed_time - FIVE_MINS) / FIVE_MINS)))

        error_rate_5xx = 0.02
        error_rate_4xx = error_rate_5xx + 0.05
        redirect_rate_3xx = + error_rate_4xx + 0.06

        for _ in range(num_requests):
            path = random.choice(paths)
            method = random.choice(methods)

            if random.random() < error_rate_5xx:
                code = '5xx'
            elif random.random() < error_rate_4xx:
                code = '4xx'
            elif random.random() < redirect_rate_3xx:
                code = '3xx'
            else:
                code = '2xx'

            responses_metric.labels(code=code, path=path, method=method).inc()

            request_latency_ms_metric.observe(MIN_LATENCY_MS + ((random.uniform(0, 1) ** 2) + random.gauss(0, 0.1)) * MIN_LATENCY_MS)

        cpu_usage = CPU_FAKE_USAGE_MS + (CPU_TOTAL_MS - CPU_FAKE_USAGE_MS) * (num_requests / MAX_RPS) * 0.5 + random.randint(0, 500)
        mem_usage = MEM_FAKE_USAGE_MB + (MEM_TOTAL_MB - MEM_FAKE_USAGE_MB) * (num_requests / MAX_RPS) * 0.2 + random.randint(0, 10)

        cpu_work_time_ms_metric.set(cpu_usage)
        cpu_idle_time_ms_metric.set(CPU_TOTAL_MS - cpu_usage)

        mem_used_mb_metric.set(mem_usage)
        mem_free_mb_metric.set(MEM_TOTAL_MB - mem_usage)

        time.sleep(1)


if __name__ == '__main__':
    start_http_server(8000)
    simulate_traffic()
