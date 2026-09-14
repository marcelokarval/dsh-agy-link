# Fork-only installed patch

This directory preserves the exact deployed pnpm patch for dsh-agy-link **0.4.27**. It is intentionally kept on `karval/integrated-corrections`, outside the upstream source PRs. `manifest.json` records source and payload identities; it contains no credentials or machine settings.

A DSH host update is not a plugin update. The currently inspected DSH profile initializer preserves existing package.json, cordis.patch.yml and pnpm-workspace.yaml, but future releases are not guaranteed compatible. Preserve the entire private profile (manifest, lockfile, workspace YAML and patches) separately. Restore this patch declaration under `patchedDependencies` and install the exact package version, rather than copying into node_modules manually.

Do not assume a future dsh-agy-link release includes the fixes just because our PRs exist. On a plugin-version change, review the published source, drop only merged patches, port residual changes, build/test, and prove UI selection -> effective config -> native CLI tool execution. This 0.4.27 patch is NOT a patch for arbitrary later versions.

Run `python3 local/pnpm/verify.py --profile /path/to/dsh/profiles/web --dsh-root /path/to/deepseek-harness` after reinstalls/updates. This is a read-only verification command, NOT an automatically installed updater hook. A changed DSH commit requires a new compatibility proof even if plugin hashes still match.

Private AGY settings (including locally authorized command/read rules), account data and credentials are deliberately NOT in this fork. Back up them privately; the source fork is not a backup of machine configuration.
