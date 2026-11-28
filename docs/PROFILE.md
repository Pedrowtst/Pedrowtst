# Maintaining this profile

The banner uses Zirtuno’s vector mark, animated water, a monthly contribution chart, and four GitHub statistics. The README links to selected projects and contact information.

## Edit and preview

- `README.md` contains the bio, selected work, and contact links.
- `generate.py` generates the water motion, layouts, and statistics.
- `artwork/` contains the original Zirtuno vector outline, gradients, and surface lighting.
- `profile_data.py`: GitHub GraphQL retrieval, monthly aggregation, and snapshot validation.
- `cache/data.json`: verified, dated contribution snapshot. Never insert example values here.
- `assets/`: dark/light desktop/mobile liquid-console variants. The existing `console-*.svg` filenames remain compatible aliases.

Use Python 3.12 or later. The generator has no third-party dependencies.

```sh
python -m unittest discover -s tests -v
python generate.py
```

An offline render keeps the snapshot's original date. To refresh locally, authenticate with GitHub CLI and run:

```sh
python generate.py --refresh
```

Alternatively provide `GH_TOKEN` or `GITHUB_TOKEN` in the environment. Tokens are never written into assets or the cache. `GH_USERNAME` defaults to `Pedrowtst`. When no token is exported, `profile_data.py` resolves the `gh` executable via `shutil.which` and reuses its local active session.

## What the chart means

The GraphQL `contributionCalendar` supplies daily counts from the first day of the month eleven months before the current month through the retrieval time, in UTC. Days are aggregated into twelve dated calendar months. The current month is always partial. These counts include the contribution types and visibility GitHub exposes to the requesting token; they are neither lifetime commits nor a performance metric. A local personal token and the workflow's repository token can see different totals. The commits capsule uses `totalCommitContributions` over the same period.

The repository count and language mix cover owned, public, non-fork, non-archived repositories, excluding the profile repository. Language percentages use GitHub's code-byte counts across those repositories. They exclude organization-owned work and are not a proficiency score. More than 100 repositories triggers an explicit pagination error rather than publishing partial counts.

The generator verifies daily coverage, unique dates, nonnegative counts, ISO timestamp validity on `fetched_at`, and the total before accepting a response. API failures fail the refresh and leave the previous snapshot and images unchanged. There are no invented fallback values. `fetched_at` records the actual retrieval time; the chart displays its UTC date.

The workflow runs daily at 05:15 UTC, manually, and when generator-related files change. It validates before refreshing, uses the built-in `GITHUB_TOKEN`, limits write permission to the refresh job, and serializes runs. Pull requests run validation without publishing. Generated-only commits do not retrigger the workflow. A conflicting remote push fails safely; rerun the workflow from the latest main.

## Visual checks

Check the rendered profile in light and dark themes. At viewport widths of 900px and below, the chart moves under the figures. The waves and droplets share a 13-second loop. Reduced motion displays the first frame. The dated monthly counts are available in `cache/data.json` and in each SVG’s description.

The Zirtuno and parking descriptions were checked against their public repository documentation. The parking system is an academic local-network prototype using MJPEG camera streaming and laptop-side inference. The backend and protocol experience is retained from the existing profile, without independently verified performance claims. Do not restore unmeasured latency, throughput, zero-data-loss, GPU-inference, or production-deployment claims without supporting evidence.

## Recovery

The previous README, generator, and graphics remain in Git history. Revert the refinement commit to restore them together. To recover from a data refresh failure, keep the last verified cache, fix the API/authentication issue, and rerun the workflow. Do not change the displayed date to hide stale data.

## References

- [GitHub's profile and themed-image formatting](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)
- [GitHub GraphQL contribution calendar](https://docs.github.com/en/graphql/reference/users#contributioncalendar)
