"""One reproduction entry point; sequential timing avoids concurrent workloads."""
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    env=os.environ.copy()
    env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',
               MPLCONFIGDIR='/tmp/tensor-empirical-mpl')
    subprocess.run([sys.executable,str(ROOT/'code/check_implementation.py')],env=env,check=True)
    for suite in [f'S{i:02d}' for i in range(1,11)]:
        print('Starting',suite,flush=True)
        with (ROOT/'logs'/f'{suite}.log').open('w') as log:
            subprocess.run([sys.executable,str(ROOT/'code/run_study.py'),'--suite',suite],
                           env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        print('Completed',suite,flush=True)
    with (ROOT/'logs/S11.log').open('w') as log:
        subprocess.run([sys.executable,str(ROOT/'code/runtime_study.py')],env=env,
                       stdout=log,stderr=subprocess.STDOUT,check=True)
    print('All registered simulation suites and runtime measurements completed.',flush=True)


if __name__=='__main__':main()
