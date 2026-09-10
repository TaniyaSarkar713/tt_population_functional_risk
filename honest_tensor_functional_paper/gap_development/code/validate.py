"""Document/build integrity checks, not an automated mathematical proof audit."""
import hashlib
import json
import platform
import re
from pathlib import Path

import numpy
import pypdf
import scipy

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    prior = ROOT.parent / "theory_review/revised_paper"
    baseline = json.loads((ROOT / "baseline_manifest.json").read_text())
    for name, expected in baseline["sha256"].items():
        require(digest(prior / name) == expected, f"Preserved baseline changed: {name}")

    source = "\n".join(p.read_text() for p in sorted((ROOT / "paper").glob("*.tex")))
    labels = re.findall(r"\\label\{([^}]+)\}", source)
    refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", source)
    require(len(labels) == len(set(labels)), "Duplicate LaTeX labels")
    require(set(refs) <= set(labels), f"Undefined source references: {set(refs)-set(labels)}")
    counts = {kind: len(re.findall(r"\\begin\{" + kind + r"\}", source))
              for kind in ("theorem", "proposition", "lemma", "proof")}
    expected_counts = dict(theorem=11, proposition=10, lemma=7, proof=28)
    require(counts == expected_counts, f"Unexpected statement/proof counts: {counts}")
    require(source.count("Roadmap.") == counts["proof"], "Missing proof roadmap")

    log = (ROOT / "paper/main.log").read_text()
    problems = [line for line in log.splitlines() if re.search(
        r"undefined|Overfull|LaTeX Warning|Package natbib Warning|^!", line)]
    require(not problems, f"Unresolved LaTeX log diagnostics: {problems}")

    pdf_pages = {}
    for name in ("paper/main.pdf", "progress_report.pdf"):
        reader = pypdf.PdfReader(ROOT / name)
        require(len(reader.pages) > 0, f"Empty PDF: {name}")
        require(all(page.extract_text().strip() for page in reader.pages),
                f"A PDF page has no extractable text: {name}")
        pdf_pages[name] = len(reader.pages)

    checked_links = 0
    generated_paths = {ROOT / "results/validation.json", ROOT / "deliverable_manifest.json"}
    for md in ROOT.rglob("*.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md.read_text()):
            if target.startswith(("http:", "https:", "#")):
                continue
            path = target.split("#", 1)[0]
            resolved = (md.parent / path).resolve()
            require(resolved in generated_paths or resolved.exists(),
                    f"Broken link in {md.name}: {target}")
            checked_links += 1

    for name in ("theory_checks.json", "scan_benchmark.json"):
        require(json.loads((ROOT / "results" / name).read_text())["status"] == "PASS",
                f"Unsuccessful recorded check: {name}")

    result = dict(
        status="PASS", check_scope="Document integrity; not mathematical proof verification",
        preserved_baseline_files=len(baseline["sha256"]), statement_counts=counts,
        proof_roadmaps=source.count("Roadmap."), distinct_labels=len(labels),
        checked_local_links=checked_links, pdf_pages=pdf_pages,
        latex_diagnostics=problems,
        environment=dict(python=platform.python_version(), platform=platform.platform(),
                         numpy=numpy.__version__, scipy=scipy.__version__, pypdf=pypdf.__version__),
    )
    (ROOT / "results/validation.json").write_text(json.dumps(result, indent=2) + "\n")
    manifest = {}
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.suffix in {".py", ".tex", ".bib", ".pdf", ".md", ".csv", ".json"}:
            if p.name == "deliverable_manifest.json":
                continue
            manifest[str(p.relative_to(ROOT))] = digest(p)
    (ROOT / "deliverable_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    require(all(p.exists() for p in generated_paths), "Missing generated validation artifact")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
