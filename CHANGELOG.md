# Changelog

## [1.0.3] - 2026-06-10

### Fixed
- Optimizer miscompiled even-step loops (e.g. `[++++++]`) as `set_data 0` — only odd steps are safe.
- Optimizer miscompiled `[[-]+]` (infinite loop) as `set_data 0`.
- `.fj` output written with system default encoding instead of UTF-8, crashing the assembler on non-ASCII BF comments.
- Test suite broken on fresh clone due to over-broad `lib/` gitignore rule and missing `.gitattributes`.

### Changed
- Requires Python 3.10–3.14 (dropped 3.8 and 3.9).
- `flipjump` dependency updated to `>=1.3.0,<2.0`; `pytest` to `^9.0.0`.

### Added
- 40 optimizer unit tests covering both miscompilation bugs and edge cases.
- CI matrix testing Python 3.10–3.14 on every push and pull request.
- Known-unsupported programs (self-modifying quine, EOF-reading programs) now marked `xfail` instead of erroring.

## [1.0.2] - 2023-10-13

Initial public release.
