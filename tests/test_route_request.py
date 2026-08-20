import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from route_request import choose_route


class RouteRequestTests(unittest.TestCase):
    def test_explicit_route_wins(self) -> None:
        result = choose_route("用 fact-check 路由研究这条说法")
        self.assertEqual(result["route"], "fact-check")

    def test_decision_route(self) -> None:
        result = choose_route("两个设备改造方案选哪个，是否先做低成本试点")
        self.assertEqual(result["route"], "decision-analysis")

    def test_timeline_route(self) -> None:
        result = choose_route("梳理产品发展历程并比较当前竞品")
        self.assertEqual(result["route"], "timeline-cross-section")

    def test_provider_fallback_is_explicit(self) -> None:
        result = choose_route("深度研究一个技术方案")
        self.assertEqual(result["method_status"], "available")
        self.assertIn(result["status"], {"available", "method-available-provider-fallback"})
        self.assertLessEqual(len(result["collaborator_candidates"]), 2)


if __name__ == "__main__":
    unittest.main()
