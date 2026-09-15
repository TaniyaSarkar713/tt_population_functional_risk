"""Validate review completeness, evidence identities, PDF layout and source preservation."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote
import fitz
from inventory import ROOT, PROJECT, PACKAGE, dump

def main():
    checks=[];failures=[]
    def check(name,value):
        checks.append(name)
        if not value:failures.append(name)
    def read(name):return json.loads((ROOT/name).read_text())
    inv=read('tables/theorem_inventory.json');audit=read('tables/theorem_audit.json')
    check('59_distinct_results',len(audit)==len(inv)==59 and len({r['label'] for r in audit})==59)
    check('all_result_labels_audited',{r['label'] for r in audit}=={r['label'] for r in inv})
    for r in audit:
        check(r['id']+'_all_audit_fields',all(r.get(k) for k in ['correct_statement','proof_complete','proof_audit','novelty','strength_and_issue']))
        lines=(PROJECT/r['source']).read_text().splitlines()
        check(r['id']+'_source_line',r['label'] in '\n'.join(lines[r['line']-1:r['line']+3]))
    cross=read('tables/guideline_coverage.json')
    check('all_50_guidelines',{r['item'] for r in cross}==set(range(1,51)))
    for r in cross:check('guideline_'+str(r['item'])+'_artifact',(ROOT/r['file']).exists())
    report=(ROOT/'report.md').read_text()
    found=re.findall(r'^### (F\d+) — (MAJOR|MODERATE|MINOR): (.+)$',report,re.M)
    check('10_classified_findings',len(found)==10)
    check('severity_counts',[sum(s==v for _,s,_ in found) for v in ['MAJOR','MODERATE','MINOR']]==[3,5,2])
    check('consistent_verdict','C — Major revision required' in report and 'Recommendation: **Major revision' in report)
    evidence={
        'F01':[('empirical_study/code/common.py','1e-11 * max(1., abs(target))'),
               ('empirical_study/code/analyze_results.py','tolerance=1e-11*max(1.,abs(target))')],
        'F02':[('empirical_study/code/tensor_methods.py','Omit only bias and fallback'),
               ('empirical_study/code/tensor_methods.py','qa=norm.isf(alpha/2)')],
        'F03':[('robust_adaptive_extension/paper/main.tex','general unseparated rank adaptation remain open'),
               ('robust_adaptive_extension/paper/main.tex','absence of actual-rank adaptation'),
               ('robust_adaptive_extension/paper/norm_loading_section.tex','What remains unresolved.')],
        'F04':[('high_dimensional_extension/code/methods.py','lo = hi = 0.'),
               ('empirical_study/code/tensor_methods.py','if lo>hi:lo=hi=0.')],
        'F05':[('empirical_study/code/run_study.py','M=max(np.sqrt(p)*tau,1.1*np.linalg.norm(A),np.linalg.norm(A)+tau)')],
        'F06':[('empirical_study/code/run_study.py','asymptotic_regular_signal')],
        'F07':[('empirical_study/figures/captions.md','not formal interval arithmetic'),
               ('high_dimensional_extension/theory/results.md','statistical')],
        'F08':[('robust_adaptive_extension/paper/refinements.tex',r'\label{prop:mom}'),
               ('robust_adaptive_extension/paper/refinements.tex',r'\label{prop:variance}')],
        'F09':[('empirical_study/code/run_study.py','Midpoint of the 95% interval; no general MSE theorem asserted.')],
        'F10':[('robust_adaptive_extension/paper/gap_section.tex',r'\label{thm:low_degree}')],
    }
    findings=[]
    for id,severity,title in found:
        locations=[]
        for name,quote in evidence[id]:
            source=(PACKAGE/name).read_text();offset=source.find(quote)
            check(id+'_quote_'+name+'_'+quote,offset>=0)
            locations.append(dict(source='honest_tensor_functional_paper/'+name,
                                  line=source[:offset].count('\n')+1,exact_excerpt=quote))
        findings.append(dict(id=id,severity=severity,title=title,locations=locations))
    dump(ROOT/'tables/findings.json',findings)
    raw=read('results/raw_results_audit.json');proof=read('results/proof_checks.json');probe=read('results/implementation_probes.json')
    check('60496_raw_checks',raw['checks']==60496 and raw['status']=='PASSED' and not raw['failures'])
    check('1377_proof_checks',proof['checks']==1377 and proof['status']=='PASSED' and not proof['failures'])
    check('3444_rows_318_stochastic',raw['summary_rows']==3444 and raw['stochastic_cases']==318)
    check('26_strict_policy_differences',len(raw['strict_coverage_differences'])==26)
    miss=probe['oracle_tolerance']['records']
    check('exact_genuine_oracle_miss',len(miss)==1 and miss[0]['trial']==41 and miss[0]['exact_noise_miss'] and miss[0]['miss_distance']>10000*miss[0]['ulp'])
    check('9_binary_grid_checks',len(probe['binary_outer_grid_checks'])==9 and all(r['passed'] for r in probe['binary_outer_grid_checks']))
    check('saved_empirical_reproduction',read('results/reproduction.json')['status']=='PASSED')
    presentation=read('results/presentation_checks.json')
    check('forced_integrated_build',presentation['isolated_latex_build']['exit_code']==0)
    check('14_vector_figures',len(presentation['figures'])==14 and all(x['embedded_raster_images']==0 for x in presentation['figures']))
    check('no_label_or_key_errors',not any(presentation[k] for k in ['duplicate_labels','missing_reference_labels','missing_bib_keys']))
    check('lexical_scan_zero',read('tables/style_scan.json')==[])
    pdfs=[]
    for name in ['report.pdf','complete_review.pdf']:
        d=fitz.open(ROOT/name);outside=[];margin=[]
        for i,page in enumerate(d):
            for b in page.get_text('dict')['blocks']:
                for line in b.get('lines',[]):
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        if min(x0,y0)<0 or x1>page.rect.width+1 or y1>page.rect.height+1:outside.append((i+1,span['text']))
                        if x0<44 or x1>page.rect.width-44:margin.append((i+1,span['text']))
        text='\n'.join(p.get_text() for p in d)
        check(name+'_layout',not outside and not margin)
        check(name+'_text_integrity','\ufffd' not in text and 'Major revision required' in text)
        pdfs.append(dict(file=name,pages=len(d),outside_page_spans=outside,margin_violations=margin))
    broken=[]
    for p in ROOT.glob('*.md'):
        for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('http:','https:','#')):continue
            target=unquote(target.split('#')[0]).strip('<>')
            if not (p.parent/target).exists():broken.append(dict(source=p.name,target=target))
    check('review_local_links',not broken)
    baseline=read('logs/input_hashes.json');changed=[];missing=[]
    for name,sha in baseline.items():
        p=PROJECT/name
        if not p.exists():missing.append(name)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=sha:changed.append(name)
    check('1469_baseline_files',len(baseline)==1469)
    check('research_files_preserved',not missing and set(changed)=={'README.md','requirements.md'})
    result=dict(status='PASSED' if not failures else 'FAILED',checks=len(checks),failures=failures,
        baseline_files=len(baseline),unchanged_baseline_files=len(baseline)-len(changed)-len(missing),
        intentional_root_documentation_changes=changed,missing_files=missing,pdfs=pdfs,broken_links=broken,
        theorem_results=59,guideline_items=50,findings_by_severity={'CRITICAL':0,'MAJOR':3,'MODERATE':5,'MINOR':2},
        scope='Review-artifact consistency and preservation checks; not theorem verification or correction of preserved research findings.')
    dump(ROOT/'results/review_validation.json',result)
    print(json.dumps(result,indent=2))
    if failures:raise AssertionError(failures)

if __name__=='__main__':main()
