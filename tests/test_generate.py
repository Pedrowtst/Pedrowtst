import copy
import datetime as dt
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import profile_data as g
import generate as liquid


class ProfileTests(unittest.TestCase):
    def fixture(self):
        now = dt.datetime(2026, 1, 2, 12, tzinfo=dt.timezone.utc)
        start = dt.date(2025, 2, 1)
        days = [{"date": (start + dt.timedelta(days=i)).isoformat(), "contributionCount": 1}
                for i in range((now.date() - start).days + 1)]
        return {"totalContributions": len(days), "weeks": [{"contributionDays": days}]}, now

    def test_months_cross_year_boundary(self):
        self.assertEqual(g.month_window(dt.date(2026, 1, 2)),
                         [f"2025-{i:02d}" for i in range(2, 13)] + ["2026-01"])

    def test_leap_year_window(self):
        months = g.month_window(dt.date(2024, 2, 29))
        self.assertEqual((months[0], months[-1], len(months)), ("2023-03", "2024-02", 12))

    def test_aggregation_includes_partial_current_month(self):
        data, now = self.fixture()
        stats = g.aggregate(data, "Pedrowtst", now)
        self.assertEqual(stats["monthly"][-1], {"month": "2026-01", "value": 2})
        self.assertEqual(stats["monthly"][0]["value"], 28)
        self.assertEqual(stats["total"], data["totalContributions"])

    def test_partial_response_rejected(self):
        data, now = self.fixture()
        data["weeks"][0]["contributionDays"].pop()
        data["totalContributions"] -= 1
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            g.aggregate(data, "Pedrowtst", now)

    def test_duplicate_day_rejected(self):
        data, now = self.fixture()
        data["weeks"][0]["contributionDays"].append(data["weeks"][0]["contributionDays"][0])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            g.aggregate(data, "Pedrowtst", now)

    def test_mismatched_total_rejected(self):
        data, now = self.fixture()
        data["totalContributions"] += 1
        with self.assertRaisesRegex(ValueError, "total"):
            g.aggregate(data, "Pedrowtst", now)

    def test_negative_counts_rejected(self):
        data, now = self.fixture()
        data["weeks"][0]["contributionDays"][0]["contributionCount"] = -1
        with self.assertRaises(ValueError):
            g.aggregate(data, "Pedrowtst", now)

    def test_unverified_cache_rejected(self):
        with self.assertRaises(ValueError):
            g.validate_cache({"commits": 231}, "Pedrowtst")

    def test_invalid_fetched_at_rejected(self):
        data, now = self.fixture()
        stats = g.aggregate(data, "Pedrowtst", now)
        stats.update(commits=0, repos=0, languages=[])
        stats["fetched_at"] = "invalid-date"
        with self.assertRaisesRegex(ValueError, "fetched_at"):
            g.validate_cache(stats, "Pedrowtst")

    def test_failed_refresh_preserves_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cache").mkdir()
            (root / "assets").mkdir()
            cache, asset = root / "cache/data.json", root / "assets/hero-dark.svg"
            cache.write_text("verified previous data")
            asset.write_text("previous image")
            with patch.object(liquid, "ROOT", root), patch.object(g, "graphql", side_effect=OSError), patch("sys.argv", ["generate.py", "--refresh"]):
                with self.assertRaises(OSError):
                    liquid.main()
            self.assertEqual(cache.read_text(), "verified previous data")
            self.assertEqual(asset.read_text(), "previous image")

    def test_zero_activity_and_all_svg_variants(self):
        data, now = self.fixture()
        for day in data["weeks"][0]["contributionDays"]:
            day["contributionCount"] = 0
        data["totalContributions"] = 0
        stats = g.aggregate(data, "Pedrowtst", now)
        stats.update(commits=0, repos=0, languages=[])
        for theme in ("dark", "light"):
            for mobile in (False, True):
                for svg in (liquid.render_liquid(stats, theme, mobile),):
                    root = ET.fromstring(svg)
                    self.assertEqual(root.attrib["role"], "img")
                    self.assertIn("<title", svg)
                    self.assertIn("<desc", svg)
                    self.assertNotIn("<script", svg)
                    self.assertNotIn("foreignObject", svg)
                    self.assertNotIn("nan", svg.lower())

    def test_offline_render_does_not_relabel_cache_date(self):
        data, now = self.fixture()
        stats = g.aggregate(data, "Pedrowtst", now)
        stats.update(commits=0, repos=0, languages=[])
        before = copy.deepcopy(stats)
        svg = liquid.render_liquid(g.validate_cache(stats, "Pedrowtst"), "dark")
        self.assertIn("UPDATED 02 JAN 2026", svg)
        self.assertEqual(stats, before)


if __name__ == "__main__":
    unittest.main()
