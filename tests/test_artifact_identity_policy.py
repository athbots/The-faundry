"""Candidate-level structural checks for FS-SYS-002; not a ratification test."""

import re
import unittest
from pathlib import Path


SPEC = (Path(__file__).resolve().parents[1] / "specifications" /
        "FS-SYS-002-INSTITUTIONAL-ARTIFACT-IDENTITY-AND-NAMING-V0.1.md")


class ArtifactIdentityPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SPEC.read_text(encoding="utf-8")

    def test_candidate_15_core_assertions(self):
        checks = [
            "Document Control ID",
            "Institutional ObjectID",
            "Filesystem Path",
            "Git Commit/Branch",
            "Validation Run ID",
            "Evidence ID",
            "Release ID",
            "Transfer Artifact Name",
            "FS-<DOMAIN>-<NNN>-<DESCRIPTIVE-TITLE>-V<MAJOR>.<MINOR>.<EXT>",
            "integration/<descriptive-purpose>-v<major>.<minor>",
            "Approval, engineering validation, and operational certification",
            "does not define institutional ObjectID semantics",
            "A Git commit proves repository provenance",
            "A transfer archive is a transport artifact",
            "New physical directories MUST NOT be created",
        ]
        self.assertEqual(len(checks), 15)
        for phrase in checks:
            with self.subTest(assertion=phrase):
                self.assertIn(phrase, self.text)
        print("FS-SYS-002 core assertions: 15/15 PASS")

    def test_opaque_name_examples_are_in_an_explicit_prohibition(self):
        naming_section = self.text.split("## 3. Relationship rules", maxsplit=1)[0]
        prohibition = re.search(
            r"Names such as (.*?) MUST NOT be used for controlled artifacts\.",
            naming_section,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(prohibition)
        clause = prohibition.group(1)
        for name in ("final", "new", "tmp", "test2", "candidate-final"):
            with self.subTest(name=name):
                self.assertIn(name, clause)

    def test_supporting_terms_are_present(self):
        self.assertRegex(self.text, re.compile(r"controlled specification", re.IGNORECASE))
        self.assertRegex(self.text, re.compile(r"validation records", re.IGNORECASE))

    def test_candidate_status_and_repository_conflicts_are_explicit(self):
        self.assertIn("CANDIDATE — NOT RATIFIED", self.text)
        self.assertIn("Repository reconciliation observations — open, not resolved", self.text)
        self.assertIn("FD-DOC-005", self.text)
        self.assertIn("PV-G05-G06-MANIFEST.json", self.text)
        self.assertIn("RATIFICATION-DECISION-REQUIRED.md", self.text)
        self.assertIn("No existing repository file, directory, identity semantic, or Genesis G-0.1 record was changed", self.text)


if __name__ == "__main__":
    unittest.main()
