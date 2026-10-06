---
name: spec-compliance-verification
description: Before and after any task that has explicit rules, check names, or output schemas.
---
- Enumerate every explicit rule and failed-check name before coding.
- Search the workspace and root for README, conventions, config, or schema files that define required formats.
- For each required artifact, confirm it exists and matches the specified schema, types, and naming.
- Run the provided test or validation commands at baseline and after changes.
- If a rule is missing from visible files, do not invent an answer; state the missing convention and apply the most literal interpretation.
- Prefer exact, integer, or canonical representations when the spec says so (e.g., cents, UTC, canonical spelling).
- Re-read the task rules at the end and cross-check each deliverable.