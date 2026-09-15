"""Build review-only deliverables and the complete 50-item guideline crosswalk."""
import re
import subprocess
from inventory import ROOT, dump

TARGETS = {
1:('report.md','Section 1: reconstruction, experiment, target and procedure'),
2:('report.md','Section 1: one-paragraph referee summary'),
3:('report.md','Section 2: statistical contribution and significance'),
4:('assumption_audit.md','Formulation and notation; report Section 1'),
5:('assumption_audit.md','R01–R20 assumption audit with use, standardness, restrictiveness and weakening'),
6:('theorem_audit.md','59 distinct results; statement/proof/novelty/strength/issues and source lines'),
7:('theorem_audit.md','Individual strength judgments; report Section 3 rates'),
8:('report.md','Section 3: matched classes, losses, budgets, logs and constants'),
9:('report.md','Section 4 dependency chains; individual proof reconstructions in theorem audit'),
10:('report.md','Section 4 dependence, nets, doubled ranks, conditioning, measurability and tail checks'),
11:('report.md','Section 4 explicit counterexamples and boundary stress tests; new proof probes'),
12:('report.md','Section 1: mean/functional identifiable, factors need not be'),
13:('report.md','F07 and Section 6: ideal estimator, binary search, polynomial regimes and input size'),
14:('assumption_audit.md','Tuning audit with theoretical/empirical choices and scope'),
15:('simulation_and_claims.md','All suites S01–S13, including separate runtime and follow-ups'),
16:('report.md','Sections 3 and 6: rate slopes, logs, finite-grid curvature and cap rounding'),
17:('simulation_and_claims.md','Pairing, exact baselines, oracles, comparator eligibility, F02/F05/F06'),
18:('report.md','Section 6: Wilson intervals, MCSE, paired differences and simultaneous screening'),
19:('report.md','F02: three-component ablation and concrete controlled replacement'),
20:('report.md','Section 7: no executed real-data analysis; existing applicability audit reviewed'),
21:('report.md','Section 7: no LLM observations used; future sampling/dependence requirements'),
22:('simulation_and_claims.md','Claim-to-evidence classifications and suite conclusions'),
23:('presentation_audit.md','All 14 active manuscript/current-study figures'),
24:('presentation_audit.md','Analytic and empirical tables, precision, uncertainty and comparison classes'),
25:('proposed_abstract.md','Proposed integrated abstract; report Section 8 critique'),
26:('report.md','Section 8 and revision plan: introduction focus and contribution hierarchy'),
27:('report.md','Section 2: focused primary-source novelty comparison, explicit citation-audit boundary'),
28:('assumption_audit.md','Tuning and computation; report Sections 1,5,8 specify missing integrated methods'),
29:('report.md','Sections 3,4,8: main theorem hierarchy and explanatory proof structure'),
30:('report.md','Sections 5,7,8: limitations and stale discussion wording'),
31:('theorem_audit.md','Proof-by-proof audit; presentation/revision plan reorganizes appendix dependencies'),
32:('report.md','F03, Section 3 and claims audit: fixed/growing caps, noise laws, pointwise/risk scope'),
33:('presentation_audit.md','Global notation audit with proposed unifying symbols'),
34:('report.md','Section 6: new checks versus saved evidence; isolated byte-identical rebuild'),
35:('simulation_and_claims.md','Fairness and sensitivity; changed-seed, parameter and noise conclusions delimited'),
36:('revision_plan.md','Three MAJOR, five MODERATE, two MINOR; no CRITICAL established'),
37:('report.md','Summary, substantive strengths, ranked concerns, author questions, revisions and recommendation'),
38:('report.md','Section 9: three explicitly simulated referee perspectives'),
39:('report.md','Section 10: associate-editor assessment and Major revision recommendation'),
40:('report.md','Section 10: six venue fit scores from 1 to 5 and obstacles'),
41:('report.md','Section 2: single strongest contribution sentence'),
42:('report.md','Section 10: single biggest weakness and exact repair'),
43:('simulation_and_claims.md','Current-claim/evidence/too-strong/recommended-wording table'),
44:('revision_plan.md','Six ranked missing-theory recommendations with impact, feasibility and publication relevance'),
45:('revision_plan.md','Seven ranked missing experiments'),
46:('revision_plan.md','Cuts, moves and suggested final organization; presentation figure audit'),
47:('revision_plan.md','P0–P3 action tables with exact source locations and completion criteria'),
48:('report.md','Section 12: final scientific checklist with pending/not-applicable distinctions'),
49:('report.md','C — Major revision required; viable core and concrete remaining corrections'),
50:('README.md','Deliverable index; complete_review.pdf includes all main review and audit documents'),
}

def main():
    guidelines=re.findall(r'^(\d+)\. (.+)$',(ROOT/'review_guidelines.txt').read_text(),re.M)
    assert len(guidelines)==50 and set(TARGETS)==set(range(1,51))
    out=['# Complete guideline coverage',
         'The supplied attachment contains 50 numbered items, including the final deliverable list. All are mapped below. “Addressed” means reviewed, not that the underlying manuscript requirement is satisfied. Real-data/LLM execution is absent and explicitly assessed as such.',
         '| Item | Guideline | Review artifact / evidence |', '|---|---|---|']
    rows=[]
    for n,title in guidelines:
        target,detail=TARGETS[int(n)]
        rows.append(dict(item=int(n),guideline=title,file=target,evidence=detail,status='Addressed'))
        out.append(f'| {n} | {title} | [{detail}]({target}) |')
    (ROOT/'guideline_coverage.md').write_text('\n\n'.join(out[:2])+'\n\n'+'\n'.join(out[2:])+'\n')
    dump(ROOT/'tables/guideline_coverage.json',rows)
    names=['report.md','theorem_audit.md','assumption_audit.md','simulation_and_claims.md',
           'presentation_audit.md','revision_plan.md','proposed_abstract.md','guideline_coverage.md']
    complete='\n\n\\newpage\n\n'.join((ROOT/n).read_text() for n in names)
    (ROOT/'complete_review.md').write_text(complete)
    header=ROOT/'code/pdf_header.tex'
    header.write_text(r'''\usepackage{xurl}
\usepackage{microtype}
\usepackage{fvextra}
\usepackage{needspace}
\setlength{\emergencystretch}{3em}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
\let\oldtexttt\texttt
\renewcommand{\texttt}[1]{{\small\oldtexttt{#1}}}
''')
    for source in ['report.md','complete_review.md']:
        target=source.replace('.md','.pdf')
        args=['pandoc',source,'-o',target,'--pdf-engine=xelatex','--standalone','--toc',
              '-f','markdown+tex_math_dollars+tex_math_single_backslash',
              '-V','geometry:margin=0.8in','-V','fontsize=10pt','-V','colorlinks=true',
              '-V','urlcolor=blue','-V','linkcolor=blue','-V','toc-depth=2','-H',str(header)]
        with (ROOT/'logs'/('build_'+target+'.log')).open('w') as log:
            subprocess.run(args,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        print('Built',target,flush=True)

if __name__=='__main__':main()
