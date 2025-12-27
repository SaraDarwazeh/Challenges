import requests
from threading import Thread, Lock
from time import perf_counter
from statistics import mean

URL = "http://127.0.0.1:8000/reports/transactions/"
N = 10
TIMEOUT = 100  # seconds


class LoadTester:
    def __init__(self, url: str, n: int = 10, timeout: int = 10, verbose: bool = True):
        self.url = url
        self.n = n
        self.timeout = timeout
        self.verbose = verbose
        self.results = []
        self.lock = Lock()

    def worker(self, i: int) -> None:
        start = perf_counter()
        try:
            r = requests.get(self.url, timeout=self.timeout)
            elapsed_ms = (perf_counter() - start) * 1000

            result = {
                "i": i,
                "ok": 200 <= r.status_code < 300,
                "status": r.status_code,
                "ms": elapsed_ms,
                "error": None,
            }

        except requests.RequestException as e:
            elapsed_ms = (perf_counter() - start) * 1000
            result = {
                "i": i,
                "ok": False,
                "status": None,
                "ms": elapsed_ms,
                "error": f"{type(e).__name__}: {e}",
            }

        # Store + optional per-request print (lock avoids messy interleaved output)
        with self.lock:
            self.results.append(result)
            if self.verbose:
                if result["error"]:
                    print(f"[{i:02d}] ERROR  {result['ms']:.2f} ms  {result['error']}")
                else:
                    print(f"[{i:02d}] {result['status']}    {result['ms']:.2f} ms")

    def run(self) -> None:
        threads = []
        for i in range(self.n):
            t = Thread(target=self.worker, args=(i,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def report(self) -> None:
        # Sort by request index
        results = sorted(self.results, key=lambda x: x["i"])
        total = len(results)
        success = sum(1 for r in results if r["ok"])
        failed = total - success

        # Latencies
        latencies = [r["ms"] for r in results]
        avg_ms = mean(latencies) if latencies else 0.0
        max_ms = max(latencies) if latencies else 0.0
        min_ms = min(latencies) if latencies else 0.0

        # Status breakdown
        status_counts = {}
        for r in results:
            key = r["status"] if r["status"] is not None else "ERROR"
            status_counts[key] = status_counts.get(key, 0) + 1

        print("\n" + "=" * 48)
        print(f"URL: {self.url}")
        print(f"Parallel requests: {self.n} (threads)")
        print(f"Timeout: {self.timeout}s")
        print("-" * 48)
        print(f"Success: {success}/{total} | Failed: {failed}/{total}")
        print(f"Latency (ms): avg={avg_ms:.2f}  min={min_ms:.2f}  max={max_ms:.2f}")
        print(f"Status counts: {status_counts}")
        print("=" * 48)

        # If failures exist, show a quick list
        failures = [r for r in results if not r["ok"]]
        if failures:
            print("\nFailures:")
            for r in failures:
                if r["error"]:
                    print(f"  - [{r['i']:02d}] ERROR  {r['ms']:.2f} ms  {r['error']}")
                else:
                    print(f"  - [{r['i']:02d}] {r['status']}    {r['ms']:.2f} ms")


if __name__ == "__main__":
    tester = LoadTester(url=URL, n=N, timeout=TIMEOUT, verbose=True)
    tester.run()
    tester.report()
