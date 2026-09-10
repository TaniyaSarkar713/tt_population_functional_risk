"""Validate review artifacts, references, original-file preservation and build state."""
from pathlib import Path
import hashlib,json,re,sys,subprocess,platform
import numpy,scipy,pypdf
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"input_manifest.json").read_text())
original={name:hashlib.sha256((ROOT.parent/"paper"/name).read_bytes()).hexdigest()==sha
          for name,sha in manifest["input_sha256"].items()}
assert all(original.values()),original
srcs=[ROOT/"revised_paper"/name for name in
      ["main.tex","appendix.tex","full_data_section.tex","full_data_proofs.tex",
       "refinements.tex","status.tex"]]
source="\n".join(p.read_text() for p in srcs)
labels=re.findall(r"\\label\{([^}]+)\}",source)
refs=re.findall(r"\\(?:eqref|ref)\{([^}]+)\}",source)
assert not set(refs)-set(labels)
assert len(labels)==len(set(labels))
counts={k:len(re.findall(r"\\begin\{"+k+r"\}",source))
        for k in ["theorem","proposition","lemma","proof"]}
assert counts==dict(theorem=8,proposition=7,lemma=7,proof=22),counts
roadmaps=source.count(r"\emph{Roadmap.}")
assert roadmaps==22,roadmaps
log=(ROOT/"revised_paper/main.log").read_text()
warnings=re.findall(r".*(?:Warning|Overfull|Underfull).*",log)
assert not warnings,warnings
terms=["innovative","pioneering","revolutionary paradigm","transformative framework",
"superior","surpass","excel","remarkable","unprecedented","achieves SOTA",
"breakthrough performance","general-purpose","is capable of","notably","yet",
"yielding","at its essence","encompass","differentiate","reveal","underscore",
"exhibit superior capability","exceed","pave the way for","highlight the potential of",
"profound challenges","stems from","rigid","impede"]
banned={t:source.lower().count(t.lower()) for t in terms if t.lower() in source.lower()}
assert not banned,banned
assert "—" not in source
bad_tables=[]
bad_links=[]
for p in ROOT.glob("*.md"):
    expected=None
    for no,line in enumerate(p.read_text().splitlines(),1):
        if not line.startswith("|"):
            expected=None
            continue
        n=len(re.split(r"(?<!\\)\|",line))-1
        if expected is None:expected=n
        if n!=expected:bad_tables.append([p.name,no,expected,n])
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",p.read_text()):
        if target.startswith(("https:","http:","#")):continue
        target=target.split("#",1)[0]
        if not (p.parent/target).exists():bad_links.append([p.name,target])
assert not bad_tables,bad_tables
assert not bad_links,bad_links
results=json.loads((ROOT/"results/audit_checks.json").read_text())
assert results["status"]=="PASS"
pdfs={str(p.relative_to(ROOT)):len(pypdf.PdfReader(p).pages)
      for p in [ROOT/"input_snapshot/main.pdf",ROOT/"revised_paper/main.pdf",ROOT/"report.pdf"]}
assert pdfs["input_snapshot/main.pdf"]==22
out=dict(status="PASS",original_files_unchanged=original,named_result_counts=counts,
         proof_roadmaps=roadmaps,pdf_pages=pdfs,duplicate_labels=[],missing_source_labels=[],
         final_latex_warnings=warnings,banned_substrings=banned,unicode_em_dashes=0,
         markdown_table_errors=bad_tables,broken_local_links=bad_links,
         numeric_checks=results["status"])
(ROOT/"results/source_audit.json").write_text(json.dumps(out,indent=2)+"\n")
versions=dict(python=sys.version,platform=platform.platform(),numpy=numpy.__version__,
              scipy=scipy.__version__,pypdf=pypdf.__version__)
for cmd in ["pdflatex","xelatex","pandoc","latexmk"]:
    result=subprocess.run([cmd,"--version" if cmd!="latexmk" else "-v"],
                          capture_output=True,text=True,check=True)
    versions[cmd]=result.stdout.strip().splitlines()[:3]
(ROOT/"results/environment.json").write_text(json.dumps(versions,indent=2)+"\n")
# A manifest for deliverable source and PDF artifacts, excluding volatile build products.
paths=[p for p in ROOT.rglob("*") if p.is_file() and
       (p.suffix in {".md",".tex",".bib",".py",".pdf",".csv"} or p.name=="audit_checks.json")]
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(paths)}
(ROOT/"results/deliverable_manifest.json").write_text(json.dumps(hashes,indent=2)+"\n")
print(json.dumps(out,indent=2))
