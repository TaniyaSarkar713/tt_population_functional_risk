"""Validate complete outputs, vector figures, frozen inputs, and preserved work."""
import hashlib
import json
from pathlib import Path
import pymupdf
from common import ROOT,PROJECT,write_json


def main():
    checks=[]
    def check(label,condition):
        if not condition:raise AssertionError(label)
        checks.append(label)
    audit=json.loads((ROOT/'results/analysis_audit.json').read_text())
    check('analysis_passed',audit['status']=='PASSED')
    check('all_registered_cases',audit['registered_cases']==402)
    check('independent_dataset_count',audit['monte_carlo_data_sets']==1084640)
    check('solver_solves',audit['solver_solves']==2160)
    for suite in range(1,14):
        d=json.loads((ROOT/'logs'/f'run_S{suite:02d}.json').read_text())
        check(f'S{suite:02d}_completed',d['status']=='COMPLETED')
        check(f'S{suite:02d}_sources',all(hashlib.sha256((PROJECT/p).read_bytes()).hexdigest()==h for p,h in d['source_hashes'].items()))
    baseline=json.loads((ROOT/'logs/preserved_stage_hashes.json').read_text())
    check('earlier_files_preserved',all(hashlib.sha256((PROJECT.parent/p).read_bytes()).hexdigest()==h for p,h in baseline.items()))
    pdfs=[ROOT/'report.pdf',ROOT/'manuscript/empirical_sections.pdf']+list((ROOT/'figures').glob('*.pdf'))
    figure_audit=[]
    for p in pdfs:
        check(p.name+'_pdf_signature',p.read_bytes().startswith(b'%PDF'))
        doc=pymupdf.open(p);text=''.join(page.get_text() for page in doc)
        check(p.name+'_nonempty',len(doc)>0 and len(text)>100)
        check(p.name+'_no_unresolved_marker','??' not in text and 'Undefined control sequence' not in text)
        if p.parent.name=='figures':
            images=sum(len(page.get_images()) for page in doc)
            check(p.name+'_vector',images==0)
            fonts=sorted({round(span['size'],2) for page in doc for block in page.get_text('dict')['blocks']
                          if 'lines' in block for line in block['lines'] for span in line['spans']})
            figure_audit.append(dict(file=p.name,pages=len(doc),embedded_images=images,font_sizes=fonts,
                note='Small math superscripts may be below 8pt; base labels/legends are >=8pt at native figure size. Visual inspection recorded separately.'))
    check('ten_vector_figures',len(figure_audit)==10)
    report=(ROOT/'report.md').read_text()
    for word in ['1,084,640','402','2,160','Real-data','midpoint','S13','intermediate']:
        check('report_'+word,word in report)
    diagnostic=json.loads((ROOT/'results/gaussian_diagnostic.json').read_text())
    check('gaussian_direct_regenerated',diagnostic['maximum_center_discrepancy']<1e-8)
    csvs=list((ROOT/'tables').glob('*.csv'))
    check('complete_tables',len(csvs)>=5)
    write_json(ROOT/'results/validation.json',dict(status='PASSED',checks=len(checks),passed=checks,figures=figure_audit,
        limitations='Artifact and numerical validation; not proof of statistical claims. Real-data analysis remains pending.'))
    paths=[p for p in ROOT.rglob('*') if p.is_file() and p.name!='artifact_manifest.json' and '__pycache__' not in p.parts]
    write_json(ROOT/'logs/artifact_manifest.json',{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    print('Passed',len(checks),'artifact checks.')


if __name__=='__main__':main()
