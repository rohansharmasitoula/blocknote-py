# Publishing blocknote-py with uv

This guide covers how to build and publish blocknote-py to PyPI using uv.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. **API Tokens**: Generate API tokens:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

3. **uv installed**: Ensure you have uv installed
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## Building the Package

### 1. Update Version

Edit `pyproject.toml`:
```toml
[project]
version = "0.1.0"  # Update this
```

### 2. Build with uv

```bash
# Build both source distribution and wheel
uv build

# Output will be in dist/:
# - blocknote_py-0.1.0.tar.gz (source distribution)
# - blocknote_py-0.1.0-py3-none-any.whl (wheel)
```

### 3. Verify the Build

```bash
# Check the contents
tar -tzf dist/blocknote_py-0.1.0.tar.gz
unzip -l dist/blocknote_py-0.1.0-py3-none-any.whl

# Test installation locally
uv pip install dist/blocknote_py-0.1.0-py3-none-any.whl
python -c "from blocknote.converter import dict_to_blocks; print('Success!')"
```

## Publishing to TestPyPI (Recommended First)

### 1. Configure TestPyPI Token

```bash
# Set environment variable
export UV_PUBLISH_TOKEN="pypi-..."  # Your TestPyPI token
```

Or create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...  # Your TestPyPI token

[pypi]
username = __token__
password = pypi-...  # Your PyPI token
```

### 2. Publish to TestPyPI

```bash
# Using uv (recommended)
uv publish --publish-url https://test.pypi.org/legacy/

# Or using twine
uv pip install twine
uv run twine upload --repository testpypi dist/*
```

### 3. Test Installation from TestPyPI

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ blocknote-py

# Test it works
python -c "from blocknote.converter import dict_to_blocks; print('Success!')"
```

## Publishing to PyPI (Production)

### 1. Final Checks

```bash
# Run all tests
make test

# Run all quality checks
make check-all

# Verify version is correct
grep version pyproject.toml

# Verify CHANGELOG is updated
cat CHANGELOG.md
```

### 2. Build Clean Distribution

```bash
# Clean old builds
make clean
rm -rf dist/

# Build fresh
uv build
```

### 3. Publish to PyPI

```bash
# Using uv (recommended)
export UV_PUBLISH_TOKEN="pypi-..."  # Your PyPI token
uv publish

# Or using twine
uv run twine upload dist/*
```

### 4. Verify Publication

```bash
# Check on PyPI
open https://pypi.org/project/blocknote-py/

# Install from PyPI
pip install blocknote-py

# Test it works
python -c "from blocknote.converter import dict_to_blocks; print('Success!')"
```

## Automated Publishing with GitHub Actions

The repository includes a GitHub Actions workflow that automatically publishes to PyPI when you create a release.

### Setup

1. **Add PyPI Token to GitHub Secrets**:
   - Go to: `https://github.com/rohansharmasitoula/blocknote-py/settings/secrets/actions`
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token

2. **Create a Release**:
   ```bash
   # Tag the release
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

3. **Create GitHub Release**:
   - Go to: `https://github.com/rohansharmasitoula/blocknote-py/releases/new`
   - Choose tag: `v0.1.0`
   - Title: `v0.1.0`
   - Description: Copy from CHANGELOG.md
   - Click "Publish release"

4. **Automatic Publishing**:
   - GitHub Actions will automatically build and publish to PyPI
   - Check progress: `https://github.com/rohansharmasitoula/blocknote-py/actions`

## Complete Release Workflow

### Step-by-Step Process

```bash
# 1. Ensure you're on main branch
git checkout main
git pull origin main

# 2. Update version in pyproject.toml
# Edit: version = "0.1.0"

# 3. Update CHANGELOG.md
# Move items from [Unreleased] to [0.1.0] - 2024-10-09

# 4. Run all checks
make test
make check-all

# 5. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 0.1.0"
git push origin main

# 6. Create and push tag
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# 7. Create GitHub Release (triggers auto-publish)
# Go to GitHub and create release from tag

# 8. Verify publication
pip install blocknote-py
python -c "from blocknote.converter import dict_to_blocks; print('Success!')"
```

## Manual Publishing (Alternative)

If you prefer to publish manually without GitHub Actions:

```bash
# 1. Build the package
uv build

# 2. Publish to TestPyPI first
export UV_PUBLISH_TOKEN="pypi-..."  # TestPyPI token
uv publish --publish-url https://test.pypi.org/legacy/

# 3. Test installation
pip install --index-url https://test.pypi.org/simple/ blocknote-py

# 4. If all good, publish to PyPI
export UV_PUBLISH_TOKEN="pypi-..."  # PyPI token
uv publish

# 5. Verify
pip install blocknote-py
```

## Troubleshooting

### Build Issues

```bash
# Clean everything
make clean
rm -rf dist/ build/ *.egg-info

# Rebuild
uv build
```

### Upload Fails

```bash
# Check token is set
echo $UV_PUBLISH_TOKEN

# Verify package name is available
# Check: https://pypi.org/project/blocknote-py/

# Use verbose mode
uv publish --verbose
```

### Version Conflicts

```bash
# PyPI doesn't allow re-uploading same version
# Bump to next version
# Edit pyproject.toml: version = "0.1.1"
uv build
uv publish
```

### Token Issues

```bash
# Verify token format
# Should start with: pypi-...

# Regenerate token if needed
# PyPI: https://pypi.org/manage/account/token/
```

## Best Practices

1. **Always test on TestPyPI first**
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Update CHANGELOG.md** before each release
4. **Tag releases** in git
5. **Use API tokens** instead of passwords
6. **Keep tokens secure** (use environment variables or secrets)
7. **Verify installation** after publishing
8. **Document breaking changes** clearly

## Security Notes

- **Never commit tokens** to git
- **Use GitHub Secrets** for CI/CD tokens
- **Rotate tokens** periodically
- **Use scoped tokens** (project-specific when possible)
- **Store tokens** in password manager

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## Quick Reference

```bash
# Build
uv build

# Publish to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Publish to PyPI
uv publish

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ blocknote-py

# Install from PyPI
pip install blocknote-py
```
