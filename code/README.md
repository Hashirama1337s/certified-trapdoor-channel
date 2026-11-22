# code/

Moki & Julio (AI-assisted) · version 1.0

## In plain words

Two programs make the two ends of the bound, and two more, written by a referee from the definitions, check them separately. Each step below is one command, run from the package root (the folder that holds README.md). Compare each output with the shipped transcript named next to it in transcripts/; they should agree except for the file path printed in a header line and for run times.

## Set-up

An interpreter for Python 3 (3.11 was used) with python-flint (Arb balls), mpmath, NumPy and SciPy; matplotlib for the figure. In the commands below, `python` stands for that interpreter (on Windows, `py -3.11`). No other program is needed. The floor kernel at depth 24 needs about 6.4 GB of memory.

## Files

| file | role |
|---|---|
| `code/floor/cert_backward2.py` | the floor kernel: certified lower bound L_N for a run-length input, with a proven log routine and a written rounding-error bound |
| `code/floor/trapcommon.py` | the input reader and exact helpers imported by the kernel (the kernel imports nothing else of ours) |
| `code/ceiling/verify_collapsed.py` | the ceiling verifier: exact dyadic certificate, 192-bit ball logs rounded upward, Bellman residual in exact integers |
| `code/ceiling/add_claim.py` | writes a copy of a certificate with its claim field set (used to make the claim and negative-control files) |
| `code/referee/ref_ub3_verify.py` | the referee's independent ceiling checker (300-bit interval logs, a different bit order) |
| `code/referee/ref_ub3_bf.py` | the referee's path-by-path brute force of the ceiling bound at small sizes (its outputs are in transcripts/ceiling-referee/) |
| `code/referee/td_ln.py` | the referee's independent exact floor evaluator (integer arithmetic plus 320-bit ball logs) |
| `code/figure/make_gap_history.py` | draws figures/gap_history.png from the milestone values in PAPER.md |

## The certification chain

### Ceiling: C <= 0.574968285761

| step | command | transcript | expected |
|---|---|---|---|
| verify the claim | `python code/ceiling/verify_collapsed.py data/ceiling/cert_col_k15_cont_claim.json` | `transcripts/push1/p3_verify.out` | self-tests PASS; `rho_up (rounded up) = 0.574968285761`; `claimed_rho_upper = 0.574968285761: PASS` |
| negative control (claim one unit lower) | `python code/ceiling/verify_collapsed.py data/ceiling/negctl_k15_cont_low.json` | `transcripts/push1/n1_verify.out` | same computed value; `claimed_rho_upper = 0.574968285760: FAIL (computed rho_up exceeds claim)` |
| independent checker | `python code/referee/ref_ub3_verify.py data/ceiling/cert_col_k15_cont_claim.json` | `transcripts/push1/p3_ref.out` | self-test PASS; `rho_up(ref) 12dp-up = 0.574968285761`, `15dp-up = 0.574968285760847`; claim PASS |
| earlier ceilings | `python code/ceiling/verify_collapsed.py data/milestones/cert_col_k15_sm.json` (likewise `cert_col_k13_ipsym.json`, `cert_col_k11_cvx.json`, `cert_col_k7_from_d8k7.json`) | `transcripts/milestones/` | 0.574968594275 (k = 15 first version), 0.574977689197 (k = 13), 0.575008505468 (k = 11), 0.575232734723 (k = 7). The paper's k = 7 row quotes 0.575232734723 from this file; the original-chain verifier (not shipped) gave 0.575232734724. The k = 11 original-chain certificate and verifier are not shipped either; only their transcript transcripts/milestones/xcheck_verify_u2b_d12k11.log is |

The certificate `data/ceiling/cert_col_k15_cont.json` is the same certificate without its claim field; `data/ceiling/cert_col_k15_cont_claim.json` is the file the verifier passes against the stated bound. `code/ceiling/add_claim.py` makes such a copy: `python code/ceiling/add_claim.py <src.json> <dst.json> <claim>`.

### Floor: C >= 0.57493196741521

| step | command | transcript | expected |
|---|---|---|---|
| kernel at depth 12 (seconds) | `python code/floor/cert_backward2.py data/floor/fL6_10_8_6.txt 12` | `transcripts/push1/cb2_fL6_N12.log` | `CERTIFIED LOWER ENDPOINT: 0.57470129676808` |
| kernel at depth 11 | `python code/floor/cert_backward2.py data/floor/fL6_10_8_6.txt 11` | `transcripts/push1/cb2_fL6_N11.log` | the log's own last lines |
| independent evaluator, depths 10 to 12 (about a minute; L_11 needs level 10 too) | `python code/referee/td_ln.py data/floor/fL6_10_8_6.txt ../out_real.txt --levels 10,11,12` | `transcripts/referee-push1/out_real_L10_12.txt` | the `L_11` and `L_12` lines (0.5745010139654546..., 0.5747012967683128...); our depth-12 endpoint 0.57470129676808 lies below the evaluator's value |
| independent evaluator, perturbed control (one transition changed by 1/100,000) | `python code/referee/td_ln.py data/floor/fL6_pert_644.txt ../out_pert.txt --levels 10,11` | `transcripts/push1b/out_pert_644.txt` | `L_11` moves from 0.57450101396545 to 0.57450101406167 (a shift of 9.6e-11) |
| FULL depth 24 (about 25 minutes, 6.4 GB; re-run from a fresh copy of this package: `transcripts/cleanroom/cleanroom_N24.log`, same endpoint) | `python code/floor/cert_backward2.py data/floor/fL6_10_8_6.txt 24 --nb 15` | `transcripts/floor-lb5/cert_fL6_10_8_6_N24_nb15_lead.log` (identical copy in `transcripts/push1/`); second chunking with `--nb 14` in `transcripts/push1/p1_fL6_N24_nb14.log` | `CERTIFIED LOWER ENDPOINT: 0.57493196741521` |
| milestone: order-9 input at depth 24 (about 15 minutes) | `python code/floor/cert_backward2.py data/milestones/s9_d100000_z0.0005.txt 24` | `transcripts/milestones/cert2_s9_N24.log` | `CERTIFIED LOWER ENDPOINT: 0.57492740773047` |

The expected output of the full job is the transcript named in the table; its last lines are the input sha256, the exact Pr(X != S), the rigorous error bound, and the certified endpoint above.

### Figure

`python code/figure/make_gap_history.py` writes `figures/gap_history.png`.

## Checksums

`MANIFEST.sha256` lists the sha256 of every file. Check with `sha256sum -c MANIFEST.sha256` from the package root. The scripts write nothing into the package unless you name an output file inside it.
