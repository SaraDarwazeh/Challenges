import requests
from threading import Thread, Lock
from time import perf_counter
from statistics import mean

URL = "http://127.0.0.1:8000/reports/transactions/"
N = 2
TIMEOUT = 100  # seconds


class LoadTester:
    def __init__(self, url: str, n: int = 2, timeout: int = 100, verbose: bool = True):
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
            elapsed_s = perf_counter() - start

            result = {
                "i": i,
                "ok": 200 <= r.status_code < 300,
                "status": r.status_code,
                "s": elapsed_s,
                "error": None,
            }

        except requests.RequestException as e:
            elapsed_s = perf_counter() - start
            result = {
                "i": i,
                "ok": False,
                "status": None,
                "s": elapsed_s,
                "error": f"{type(e).__name__}: {e}",
            }

        # Store + optional per-request print (lock avoids messy interleaved output)
        with self.lock:
            self.results.append(result)
            if self.verbose:
                if result["error"]:
                    print(f"[{i:02d}] ERROR  {result['s']:.2f} s  {result['error']}")
                else:
                    print(f"[{i:02d}] {result['status']}    {result['s']:.2f} s")

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

        # Latencies (seconds)
        latencies = [r["s"] for r in results]
        avg_s = mean(latencies) if latencies else 0.0
        max_s = max(latencies) if latencies else 0.0
        min_s = min(latencies) if latencies else 0.0

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
        print(f"Latency (s): avg={avg_s:.2f}  min={min_s:.2f}  max={max_s:.2f}")
        print(f"Status counts: {status_counts}")
        print("=" * 48)

        # If failures exist, show a quick list
        failures = [r for r in results if not r["ok"]]
        if failures:
            print("\nFailures:")
            for r in failures:
                if r["error"]:
                    print(f"  - [{r['i']:02d}] ERROR  {r['s']:.2f} s  {r['error']}")
                else:
                    print(f"  - [{r['i']:02d}] {r['status']}    {r['s']:.2f} s")
