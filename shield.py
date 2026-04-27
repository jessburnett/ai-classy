import os

class AiClassifiedShield:
    def __init__(self):
        self.manifests = {
            "operability": ["justfile", "Makefile", "package.json", "reproduce.sh", "venv", "requirements.txt", "Dockerfile", ".env.example", "SECURITY.md"],
            "regulatory": ["TRANSPARENCY.md", "HITL_POLICY.md", "IMPACT_ASSESSMENT.md", "LICENSE", "PRIVACY.md", "NOTICE", "ETHICS.md", "GOVERNANCE.md", "COMPLIANCE.md"],
            "context": ["README.md", "CONTRIBUTING.md", "ARCHITECTURE.md", "CHANGELOG.md", "ROADMAP.md", "CODE_OF_CONDUCT.md", "SUPPORT.md", "AUTHORS.md", "CITATION.cff"],
            "velocity": ["benchmark.py", "pytest.ini", "tox.ini", "pylintrc", ".github/workflows/ci.yml", "setup.cfg", "pyproject.toml", "MANIFEST.in", "VERSION"]
        }

    def get_results(self, quadrant):
        files = self.manifests.get(quadrant, [])
        results = [{"name": f, "status": "PASS" if os.path.exists(f) else "FAIL"} for f in files]
        score = sum(1 for r in results if r["status"] == "PASS")
        return results, score

    def get_total_score(self):
        total = 0
        for q in self.manifests:
            _, score = self.get_results(q)
            total += score
        return total
