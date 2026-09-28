# Profile maintenance

This is the `Pedrowtst` GitHub profile repository. Keep edits focused on the profile, its generated graphics, and their update workflow.

- Preserve the original liquid-console composition in `generate.py`: authentic embedded Zirtuno mark, waves, droplets, timeline, stat capsules, and three engineering pillars. The user explicitly rejected replacing this with a minimal portfolio header. Refine the original; do not redesign it.
- Put essential content in native Markdown; SVGs supplement it. Preserve theme variants, mobile compositions, alt text, and reduced motion.
- Describe publicly linked projects from their actual code or documentation. Distinguish prototypes from production systems and avoid unsupported benchmarks.
- `generate.py --refresh` retrieves real contribution and repository data through `profile_data.py`. `generate.py` renders the existing verified cache without changing its freshness date.
- Do not invent numbers, relabel contributions as lifetime commits, or expose tokens or private repository details.
- Keep Python dependency-free. Run `python -m unittest discover -s tests -v`, `python generate.py`, and `git diff --check` after generator changes.
- Visually check desktop/mobile and dark/light variants after layout changes. Unit tests alone do not prove rendering on GitHub.
- After publishing, inspect the actual GitHub-rendered README and refresh workflow result. Report evidence precisely.
- Recovery and architecture are documented in `docs/PROFILE.md`. The pre-redesign assets remain recoverable in Git history.
