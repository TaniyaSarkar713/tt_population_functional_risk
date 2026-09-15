"""Issue registry and response matrix for the scientific revision."""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ISSUES=[
('F01','P0','Coverage tolerance counts a genuine miss','empirical_study/code/common.py:66; analyze_results.py:74','REPRODUCIBILITY / SIMULATION','Use bounded ULP comparisons; replay every saved interval and regenerate dependent statistics; exact-noise and scaling regression checks.'),
('F03','P0','No synchronized final submission','robust_adaptive_extension/paper/main.tex and later supplements','NOTATION / STRUCTURE','Assemble a canonical main paper and complete proof supplement after scientific results stabilize; replace obsolete rate figure and claims.'),
('F02','P1','No-bias ablation changes three components','empirical_study/code/tensor_methods.py:92–103','SIMULATION','Run paired isolated bias, fallback and quantile ablations; relabel preserved combined diagnostic.'),
('F04','P1','Interval midpoint has catastrophic rare-fallback loss','high_dimensional_extension/code/methods.py:190–191','METHOD / THEORY','Add a separately defined scalar companion with a uniform risk proof; retain historical midpoint losses and re-evaluate affected saved draws.'),
('F05','P1','Signal sweep changes supplied norm budget','empirical_study/code/run_study.py:89','SIMULATION','Run paired fixed-M sweeps; keep and label norm-comparable prior sweep.'),
('F06','P1','Comparator guarantee type is not applicability','empirical_study/code/run_study.py:138; main.tex:83','METHOD / NOVELTY','Record case-level rank, signal and unverified initialization/alignment status; map implementation to XCH PCA theorem.'),
('F07','P1','Ideal high-dimensional fit versus binary computation','certified C1/C2; high-dimensional W1; S08','METHOD / REPRODUCIBILITY','Explicit method/guarantee table; fixed-loading fixed-tolerance solver experiment; retain all global gaps and numerical limitations.'),
('N01','P1','Focus the distinct tensor likelihood contribution','main Introduction/Related work; novelty matrix','NOVELTY','Compare experiments and mixture likelihoods mathematically; foreground sharp cubic/all-budget theory and avoid firstness claims.'),
('F08','P2','Two calibration refinements lack direct experiments','robust_adaptive_extension/paper/refinements.tex:139,184','SIMULATION','Execute bounded whole-replicate corruption and independent chi-square scale calibration with their actual conditions.'),
('E01','P2','Pointwise precision and finite-grid interpretation','S03/S04 and P1','SIMULATION','Increase independent large-p and transition repetitions; show normalized lengths, cap rounding and raw rare losses.'),
('D01','P2','No justified real-data/LLM application','empirical_study/real_data/README.md','REAL DATA','Retain a theory-led scope unless a defensible repeated-tensor dataset/target is supplied; do not invent an application.'),
('C01','P2','Runtime and memory access models differ','S11/runtime tables','REPRODUCIBILITY','Export full input entries/bytes, measured access, traced allocation and excluded workspace; refresh timing for revised scalar interface.'),
('F09','P3','Scalar losses reused across interval levels without identity','empirical_study/code/common.py:81–96','REPRODUCIBILITY','Attach estimator_id and estimator_alpha to all interval records and separate legacy midpoint diagnostics.'),
('F10','P3','Colliding symbols and historical exposition','all active theory sources','NOTATION / STRUCTURE','Global notation dictionary and consistent main/supplement symbols; move preliminary bounds to technical supplement.'),
('T01','P2','General fixed-cap weak-signal minimax computation','requirements.md','THEORY / METHOD','Assess available contracts and obstacles; keep as a precise open problem if no general proved algorithm is obtained.'),
('T02','P2','Intermediate growing-cap minimax matching','requirements.md; G1/G2','THEORY','State current lower/upper envelopes with uniform constants and tested gap; do not infer missing rates from simulations.'),
('T03','P2','Arbitrary loading profiles beyond matched regimes','requirements.md; L1/W1/W2','THEORY','Preserve small-budget/every-loading and fixed-decay results; delimit unmatched profiles and computational envelope status.'),
('T04','P2','Complete pointwise and TT adaptation theory','requirements.md; A4/P1','THEORY','Explain where saturation/signal/norm conditions enter; add scalar-risk companion without asserting general pointwise sharpness.'),
('T05','P2','Unknown directional scale, dependent replicates and selected loading','assumption audit R09–R19','THEORY / REAL DATA','Execute the available independent-scale refinement; preserve explicit counterexamples and identify unsupported general extensions.'),
]

def main():
    dest=ROOT/'tables/issue_registry.json'
    old={r['id']:r for r in json.loads(dest.read_text())} if dest.exists() else {}
    rows=[]
    for id,priority,concern,location,kind,action in ISSUES:
        r=dict(id=id,severity=priority,review_concern=concern,paper_location=location,scientific_type=kind,
               proposed_action=action,status='NOT RESOLVED',action_taken='',files_changed=[],new_result='',remaining_issue='')
        r.update({k:v for k,v in old.get(id,{}).items() if k in ['status','action_taken','files_changed','new_result','remaining_issue']})
        rows.append(r)
    dest.write_text(json.dumps(rows,indent=2)+'\n')
    with (ROOT/'tables/issue_registry.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    out=['# Complete revision issue registry','Created before scientific edits. Priorities follow the supplied revision protocol; review IDs are preserved. Open research extensions are tracked without treating them as prerequisites for a focused statistical minimax paper.',
         '| ID | Severity | Concern / location | Scientific type | Proposed action | Status |','|---|---|---|---|---|---|']
    for r in rows:out.append('| '+' | '.join([r['id'],r['severity'],r['review_concern']+'; '+r['paper_location'],r['scientific_type'],r['proposed_action'],r['status']])+' |')
    (ROOT/'issue_registry.md').write_text('\n\n'.join(out[:2])+'\n\n'+'\n'.join(out[2:])+'\n')
    print(len(rows),'review concerns registered.')

if __name__=='__main__':main()
