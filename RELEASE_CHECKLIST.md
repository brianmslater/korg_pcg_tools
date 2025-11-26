# Release Checklist

Checklist for preparing PCG Tools Python for public release on GitHub.

## Pre-Release Verification

### Documentation
- [x] README.md updated and accurate
- [x] QUICKSTART.md updated
- [x] INSTALL.md complete for all platforms
- [x] SIMPLE_EDITOR_GUIDE.md complete
- [x] FEATURE_COMPARISON.md created
- [x] PROJECT_STRUCTURE.md created
- [x] KNOWN_ISSUES.md updated
- [x] CONTRIBUTING.md present
- [ ] CHANGELOG.md updated with v1.1.0
- [ ] LICENSE file present and correct

### Code Quality
- [x] Simple Setlist Editor working
- [x] Hardware tested on Kronos
- [x] No syntax errors
- [x] Writer code confirmed working
- [ ] CLI commands tested
- [ ] Example scripts working
- [ ] All imports resolve correctly

### Repository Structure
- [x] Clean root directory
- [x] Development files in archive/ (gitignored)
- [x] Session notes in dev_notes/ (gitignored)
- [x] Documentation in docs/
- [x] Examples in examples/
- [x] No sensitive data in repo
- [x] No large binary files tracked

### Files to Review
- [ ] .gitignore complete
- [ ] requirements.txt accurate
- [ ] setup.py functional
- [ ] Launcher scripts executable
- [ ] No broken symlinks

## Release Preparation

### Version Information
- [ ] Update version in setup.py
- [ ] Update version in README.md
- [ ] Update version in CHANGELOG.md
- [ ] Update version in simple_setlist_editor.py
- [ ] Tag release in git

### GitHub Setup
- [ ] Repository name decided
- [ ] Repository description written
- [ ] Topics/tags selected
- [ ] README renders correctly on GitHub
- [ ] License badge added
- [ ] Status badges added (if desired)

### Release Notes
- [ ] Create RELEASE_NOTES.md for v1.1.0
- [ ] Highlight hardware testing
- [ ] List new features
- [ ] Document known limitations
- [ ] Include upgrade instructions

## Testing Before Release

### Installation Testing
- [ ] Test on clean Windows system
- [ ] Test on clean macOS system
- [ ] Test on clean Linux system
- [ ] Verify all dependencies install
- [ ] Test launcher scripts

### Functionality Testing
- [ ] Simple Setlist Editor launches
- [ ] Can open PCG files
- [ ] Can edit setlist names
- [ ] Can edit slot properties
- [ ] Can save files
- [ ] Recent files work
- [ ] Window position saves
- [ ] CLI commands work
- [ ] Report generation works

### Documentation Testing
- [ ] All links in README work
- [ ] All cross-references resolve
- [ ] Installation instructions work
- [ ] Examples run without errors

## Post-Release

### Announcement
- [ ] Post to Korg Forums
- [ ] Post to relevant subreddits
- [ ] Announce on social media (if applicable)
- [ ] Update any existing threads

### Monitoring
- [ ] Watch for issues
- [ ] Respond to questions
- [ ] Track feature requests
- [ ] Monitor stars/forks

### Follow-up
- [ ] Create GitHub Issues for known limitations
- [ ] Set up project board (optional)
- [ ] Plan next release features
- [ ] Update documentation based on feedback

## Critical Items (Must Complete)

1. **CHANGELOG.md** - Document v1.1.0 changes
2. **Test CLI** - Verify all commands work
3. **Test Installation** - Fresh install on each platform
4. **Release Notes** - Clear, comprehensive notes
5. **GitHub Description** - Compelling project description

## Nice to Have

- [ ] Screenshots in README
- [ ] Demo video/GIF
- [ ] GitHub Actions for CI/CD
- [ ] Automated tests
- [ ] Code coverage badge
- [ ] Contributing guidelines expanded

## Blockers

Issues that MUST be resolved before release:

- None currently identified

## Notes

- Simple Setlist Editor is the main feature - emphasize this
- Hardware testing is a key differentiator
- Be clear about what's NOT implemented (vs C# version)
- Point users to C# version for missing features
- Emphasize reliability over feature completeness

---

**Target Release Date**: TBD
**Version**: 1.1.0
**Status**: In Preparation
