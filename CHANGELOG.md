# Changelog

## [1.0.3] - 2026-06-10

### Fixed
- **Optimizer miscompilation: even-step zeroing loops** — `[-]`, `[+]`, `[+++]` were correctly
  optimized, but loops with an even non-power-of-2 step (e.g. `[++++++]`, step = 6) were
  wrongly treated as zeroing loops. A loop that adds 6 per iteration can never reach 0 from an
  odd starting value, so it must not be replaced with `set_data 0`.
- **Optimizer miscompilation: nested zeroing loops** — `[[-]+]` (which sets the cell to 1 on
  every iteration and never terminates) was miscompiled as `set_data 0`. The optimizer now
  correctly distinguishes a loop whose body is a prior zeroing-set (`DataSetOp`) from one whose
  body is a plain increment/decrement (`DataAddOp`).
- **Encoding crash on non-ASCII Brainfuck comments** — Compiled `.fj` files are now always
  written as UTF-8 (with `\n` line endings), matching what the FlipJump assembler requires.
  Previously, the system default encoding was used, which crashed the assembler on Windows when
  the Brainfuck source file contained non-ASCII bytes in comments.
- **Test suite broken on a fresh clone** — The `programs/.../bf-source/lib/` corpus was silently
  excluded by a too-broad `lib/` rule in `.gitignore` (now anchored to `/lib/`). The
  `gitattributes.txt` file was renamed to `.gitattributes` and extended with `-text` attributes
  for `*.b`, `*.bf`, `*.fj`, and `programs/**/input|output` to prevent Windows line-ending
  conversion from corrupting byte-exact test fixtures (e.g. quines).

### Changed
- Dropped support for Python 3.8 and 3.9; now requires **Python 3.10–3.14**.
- Updated `flipjump` dependency to `>=1.3.0,<2.0`.
- Updated `pytest` (optional test dependency) to `^9.0.0`.
- Fixed `license` field to use the correct SPDX identifier `BSD-2-Clause`.

### Added
- **40 optimizer unit tests** (`tests/test_optimizer.py`) covering both miscompilation bugs,
  edge cases (`[+-]`, `[++++++]`, `[[-]+]`, `[[-]]`, high-byte comment round-trip), and
  end-to-end compile-and-run verification with and without optimizations.
- **`KNOWN_RUN_FAILURES`** in `tests/test_cases.py`: programs that compile correctly but are
  known to fail at runtime (self-modifying quine, EOF-reading programs) are now marked
  `xfail` instead of erroring.
- **CI test matrix** (`.github/workflows/tests.yml`): runs unit tests and compile-only
  integration tests on Python 3.10–3.14 for every push and pull request.
- **Hardened publish workflow**: replaced the mutable third-party `JRubics/poetry-publish`
  action with the official `pypa/gh-action-pypi-publish` action pinned to a specific commit
  SHA, eliminating a supply-chain risk.

## [1.0.2] - 2023-10-13

Initial public release on PyPI.
