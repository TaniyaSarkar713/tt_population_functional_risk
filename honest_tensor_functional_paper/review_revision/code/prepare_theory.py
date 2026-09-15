"""Assemble a self-contained technical supplement from the reviewed proofs."""
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];PACKAGE=ROOT.parent

def between_replace(text,start,end,old,new):
    a=text.index(start);b=text.index(end,a) if end else len(text)
    return text[:a]+text[a:b].replace(old,new)+text[b:]

def main():
    old=PACKAGE/'robust_adaptive_extension/paper'
    main=(old/'main.tex').read_text();preamble=main[:main.index(r'\title')]
    preamble=preamble.replace(r'\usepackage[margin=1in]{geometry}',r'\usepackage[margin=0.85in]{geometry}')
    preamble+=r'\emergencystretch=1em'+'\n'
    preamble+=r'\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}'+'\n'
    body=main[main.index(r'\section{Experiment and parameter classes}'):main.index(r'\section{Simulation study}')]
    # Numerical experiments and superseded gap pictures belong to the archive.
    body=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}','',body,flags=re.S)
    body=body.replace(r'; Figure~\ref{fig:theory} displays the corresponding bounds','')
    body=body.replace(r'Figure~\ref{fig:theory} displays the explicit comparisons and the within-class bracket established next.', 'The following benchmark concerns the diagonal observation experiment; the subsequent full-data theorem gives the final rate.')
    body=body.replace('This result does not close the full-data gap in', 'For comparison with the full-data result, consider the preliminary bound in')
    body=body.replace('arbitrary loadings are untreated','general loading results require the additional conditions stated later in this supplement')
    body=body.replace('$D=\\prod', '$D_{\\mathrm{amb}}=\\prod').replace('I_D','I_{D_{\\mathrm{amb}}}')
    body=body.replace('+D\\sigma^2','+D_{\\mathrm{amb}}\\sigma^2').replace('$D=n^K$','$D_{\\mathrm{amb}}=n^K$')
    body=body.replace('overlap $J$ have diagonal inner product $b_s^2J$ but full-tensor inner product $b_s^2J^K$',
                      'overlap $H$ have diagonal inner product $b_s^2H$ but full-tensor inner product $b_s^2H^K$')
    body=body.replace('The principal asymptotic comparison','The fixed-budget benchmark comparison')
    for p in old.glob('*.tex'):
        if p.name in ['main.tex','status.tex','robust_experiments.tex','coverage_table.tex','precision_table.tex','stress_table.tex']:continue
        s=p.read_text()
        if p.name in ['gap_section.tex','gap_proofs.tex']:
            # A single symbol for polynomial degree; no ambient D occurs in these files.
            s=re.sub(r'(?<![A-Za-z\\])D(?![A-Za-z])',lambda m:r'\mathsf d',s)
            s=s.replace('KD',r'K\mathsf d')
            # TeX requires grouping after a subscript if the replacement is a command sequence.
            s=s.replace(r'_\mathsf d',r'_{\mathsf d}').replace(r'^\mathsf d',r'^{\mathsf d}')
        if p.name=='refinements.tex':
            s=s.replace(r'D_{\Tu}',r'C_{\mathrm{diag},\Tu}').replace(r'D_{\TT}',r'C_{\mathrm{diag},\TT}')
            s=s.replace(r'D_\Tu',r'C_{\mathrm{diag},\Tu}').replace(r'D_\TT',r'C_{\mathrm{diag},\TT}')
            s=re.sub(r'(?<![A-Za-z\\])D(?![A-Za-z])',lambda m:r'C_{\mathrm{diag}}',s)
            s=s.replace(r'\mathcal C_{\mathrm{diag}}',r'\mathcal D').replace(r'C_{\mathrm{diag}}_B',r'C_{\mathrm{diag},B}')
            s=between_replace(s,r'\subsection{Noise envelopes',r'\subsection{Finite variance',r'\eta',r'\varepsilon_A')
            s=between_replace(s,r'\subsection{Confidence levels',None,r'\eta',r'\varepsilon_{\mathrm{TV}}')
            s=s.replace(r'c_\varepsilon_{\mathrm{TV}}',r'c_{\varepsilon_{\mathrm{TV}}}')
        if p.name=='robust_adaptive_section.tex':
            s=between_replace(s,r'\subsection{Approximate ranks',r'\subsection{Arbitrary loading',r'\eta',r'\varepsilon_A')
        if p.name=='robust_adaptive_proofs.tex':
            s=between_replace(s,r'\subsection{Proof of Theorem~\ref{thm:approx_sharp}}',r'\subsection{Proof of Proposition~\ref{prop:growing_caps}}',r'\eta',r'\varepsilon_A')
        if p.name=='norm_loading_section.tex':
            s=s[:s.index(r'\paragraph{What remains unresolved.}')]+r'''\paragraph{Scope of the general-loading bounds.}
The displayed envelopes need not match for arbitrary unequal weights. Results L1 and W2 below establish additional small-budget and fixed-decay regimes. Results A1, G2 and P1 separately describe fixed-cap rate adaptation, a growing-outer-class obstruction and strong saturated pointwise inference. General loading profiles and complete pointwise adaptation remain open.
'''
        s=s.replace(r'^\varepsilon_A',r'^{\varepsilon_A}')
        (ROOT/'paper'/p.name).write_text(s)
    header=r'''\title{Technical Supplement: Honest Tensor-Functional Inference}
\author{}\date{Revised September 13, 2026}
\begin{document}\maketitle
This supplement contains the complete supplied proofs supporting the accompanying revised main paper. The main paper states the final central results and empirical findings; this document records the auxiliary comparisons, calibrations, computational contracts and proofs. Fixed-budget intermediate results are retained here as proof ingredients, not as unresolved final rate claims. All formal results have internal status PROVED; this means a checked supplied derivation, not formal verification or external peer review.

The notation is local to each explicit experiment: $D_{\mathrm{amb}}$ is ambient dimension, $\mathsf d$ polynomial degree, $C_{\mathrm{diag}}$ a diagonal-envelope coefficient, $\varepsilon_A$ an approximation allowance and $\eta_k$ a pilot operator bound. The main paper's $q_K=2/K$ is denoted $q$ in scalar-threshold proofs; its $z$-quantile notation (or $z_{\mathrm{val}}$) is used for Gaussian critical values. Canonical complexity $J$ and support overlap $H$ are distinguished.

\tableofcontents
'''
    tail=r'''\appendix
\input{appendix.tex}
\input{full_data_proofs.tex}
\input{refinements.tex}
\input{gap_proofs.tex}
\input{norm_loading_proofs.tex}
\input{robust_adaptive_proofs.tex}
'''
    for stage,name,title in [('certified_weak_signal','certified_results','Optimization contracts, loadings and cap-valid inference'),
                             ('high_dimensional_extension','growing_results','Growing caps, decaying loadings and pointwise inference')]:
        source=(PACKAGE/stage/'theory/results.md').read_text()
        source=source[source.index('Observe '):]
        source=re.sub(r'(?<![A-Za-z\\])D(?![A-Za-z])',lambda m:r'\mathsf d',source)
        source=source.replace('KD',r'K\mathsf d')
        if stage=='certified_weak_signal':
            source=re.sub(r'(?<![A-Za-z\\])q(?![A-Za-z])',lambda m:r'z_{\mathrm{val}}',source)
        else:
            source=between_replace(source,'## P1.',None,'$q=',r'$z_{\mathrm{val}}=')
        source=source.replace(r'_\mathsf d',r'_{\mathsf d}').replace(r'^\mathsf d',r'^{\mathsf d}')
        (ROOT/'theory'/f'{name}.md').write_text(source)
        result=subprocess.run(['pandoc','-f','markdown+tex_math_dollars','-t','latex'],input=source,text=True,capture_output=True,check=True).stdout
        # Keep stable short labels in addition to Pandoc's descriptive labels.
        result=re.sub(r'(\\subsection\{([A-Z]\d+)\..*?\\label\{[^}]+\})',lambda m:m.group(1)+r'\label{sup:'+m.group(2)+'}',result,flags=re.S)
        (ROOT/'paper'/f'{name}.tex').write_text(result)
        tail+=f'\n\\section{{{title}}}\n\\input{{{name}.tex}}\n'
    source=(ROOT/'theory/scalar_companion.md').read_text()
    source=source.replace('**Status: PROVED.**','').replace('# R1. A scalar companion with unconditional risk control','# R1. Scalar companion and risk proof')
    result=subprocess.run(['pandoc','-f','markdown+tex_math_dollars','-t','latex'],input=source,text=True,capture_output=True,check=True).stdout
    result=re.sub(r'(\\label\{[^}]+\})',lambda m:m.group(1)+r'\label{sup:R1}',result,count=1)
    (ROOT/'paper/scalar_companion_proof.tex').write_text(result)
    tail+='\n\\input{scalar_companion_proof.tex}\n\\bibliographystyle{plainnat}\n\\bibliography{references}\n\\end{document}\n'
    (ROOT/'paper/technical_supplement.tex').write_text(preamble+header+body+tail)
    inventory=json.loads((PACKAGE/'independent_review/tables/theorem_inventory.json').read_text())
    statuses=[dict(label=r['label'],title=r['title'],status='PROVED',change='Statement/rate unchanged; reorganized and notation clarified',
                   proof_evidence='Complete supplied derivation and prior 59-result adversarial audit; revision dependency/statement checks',
                   previous_source=r['source']) for r in inventory]
    statuses.append(dict(label='R1',title='Risk-controlled scalar companion',status='PROVED',change='New proposition and complete pathwise/moment proof',proof_evidence='theory/scalar_companion.md'))
    (ROOT/'theory/theorem_status.json').write_text(json.dumps(statuses,indent=2)+'\n')
    print('Assembled 59 reviewed results plus new R1, with explicit proof status.')

if __name__=='__main__':main()
