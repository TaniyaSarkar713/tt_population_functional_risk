# Registered follow-ups, 2026-09-13

These additions were specified after inspecting part of the primary run, before executing either addition. The original 351 configurations and their results are preserved; follow-ups use a separate configuration file and new fixed seed streams. The original design, registry and theorem map stay frozen at their execution hashes.

| ID | Reason / question | Fixed design | Interpretation |
|---|---|---|---|
| S12 | The requirements audit found no isolated large-p intermediate-cap sweep | 50 cases: p256..65536, caps1,p^.25,p^.375,sqrt(p),4sqrt(p), M1 orsqrt(p), B5000; common-target sparse diagonal signals | Executable upper intervals and support-oracle performance versus analytic lower bounds; no sharp intermediate-cap rate claim |
| S13 | Unusually low direct Gaussian coverage in original S03_007 | p64, B10000, new fixed stream, exact Gaussian diagonal observations, 90/95/99% levels | Independent calibration check; original low coverage and its uncertainty remain visible |

S12 maps to the robust growing-rank lower bound and high-dimensional G1's general valid upper construction, while retaining the latter's sharpness restriction. S13 maps to the exact Gaussian pivot and implementation calibration, not a new statistical result. Both additions are documented in `logs/deviations.md` before execution. Their results must be distinguished from the initial study.
