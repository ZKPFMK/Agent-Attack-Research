import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crbench import parsers  # noqa: E402
from crbench.parsers import Record, parse_text, register_parser, values  # noqa: E402

# All logs below are SYNTHETIC. They model agent-harness, benchmark-tool and
# local-resource output; they are not measurements from a live target.


class TestParsers(unittest.TestCase):
    def test_agent_jsonl(self):
        txt = "\n".join([
            json.dumps({"arm": "naive", "task": "tool-routing", "latency_ms": 12.5,
                        "success": False, "tokens": 240, "queries": 2}),
            json.dumps({"arm": "proposed", "task": "tool-routing", "latency_s": 1.5,
                        "success": True, "utility": 0.9, "detected": 0, "input_tokens": 120,
                        "output_tokens": 80, "queries": 3, "cost": 0.003, "status": "ok"}),
        ]) + "\n"
        recs = parse_text(txt, "auto")
        self.assertAlmostEqual(values(recs, "time", "naive")[0], 0.0125)
        self.assertAlmostEqual(values(recs, "time", "proposed")[0], 1.5)
        self.assertEqual(values(recs, "success", "naive"), [0.0])
        self.assertEqual(values(recs, "success", "proposed"), [1.0])
        self.assertEqual(values(recs, "queries", "proposed"), [3.0])
        self.assertEqual(values(recs, "cost", "proposed"), [0.003])
        self.assertTrue(any(r.metric == "status" and r.value == "ok" for r in recs))

    def test_generic(self):
        txt = ("planner time: 12.5 ms\nrouter elapsed = 3 us\n"
               "tool-call took 1.5 s\nRESULT name=proposed latency=2.5ms tokens=26 status=SUCCESS\n")
        recs = parse_text(txt, "generic")
        t = values(recs, "time")
        self.assertAlmostEqual(t[0], 0.0125)
        self.assertAlmostEqual(t[1], 3e-6)
        self.assertAlmostEqual(t[2], 1.5)
        self.assertAlmostEqual(values(recs, "latency", "proposed")[0], 0.0025)
        self.assertEqual(values(recs, "tokens", "proposed"), [26.0])
        self.assertTrue(any(r.metric == "status" and r.value == "SUCCESS" for r in recs))

    def test_criterion(self):
        txt = "agentdojo-style/task-01\n                        time:   [11.200 ms 11.350 ms 11.500 ms]\n"
        recs = parse_text(txt, "auto")
        mid = [r for r in recs if r.metric == "time"][0]
        self.assertAlmostEqual(mid.value, 0.01135)
        self.assertEqual(mid.label, "agentdojo-style/task-01")
        self.assertAlmostEqual(values(recs, "time_lo")[0], 0.0112)

    def test_gobench(self):
        txt = "goos: linux\nBenchmarkAgentRoute/agents=4-8   \t    1000\t   1234567 ns/op\t  4096 B/op\t  12 allocs/op\nPASS\n"
        recs = parse_text(txt, "auto")
        self.assertAlmostEqual(values(recs, "time")[0], 1.234567e-3)
        self.assertEqual(recs[0].label, "BenchmarkAgentRoute/agents=4")
        self.assertEqual(values(recs, "alloc"), [4096.0])

    def test_gbench(self):
        txt = ("-----------------------------------------------------------\n"
               "Benchmark                 Time             CPU   Iterations\n"
               "-----------------------------------------------------------\n"
               "BM_ToolSelection         1.50 ms         1.49 ms          466\n")
        recs = parse_text(txt, "auto")
        self.assertAlmostEqual(values(recs, "time")[0], 1.5e-3)
        self.assertAlmostEqual(values(recs, "cpu_time")[0], 1.49e-3)

    def test_solver_status(self):
        txt = "c local harness precheck\ns UNSATISFIABLE\nc total process time since initialization:         2.41    seconds\n"
        recs = parse_text(txt, "auto")
        self.assertEqual(values(recs, "time"), [2.41])
        self.assertTrue(any(r.value == "UNSATISFIABLE" for r in recs))

    def test_gnu_time(self):
        txt = "\tElapsed (wall clock) time (h:mm:ss or m:ss): 1:02.50\n\tMaximum resident set size (kbytes): 2048\n"
        recs = parse_text(txt, "auto")
        self.assertEqual(values(recs, "time"), [62.5])
        self.assertEqual(values(recs, "max_rss"), [2048 * 1024.0])

    def test_register_custom(self):
        @register_parser("toytool", "custom", sniff=r"^TOYTOOL")
        def _p(text):
            return [Record("time", float(text.split()[-1]), "s", "toy", 1)]

        self.assertIn("toytool", parsers.REGISTRY)
        self.assertEqual(values(parse_text("TOYTOOL v1 0.25", "auto")), [0.25])
        parsers.REGISTRY.pop("toytool")

    def test_regex_parser_builder(self):
        parsers.regex_parser("toyrx", r"^lat=(?P<value>\d+(?:\.\d+)?)(?P<unit>ms)", description="x")
        self.assertEqual(values(parse_text("lat=3ms\n", "toyrx")), [0.003])
        parsers.REGISTRY.pop("toyrx")

    def test_adapters_reference_real_parsers(self):
        from crbench.adapters import ADAPTERS
        for name, a in ADAPTERS.items():
            self.assertIn(a["parser"], parsers.REGISTRY, name)

    def test_unknown(self):
        with self.assertRaises(KeyError):
            parse_text("x", "nope")
        with self.assertRaises(ValueError):
            parsers.to_seconds(1, "fortnights")


if __name__ == "__main__":
    unittest.main()
