# PATCHES

Moki & Julio (AI-assisted) · version 1.0

## In plain words

Most files in this package are byte-for-byte copies of the files our computations produced. A few copies had to be changed before release, because they named folders on the machine where they ran, or carried a time of day. Every such change is listed here, with the sha256 of the original so the original can be identified. Sources stay untouched in the working folder: everything was copied, nothing moved or deleted. Source paths in FILELIST.md are relative to the working folder.

## No code was changed

All seven programs under `code/` (`cert_backward2.py`, `trapcommon.py`, `verify_collapsed.py`, `add_claim.py`, `ref_ub3_verify.py`, `ref_ub3_bf.py`, `td_ln.py`) are byte-identical to their sources; this was checked with a byte comparison. The kernel imports `trapcommon` from its own folder, so both sit together in `code/floor/`, and every command in `code/README.md` runs from the package root with no path fix. The only program written for this release is `code/figure/make_gap_history.py` (new).

## Path and time redactions (text copies)

Rules applied to the copies: (a) the working-folder prefix of the project was removed, leaving a path relative to the working folder (`<prefix>build-ub3/certs/x.json` became `build-ub3/certs/x.json`); (b) the full path of the lab's memory-cap wrapper was shortened to `memcap.py`; (c) a time of day was removed from one date stamp. The original strings are not reproduced. Lines are line numbers in the original file, which are also the line numbers in the shipped file (no line was added or removed).

| shipped file | original sha256 | lines changed | rule |
|---|---|---|---|
| `referees/REFEREE-LB1.md` | `4c2343880a27f07654911d8ba431d01f9a29f90ddf5e96ac8aabaa63f77a8f0f` | 3 | (a) |
| `referees/REFEREE-LB3.md` | `605c85b11753c2be97c56a9162d2165617eb521406198f1c0978ae078b06dcca` | 66 | (a) |
| `referees/REFEREE-PAPER1.md` | `7649f6c6764e5923d1a719481e06840809a5347f2869eb70dd0ad2fb6727ecaf` | 1 | (c) |
| `referees/REFEREE-UB3.md` | `92d564bce00dcc2d69811b795d1ab4ce61e53d9d7f80afc941423820435b2c6d` | 5 | (a) |
| `references/NOTES-UB4.md` | `2e0493d0adc1dd7c65c6e7a4e9007f33bf74c008b043fed39460a8e3fbe050aa` | 41, 225, 226, 227, 230 | (a), (b) |
| `transcripts/ceiling-referee/run_big.out` | `800e64f740f92ec365e1f95f4435f3756bcef36f4626269281b76a622074c3bd` | 2, 4, 6, 8 | (a) |
| `transcripts/ceiling-referee/run_small.out` | `a81fe1d1934448519be1825461a5cef60b56687073ed2a69099018e62814f069` | 3, 5, 7 | (a) |
| `transcripts/ceiling-referee/their_verifier_rerun.out` | `a2a515f4e000da734077be207c64fe211ec713530e600fbc926137e01460887d` | 2, 7, 12, 17 | (a) |

No other transcript, log, bar, certificate or input needed a change. Paths that were already relative to the working folder (for example the input path `input/fL6_10_8_6.txt` in the referee's transcript headers, or `../../runs/push1/...` in `transcripts/push1/p3_ref.out`) were left as printed: they name no machine and are part of the verbatim transcript. They do not match the package layout; the table in `code/README.md` gives the package paths. The sealed files in `bars/` are byte-identical to the sealed versions.

## PAPER.md

`PAPER.md` is the refereed text with only file paths adjusted to the package layout. Original sha256 of the source: `4dd0e916a15a94cdcb05d494924a71a9ab4c13e7bec6d73c4a8c0d2a7c39ae9d`. Changes, all in file paths or file names (no number, claim or sentence of argument changed):

1. Section 2: `PROOF-LB1.md` and `PROOF-LB1-ADDENDUM-AUTOMATON.md` now carry the prefix `proofs/`.
2. Section 2: `fL6_10_8_6.txt` now `data/floor/fL6_10_8_6.txt`.
3. Section 2: `REFEREE-LB4` now `referees/REFEREE-LB4.md`.
4. Section 3: `build-ub3/PROOF-COLLAPSE.md` now `proofs/PROOF-COLLAPSE.md`; `fixes/PROOF-COLLAPSE-FIXES.md` now `proofs/PROOF-COLLAPSE-FIXES.md`; `REFEREE-UB3` now `referees/REFEREE-UB3.md`.
5. Section 3 table: the two certificate file names now carry `data/ceiling/`.
6. Section 6: `build-ub4/NOTES.md` now `references/NOTES-UB4.md`.
7. "Files and reproduction": the floor and ceiling commands now use the package paths (`code/floor/...`, `data/floor/...`, `code/ceiling/...`, `data/ceiling/...`); the sentence on sealed tests and referee reports points at `bars/`, `referees/`, `transcripts/` and `code/README.md`, and one clause was added: 'every transcript the numbers above come from: transcripts/; the step-by-step commands: code/README.md' (later narrowed, see below).

The status line was changed at the source to 'Version 1.0.' before copying. After the release referee: in 'Files and reproduction' the clause on transcripts was narrowed to what the transcripts hold, and in section 6 the floor is quoted as 0.5749319 (at the source too).

## Notes that are not patches

- `references/NOTES-UB4.md` is the ceiling builder's working note, copied because PAPER.md section 6 cites it. It is not refereed, and its run commands name the working-folder layout (not the package layout); one of its sentences (an exact k = 13 solve "not run") predates the k = 13 solve reported in PAPER.md.
- `transcripts/floor-lb5/cert_fL6_10_8_6_N24_nb15_lead.log` and `transcripts/push1/cert_fL6_10_8_6_N24_nb15_lead.log` are two copies of one log (byte-identical).
- `data/floor/fL6_10_8_6.txt` is the one copy of the floor input; the referee's own copy of the same file (identical bytes) is not duplicated.
- The k = 7 ceiling row: see code/README.md (earlier ceilings) and PAPER.md section 3.
