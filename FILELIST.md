# FILELIST

Moki & Julio (AI-assisted) · version 1.0

## In plain words

Every file in this package: what it is for, where it came from in the working folder, and whether it was changed on the way ("yes": see PATCHES.md), copied byte for byte ("no"), or written for this release ("new"). `MANIFEST.sha256` holds the checksum of every file listed here.

101 files listed here, plus `MANIFEST.sha256` itself.

| file | purpose | source | changed |
|---|---|---|---|
| `CITATION.cff` | citation metadata | new | new |
| `FILELIST.md` | this list | new | new |
| `LICENSE` | CC BY 4.0 licence text | Y56 conic-records release (CC BY 4.0 text, unchanged) | new |
| `LICENSE-CODE` | MIT licence for code/ | MIT text from the same release; coverage list rewritten | new |
| `PAPER.md` | the write-up (refereed text; file paths adjusted) | release/PAPER.md | yes |
| `PATCHES.md` | every change made to a copied file | new | new |
| `README.md` | front page | new | new |
| `bars/AMENDMENT-PUSH1a.md` | sealed test file | AMENDMENT-PUSH1a.md | no |
| `bars/AMENDMENT-PUSH1b.md` | sealed test file | AMENDMENT-PUSH1b.md | no |
| `bars/BAR-LB1.md` | sealed test file | BAR-LB1.md | no |
| `bars/BAR-LB2.md` | sealed test file | BAR-LB2.md | no |
| `bars/BAR-LB3.md` | sealed test file | BAR-LB3.md | no |
| `bars/BAR-LB4.md` | sealed test file | BAR-LB4.md | no |
| `bars/BAR-PUSH1.md` | sealed test file | BAR-PUSH1.md | no |
| `bars/BAR-UB1.md` | sealed test file | BAR-UB1.md | no |
| `bars/BAR-UB2.md` | sealed test file | BAR-UB2.md | no |
| `bars/BAR-UB3.md` | sealed test file | BAR-UB3.md | no |
| `bars/RESULT-LB1.md` | scoring note for a sealed test | RESULT-LB1.md | no |
| `bars/RESULT-LB2.md` | scoring note for a sealed test | RESULT-LB2.md | no |
| `bars/RESULT-LB3.md` | scoring note for a sealed test | RESULT-LB3.md | no |
| `bars/RESULT-LB4.md` | scoring note for a sealed test | RESULT-LB4.md | no |
| `bars/RESULT-UB1.md` | scoring note for a sealed test | RESULT-UB1.md | no |
| `bars/RESULT-UB2.md` | scoring note for a sealed test | RESULT-UB2.md | no |
| `bars/RESULT-UB3.md` | scoring note for a sealed test | RESULT-UB3.md | no |
| `bars/SEALS-LB2.txt` | hashes of the seals | SEALS-LB2.txt | no |
| `bars/SEALS-LB3.txt` | hashes of the seals | SEALS-LB3.txt | no |
| `bars/SEALS-LB4.txt` | hashes of the seals | SEALS-LB4.txt | no |
| `bars/SEALS-UB2.txt` | hashes of the seals | SEALS-UB2.txt | no |
| `bars/SEALS-UB3.txt` | hashes of the seals | SEALS-UB3.txt | no |
| `code/README.md` | one command per step, with expected output | new | new |
| `code/ceiling/add_claim.py` | ceiling verifier (code) | fixes/add_claim.py | no |
| `code/ceiling/verify_collapsed.py` | ceiling verifier (code) | build-ub3/verify_collapsed.py | no |
| `code/figure/make_gap_history.py` | figure script (code) | new | new |
| `code/floor/cert_backward2.py` | floor kernel (code) | build-lb3/cert_backward2.py | no |
| `code/floor/trapcommon.py` | floor kernel (code) | build-lb2/trapcommon.py (identical to build-lb3/trapcommon.py) | no |
| `code/referee/ref_ub3_bf.py` | referee's independent checker (code) | referee/ub3/ref_ub3_bf.py | no |
| `code/referee/ref_ub3_verify.py` | referee's independent checker (code) | referee/ub3/ref_ub3_verify.py | no |
| `code/referee/td_ln.py` | referee's independent checker (code) | referee/push1/td_ln.py | no |
| `data/ceiling/cert_col_k15_cont.json` | ceiling certificate or control | build-ub4/certs/cert_col_k15_cont.json | no |
| `data/ceiling/cert_col_k15_cont_claim.json` | ceiling certificate or control | runs/push1/cert_col_k15_cont_claim.json | no |
| `data/ceiling/negctl_k15_cont_low.json` | ceiling certificate or control | runs/push1/negctl_k15_cont_low.json | no |
| `data/floor/fL6_10_8_6.txt` | floor input (rational probabilities) | build-lb5/fL6_10_8_6.txt | no |
| `data/floor/fL6_pert_644.txt` | floor input (rational probabilities) | runs/push1b/fL6_pert_644.txt | no |
| `data/milestones/cert_col_k11_cvx.json` | earlier milestone certificate or input | build-ub3/certs/cert_col_k11_cvx.json | no |
| `data/milestones/cert_col_k13_ipsym.json` | earlier milestone certificate or input | build-ub4/certs/cert_col_k13_ipsym.json | no |
| `data/milestones/cert_col_k15_sm.json` | earlier milestone certificate or input | build-ub3/certs/cert_col_k15_sm.json | no |
| `data/milestones/cert_col_k7_from_d8k7.json` | earlier milestone certificate or input | build-ub3/certs/cert_col_k7_from_d8k7.json | no |
| `data/milestones/s9_d100000_z0.0005.txt` | earlier milestone certificate or input | build-lb3/s9_d100000_z0.0005.txt | no |
| `figures/gap_history.png` | figure | new | new |
| `proofs/ERROR-LEMMA2-FIX.md` | written proof | build-lb3/ERROR-LEMMA2-FIX.md | no |
| `proofs/ERROR-LEMMA2.md` | written proof | build-lb3/ERROR-LEMMA2.md | no |
| `proofs/PROOF-COLLAPSE-FIXES.md` | written proof | fixes/PROOF-COLLAPSE-FIXES.md | no |
| `proofs/PROOF-COLLAPSE.md` | written proof | build-ub3/PROOF-COLLAPSE.md | no |
| `proofs/PROOF-LB1-ADDENDUM-AUTOMATON.md` | written proof | PROOF-LB1-ADDENDUM-AUTOMATON.md | no |
| `proofs/PROOF-LB1.md` | written proof | PROOF-LB1.md | no |
| `proofs/PROOF-UB1.md` | written proof | PROOF-UB1.md | no |
| `referees/REFEREE-LB1.md` | referee report | REFEREE-LB1.md | yes |
| `referees/REFEREE-LB3.md` | referee report | REFEREE-LB3.md | yes |
| `referees/REFEREE-LB4.md` | referee report | REFEREE-LB4.md | no |
| `referees/REFEREE-PAPER1.md` | referee report | REFEREE-PAPER1.md | yes |
| `referees/REFEREE-UB1.md` | referee report | REFEREE-UB1.md | no |
| `referees/REFEREE-UB3.md` | referee report | REFEREE-UB3.md | yes |
| `references/NOTES-UB4.md` | builder's working note (not refereed) | build-ub4/NOTES.md | yes |
| `transcripts/ceiling-referee/bf.out` | program transcript cited by PAPER.md | referee/ub3/bf.out | no |
| `transcripts/ceiling-referee/run_big.out` | program transcript cited by PAPER.md | referee/ub3/run_big.out | yes |
| `transcripts/ceiling-referee/run_small.out` | program transcript cited by PAPER.md | referee/ub3/run_small.out | yes |
| `transcripts/ceiling-referee/their_verifier_rerun.out` | program transcript cited by PAPER.md | referee/ub3/their_verifier_rerun.out | yes |
| `transcripts/floor-lb5/cert_fL6_10_8_6_N24_nb15_lead.log` | program transcript cited by PAPER.md | build-lb5/cert_fL6_10_8_6_N24_nb15_lead.log | no |
| `transcripts/milestones/cert2_s9_N24.log` | program transcript cited by PAPER.md | build-lb3/cert2_s9_N24.log | no |
| `transcripts/milestones/verify_conv_d8k7.log` | program transcript cited by PAPER.md | build-ub3/logs/verify_conv_d8k7.log | no |
| `transcripts/milestones/verify_cvx_k11.log` | program transcript cited by PAPER.md | build-ub3/logs/verify_cvx_k11.log | no |
| `transcripts/milestones/verify_k13_ipsym.log` | program transcript cited by PAPER.md | build-ub4/logs/verify_k13_ipsym.log | no |
| `transcripts/milestones/verify_k15_claim.out` | program transcript cited by PAPER.md | fixes/verify_k15_claim.out | no |
| `transcripts/milestones/verify_k15_cont.log` | program transcript cited by PAPER.md | build-ub4/logs/verify_k15_cont.log | no |
| `transcripts/milestones/verify_k15_negctl.out` | program transcript cited by PAPER.md | fixes/verify_k15_negctl.out | no |
| `transcripts/milestones/verify_sm_k15.log` | program transcript cited by PAPER.md | build-ub3/logs/verify_sm_k15.log | no |
| `transcripts/milestones/xcheck_verify_u2b_d12k11.log` | program transcript cited by PAPER.md | build-ub3/logs/xcheck_verify_u2b_d12k11.log | no |
| `transcripts/push1/cb2_fL6_N11.log` | program transcript cited by PAPER.md | runs/push1/cb2_fL6_N11.log | no |
| `transcripts/push1/cb2_fL6_N12.log` | program transcript cited by PAPER.md | runs/push1/cb2_fL6_N12.log | no |
| `transcripts/push1/cert_fL6_10_8_6_N24_nb15_lead.log` | program transcript cited by PAPER.md | runs/push1/cert_fL6_10_8_6_N24_nb15_lead.log | no |
| `transcripts/push1/n1_verify.out` | program transcript cited by PAPER.md | runs/push1/n1_verify.out | no |
| `transcripts/push1/p1_fL6_N24_nb14.log` | program transcript cited by PAPER.md | runs/push1/p1_fL6_N24_nb14.log | no |
| `transcripts/push1/p3_ref.out` | program transcript cited by PAPER.md | runs/push1/p3_ref.out | no |
| `transcripts/push1/p3_verify.out` | program transcript cited by PAPER.md | runs/push1/p3_verify.out | no |
| `transcripts/push1b/out_pert_644.txt` | program transcript cited by PAPER.md | runs/push1b/out_pert_644.txt | no |
| `transcripts/push1b/run_pert.log` | program transcript cited by PAPER.md | runs/push1b/run_pert.log | no |
| `transcripts/referee-push1/out_iid_L10_12.txt` | program transcript cited by PAPER.md | referee/push1/out_iid_L10_12.txt | no |
| `transcripts/referee-push1/out_iid_probe.txt` | program transcript cited by PAPER.md | referee/push1/out_iid_probe.txt | no |
| `transcripts/referee-push1/out_null2_live.txt` | program transcript cited by PAPER.md | referee/push1/out_null2_live.txt | no |
| `transcripts/referee-push1/out_null_N2_L10_11.txt` | program transcript cited by PAPER.md | referee/push1/out_null_N2_L10_11.txt | no |
| `transcripts/referee-push1/out_real_L10_12.txt` | program transcript cited by PAPER.md | referee/push1/out_real_L10_12.txt | no |
| `transcripts/referee-push1/out_real_probe.txt` | program transcript cited by PAPER.md | referee/push1/out_real_probe.txt | no |
| `transcripts/referee-push1/run_null.log` | program transcript cited by PAPER.md | referee/push1/run_null.log | no |
| `transcripts/referee-push1/run_real.log` | program transcript cited by PAPER.md | referee/push1/run_real.log | no |
| `.gitattributes` | tells git to store every file byte for byte (no line-ending conversion), so checksums survive a clone | written for this release | new |
| `bars/RESULT-PUSH1.md` | scoring of the sealed test BAR-PUSH1 and its amendments | RESULT-PUSH1.md (paths changed to package paths) | new |
| `transcripts/cleanroom/cleanroom_N24.log` | the depth-24 floor re-run from a fresh copy of this package, following code/README.md | written for this release | new |
| `.zenodo.json` | metadata for the Zenodo archive of this release | written for this release | new |
| `brand/doi.svg` | DOI badge | written for this release | new |
| `brand/licence.svg` | licence badge | lab house style | new |
| `brand/lab.svg` | lab map badge | lab house style | new |
