"""Render current PDF pages for review and reject content outside page bounds."""
import json
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]


def main():
    records=[]
    for name in ['report','technical_supplement']:
        doc=fitz.open(ROOT/'paper'/f'{name}.pdf');violations=[]
        for i,page in enumerate(doc):
            for r in page.get_text('blocks'):
                if r[0]<25 or r[2]>page.rect.width-20 or r[3]>page.rect.height-15:violations.append([i+1,list(r[:4])])
            page.get_pixmap(matrix=fitz.Matrix(.9,.9)).save(str(ROOT/'audit'/f'{name}_page_{i+1}.png'))
        records.append(dict(file=name+'.pdf',pages=len(doc),out_of_bounds_blocks=violations))
    (ROOT/'audit/pdf_layout.json').write_text(json.dumps(records,indent=2)+'\n')
    if any(r['out_of_bounds_blocks'] for r in records):raise AssertionError(records)
    print('All PDF pages are within bounds:',[(r['file'],r['pages']) for r in records])


if __name__=='__main__':main()
