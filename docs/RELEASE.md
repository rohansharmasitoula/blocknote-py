# Release Process

This document describes the process for releasing a new version of blocknote-py.

## Pre-release Checklist

- [ ] All tests pass on all supported Python versions
- [ ] Code coverage is at least 80%
- [ ] All CI/CD checks pass
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated with all changes
- [ ] Version number is bumped in `pyproject.toml`
- [ ] No open critical or high-priority issues

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality (backwards compatible)
- **PATCH** version: Bug fixes (backwards compatible)
 
Examples:
- `0.1.0` → `0.2.0`: New features added
- `0.1.0` → `0.1.1`: Bug fixes only
- `0.1.0` → `1.0.0`: Breaking changes

## Release Steps

### 1. Prepare the Release

```bash
# Ensure you're on main branch and up to date
git checkout main
git pull origin main

# Create a release branch
git checkout -b release/v0.2.0

# Update version in pyproject.toml
# Edit the version field: version = "0.2.0"

# Update CHANGELOG.md
# Move items from [Unreleased] to [0.2.0] - YYYY-MM-DD
```

### 2. Run Final Checks

```bash
# Run all tests
make test

# Run code quality checks
make check-all

# Build the package
make build

# Test the built package locally
uv pip install dist/blocknote_py-0.2.0-py3-none-any.whl
python -c "from blocknote.converter import dict_to_blocks; print('Success!')"
```

### 3. Commit and Push

```bash
# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"

# Push release branch
git push origin release/v0.2.0

# Create and merge PR to main
# Wait for all CI checks to pass
```

### 4. Create GitHub Release

```bash
# After PR is merged, tag the release
git checkout main
git pull origin main
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

On GitHub:
1. Go to Releases → Draft a new release
2. Choose the tag `v0.2.0`
3. Title: `v0.2.0`
4. Description: Copy relevant section from CHANGELOG.md
5. Attach built distributions (optional)
6. Click "Publish release"

### 5. Publish to PyPI

The GitHub Actions workflow will automatically publish to PyPI when a release is created.

Or manually:

```bash
# Build the package
uv build

# Upload to TestPyPI first (optional)
uv run twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ blocknote-py

# Upload to PyPI
uv run twine upload dist/*
```

### 6. Post-release

```bash
# Update main branch for next development cycle
git checkout main
git pull origin main

# Update CHANGELOG.md - add new [Unreleased] section
# Commit
git add CHANGELOG.md
git commit -m "chore: prepare for next development cycle"
git push origin main
```

## Hotfix Release Process

For critical bugs that need immediate release:

```bash
# Create hotfix branch from the release tag
git checkout -b hotfix/v0.2.1 v0.2.0

# Make the fix
# Update version to 0.2.1
# Update CHANGELOG.md

# Commit and tag
git commit -am "fix: critical bug description"
git tag -a v0.2.1 -m "Hotfix release 0.2.1"

# Merge back to main
git checkout main
git merge hotfix/v0.2.1
git push origin main
git push origin v0.2.1

# Create GitHub release and publish
```

## Release Announcement

After publishing:

1. Announce on GitHub Discussions (if enabled)
2. Update project documentation
3. Notify users through appropriate channels
4. Update any related projects or examples

## Rollback Procedure

If a release has critical issues:

1. Yank the release from PyPI:
   ```bash
   uv run twine upload --repository pypi --skip-existing dist/*
   # Contact PyPI support to yank the release
   ```

2. Create a hotfix release with the fix
3. Announce the issue and the fix

## Checklist Template

Copy this for each release:

```markdown
## Release vX.Y.Z Checklist

### Pre-release
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] CI/CD green
- [ ] Docs updated
- [ ] CHANGELOG updated
- [ ] Version bumped

### Release
- [ ] Release branch created
- [ ] Final checks passed
- [ ] PR merged to main
- [ ] Tag created and pushed
- [ ] GitHub release published
- [ ] PyPI published

### Post-release
- [ ] Installation verified
- [ ] Announcement made
- [ ] Next dev cycle prepared
```

## Troubleshooting

### Build Fails

```bash
# Clean build artifacts
make clean

# Rebuild
uv build
```

### PyPI Upload Fails

```bash
# Check credentials
cat ~/.pypirc

# Use token authentication
uv run twine upload --username __token__ --password $PYPI_TOKEN dist/*
```

### Version Conflict

```bash
# Ensure version is unique
# PyPI doesn't allow re-uploading same version
# Bump to next patch version
```
