# Submodule Patches

Local fixes maintained outside the submodule history. The submodule (`lerobot/`)
stays at its upstream commit; patches in this directory are applied on top with
`scripts/apply_patches.sh` and regenerated from the working tree with
`scripts/sync_patches.sh`.

## Layout

```
patches/
  lerobot/
    BASE_COMMIT          # submodule commit the patch is rebased on
    local-fixes.patch    # aggregated diff vs BASE_COMMIT
```

## Workflow

- **After cloning / `git submodule update`** — run `scripts/apply_patches.sh`
  once to reapply local fixes. The script is idempotent: it checks each hunk
  with `git apply --check` first and skips a patch that's already applied.
- **After editing files inside `lerobot/`** — run `scripts/sync_patches.sh` to
  regenerate `local-fixes.patch` from the current submodule working tree.
  Commit the updated patch file in the outer repo.
- **After bumping the submodule** — update `BASE_COMMIT`, rebase the patch by
  hand if it stops applying cleanly, then re-run sync.

## What's in `local-fixes.patch`

- `envs/configs.py` — re-import gym package inside `_make_one` so forkserver
  workers register the namespace.
- `envs/utils.py` — skip `check_env_attributes_and_types` on AsyncVectorEnv
  (probing a missing attr permanently kills the worker).
- `scripts/lerobot_eval.py` — cache task description once before the rollout
  loop instead of calling `env.call("task_description")` every step.
- `policies/factory.py` — fall back to extracting `normalize_*` buffers from
  `model.safetensors` when a legacy HF repo lacks `policy_preprocessor.json`.
- `envs/metaworld.py`, `envs/robotwin.py`, `pyproject.toml` — local env
  integration fixes / extras.
