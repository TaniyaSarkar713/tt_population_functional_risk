"""Stream the full UCI archive; do not extract untrusted archive paths."""
import argparse, gzip, hashlib, io, json, re, tarfile, time, zipfile
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CONDITIONS=['S1 obj','S2 match','S2 nomatch']
CLIPS=[50.,100.,200.]

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def main(archive):
    start=time.perf_counter(); rows=[]; tensors=[]; ids=[]; counts=[]; channels=None; trial_manifest=[]
    archive=Path(archive)
    provenance={'url':'https://archive.ics.uci.edu/static/public/121/eeg+database.zip',
                'citation':'Begleiter, H. (1995). EEG Database. UCI Machine Learning Repository. DOI:10.24432/C5TS3D',
                'license':'CC BY 4.0','archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
                'raw_cache':str(archive),'subjects':[]}
    with zipfile.ZipFile(archive) as z:
        for name in ['eeg.html','eeg.data.html','eeg.full.html']:
            (ROOT/'real_data'/name).write_bytes(z.read(name))
        names=sorted(n for n in z.namelist() if n.startswith('eeg_full/') and n.endswith('.tar.gz'))
        for si,name in enumerate(names):
            subject=Path(name).name[:-7]; payload=z.read(name)
            totals=np.zeros((3,3,64,16)); ns=np.zeros(3,int); seen=set(); exclusions=Counter()
            nclip=np.zeros(3,dtype=np.int64); nvalues=0; members=0; maxima=0.
            with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as t:
                for member in t:
                    if not member.isfile(): continue
                    members+=1; raw=t.extractfile(member).read(); reason=None; cond=None
                    rec={'subject':subject,'file':member.name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
                    try:
                        if raw[:2]==b'\x1f\x8b': raw=gzip.decompress(raw)
                        s=raw.decode('ascii'); lines=s.splitlines()
                        if not s.strip(): raise ValueError('empty')
                        header='\n'.join(lines[:4])
                        if re.search(r'\berr\b',header,re.I): raise ValueError('error_flag')
                        cond=next((j for j,c in enumerate(CONDITIONS) if re.search(r'^# '+re.escape(c)+r'\s*,',s,re.M)),None)
                        if cond is None: raise ValueError('unknown_condition')
                        mt=re.search(r', trial (\d+)',header)
                        trial=int(mt.group(1)) if mt else -1
                        if trial < 0: raise ValueError('missing_trial_identifier')
                        if trial in seen: raise ValueError('duplicate_trial')
                        current=re.findall(r'^# (\S+) chan (\d+)\s*$',s,re.M)
                        ch=[c for c,i in current]
                        if len(ch)!=64 or len(set(ch))!=64 or [int(i) for c,i in current]!=list(range(64)):
                            raise ValueError('channel_schema')
                        # Read all four columns, including labels and sample indices, to
                        # reject reordered, repeated, or incomplete measurements.
                        a=np.loadtxt(io.StringIO(s),dtype={'names':['trial','channel','sample','voltage'],
                                    'formats':['i4','U4','i4','f8']})
                        if a.shape!=(64*256,) or not np.isfinite(a['voltage']).all(): raise ValueError('shape_or_nonfinite')
                        if not np.array_equal(a['sample'],np.tile(np.arange(256),64)) or not np.all(a['trial']==trial):
                            raise ValueError('sample_or_trial_schema')
                        if not np.array_equal(a['channel'],np.repeat(ch,256)): raise ValueError('channel_data_mismatch')
                        if 'CZ' not in ch or 'PZ' not in ch: raise ValueError('missing_primary_channel')
                        if channels is None: channels=ch
                        if set(ch)!=set(channels): raise ValueError('inconsistent_channel_set')
                        a=a['voltage'].reshape(64,256)[[ch.index(c) for c in channels]]
                        seen.add(trial); ns[cond]+=1; nvalues+=a.size; maxima=max(maxima,float(np.max(np.abs(a))))
                        for j,bound in enumerate(CLIPS):
                            nclip[j]+=np.count_nonzero(np.abs(a)>bound)
                            totals[j,cond]+=np.clip(a,-bound,bound).reshape(64,16,16).mean(axis=2)
                    except (ValueError,UnicodeError,EOFError,OSError) as e:
                        reason=str(e); exclusions[reason]+=1
                    rec.update(condition=CONDITIONS[cond] if cond is not None else None,status=reason or 'included')
                    trial_manifest.append(rec)
            eligible=bool(np.all(ns>0))
            record={'subject':subject,'group_code':subject[3],'archive_sha256':hashlib.sha256(payload).hexdigest(),
                    'archive_bytes':len(payload),'trial_files':members,'valid_trials':int(ns.sum()),'condition_counts':ns.tolist(),
                    'excluded_trials':dict(exclusions),'eligible':eligible,'voltage_values':nvalues,
                    'clipped_counts':nclip.tolist(),'max_absolute_voltage':maxima}
            provenance['subjects'].append(record)
            if eligible:
                ids.append(subject); counts.append(ns); tensors.append(totals/ns[None,:,None,None])
            if (si+1)%10==0: print(f'Processed {si+1}/{len(names)} subjects; {len(ids)} eligible',flush=True)
    np.savez_compressed(ROOT/'real_data/subject_tensors.npz',tensors=np.stack(tensors),subjects=np.array(ids),
                        condition_counts=np.stack(counts),channels=np.array(channels),clips=np.array(CLIPS),conditions=np.array(CONDITIONS))
    provenance['processing_seconds']=time.perf_counter()-start
    provenance['eligible_subjects']=len(ids);provenance['trial_file_count']=len(trial_manifest)
    provenance['trial_status_counts']=dict(Counter(r['status'] for r in trial_manifest))
    (ROOT/'real_data/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    with (ROOT/'real_data/trial_manifest.jsonl').open('w') as f:
        for r in trial_manifest: f.write(json.dumps(r)+'\n')
    (ROOT/'real_data/deviations.md').write_text('''# Schema observations and deviations

No outcome-driven changes to the locked protocol. Trial files are gzip members inside subject tar.gz archives inside the downloaded zip; they are streamed without path extraction. Actual sample indices 0--255 govern parsing, despite legacy headers mentioning 416 samples. All 64 recorded channels are retained for the tensor demonstration, including auxiliary labels X, Y, and nd; the primary contrast uses CZ and PZ only. Error notices, malformed records, and missing conditions are handled by the prespecified rules. The full archive contains fewer usable files than 122 times 120; the actual manifest is authoritative. The downloaded raw archive remains in an external temporary cache; the repository preserves its checksum, all subject/trial checksums, parser, source metadata, and compact derived tensors. Reproduction of parsing requires downloading that public archive again if the temporary cache is removed.
''')
    print(json.dumps({k:provenance[k] for k in ['eligible_subjects','trial_file_count','trial_status_counts','processing_seconds']},indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');main(p.parse_args().archive)
