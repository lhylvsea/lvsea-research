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

    def test_research_diagram_route(self) -> None:
        result = choose_route("研究 Kubernetes 架构并生成可视化知识图谱")
        self.assertEqual(result["route"], "research-diagram")
        self.assertEqual(result["depth"], "standard")

    def test_explicit_research_diagram_route_wins(self) -> None:
        result = choose_route("用 research-to-diagram 研究石墨深加工工艺并做结构图")
        self.assertEqual(result["route"], "research-diagram")

    def test_academic_question_mode(self) -> None:
        result = choose_route("把研究兴趣转成可检索、可证伪的研究问题，并给出文献检索概念")
        self.assertEqual(result["route"], "academic-research")
        self.assertEqual(result["academic_mode"], "question-discovery")

    def test_academic_evidence_mode(self) -> None:
        result = choose_route("精读这篇论文，提取主张原文定位，做证据图和引用审计")
        self.assertEqual(result["route"], "academic-research")
        self.assertEqual(result["academic_mode"], "evidence-audit")

    def test_academic_design_mode(self) -> None:
        result = choose_route("审查研究方案的设计、数据可取得性和统计方法")
        self.assertEqual(result["route"], "academic-research")
        self.assertEqual(result["academic_mode"], "design-review")

    def test_academic_writing_mode(self) -> None:
        result = choose_route("按样稿保持学术语气，修订博士论文并准备投稿")
        self.assertEqual(result["route"], "academic-research")
        self.assertEqual(result["academic_mode"], "academic-writing")

    def test_academic_fast_lookup_stays_fast(self) -> None:
        result = choose_route("查一下这篇论文的 DOI 和正式题名")
        self.assertEqual(result["route"], "fast-retrieval")

    def test_decision_remains_primary_when_diagram_is_only_format(self) -> None:
        result = choose_route("比较两个设备改造方案并做一张决策结构图")
        self.assertEqual(result["route"], "decision-analysis")

    def test_provider_fallback_is_explicit(self) -> None:
        result = choose_route("深度研究一个技术方案")
        self.assertEqual(result["method_status"], "available")
        self.assertIn(result["status"], {"available", "method-available-provider-fallback"})
        self.assertLessEqual(len(result["collaborator_candidates"]), 2)


if __name__ == "__main__":
    unittest.main()
