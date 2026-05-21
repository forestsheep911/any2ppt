# AGENTS.md

## Personal Conventions

- When the user refers to a screenshot without attaching it, first check `D:\usr\bxu\Pictures\Screenshots`.
- Prefer the most recently modified image in that directory unless the user specifies another file.
- If multiple recent screenshots are plausible, mention the exact filename you inspected before answering.

## Deckit Release / Upgrade Checklist

When releasing a new Deckit plugin version, do not stop after updating the plugin manifest or pushing code to the `deckit` repo. Users install and upgrade through the marketplace, so the release must include both a git tag in this repo and a marketplace ref update.

1. Update and verify the plugin manifest version:
   - File: `plugins/deckit/.codex-plugin/plugin.json`
   - Check that `"version"` matches the intended release version, for example `0.4.0`.
2. Commit and push all release changes in the `forestsheep911/deckit` repository.
3. Create and push a matching version tag from the release commit:
   - Example: `git tag -a v0.4.0 -m "Release Deckit v0.4.0"`
   - Example: `git push origin v0.4.0`
4. Update the 2water marketplace repository:
   - Repository: `forestsheep911/codex-plugin-marketplace-2water`
   - File: `.agents/plugins/marketplace.json`
   - Deckit entry should keep:
     - `"source": "git-subdir"`
     - `"url": "forestsheep911/deckit"`
     - `"path": "plugins/deckit"`
   - Update only the Deckit source ref to the new tag, for example:
     - `"ref": "v0.4.0"`
5. Commit and push the marketplace change to its `main` branch.
6. Verify both remote references exist:
   - `git ls-remote --tags https://github.com/forestsheep911/deckit.git refs/tags/vX.Y.Z`
   - Check the raw marketplace JSON or GitHub page confirms `"ref": "vX.Y.Z"`.

Lesson learned: if the plugin version is upgraded but the marketplace still points at an older tag, users will not be able to upgrade to the latest version. If the marketplace is changed to a tag that does not exist remotely, installation or upgrade can also fail. Always publish the tag first, then update the marketplace to that tag.
