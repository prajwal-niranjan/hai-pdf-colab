# Commits Guide

A specification for writing clear, consistent, and meaningful commit messages.

## Format

```
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

**Examples:**
```
feat(auth): add OAuth2 authentication
fix(api): handle null responses in user endpoint
docs: update installation instructions
```

## Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat: add user profile page` |
| `fix` | Bug fix | `fix: prevent race condition in cache` |
| `docs` | Documentation only | `docs: update API reference` |
| `style` | Formatting, whitespace | `style: run prettier on all files` |
| `refactor` | Code restructuring | `refactor: extract validation logic` |
| `perf` | Performance improvement | `perf: optimize database queries` |
| `test` | Add or modify tests | `test: add unit tests for parser` |
| `chore` | Build, dependencies, tooling | `chore: update webpack to v5` |

## Using Scopes

Scopes provide context about what part of the codebase changed:

```
feat(auth): add password reset flow
fix(database): resolve connection pooling issue
test(api): add integration tests for payments
```

**Define scopes relevant to your project:**
- Module names: `(auth)`, `(payments)`, `(dashboard)`
- Layers: `(api)`, `(ui)`, `(database)`
- Features: `(search)`, `(notifications)`, `(reports)`

## Breaking Changes

Mark breaking changes with `!` or a footer:

```
feat!: remove support for Node 12

BREAKING CHANGE: Node 12 is no longer supported.
Minimum required version is now Node 16.
```

## Writing Good Descriptions

**DO:**
- Use imperative mood: "add feature" not "added feature"
- Be concise but descriptive
- Start with lowercase (after the colon)
- No period at the end

```
✓ feat: add email validation
✗ feat: Added email validation.
✗ feat: email stuff
```

**DON'T:**
- Use vague messages: "fix bug", "update code", "changes"
- Create "checkpoint" or "WIP" commits (use branches/stash instead)
- Commit multiple unrelated changes together

## Body and Footer

Use when you need to explain *why* or provide context:

```
fix(api): handle timeout errors gracefully

Previously, timeout errors would crash the application.
Now they return a 503 status with retry-after header.

Fixes #234
```

**Footer keywords:**
- `Fixes #123` - Links to issue
- `Closes #123` - Closes issue
- `Refs #123` - References issue
- `BREAKING CHANGE:` - Describes breaking change

## Real-World Examples

**Feature addition:**
```
feat(search): implement fuzzy matching algorithm

Adds fuzzy search to improve user experience when typing
queries with minor typos. Uses Levenshtein distance with
configurable threshold.

Closes #156
```

**Bug fix:**
```
fix(auth): prevent token expiration during active sessions

Tokens were expiring while users were actively using the app.
Now automatically refreshes tokens 5 minutes before expiration.

Fixes #892
```

**Performance improvement:**
```
perf(rendering): lazy load images below fold

Reduces initial page load by 40% on average.
Images load as user scrolls down.
```

**Documentation:**
```
docs(api): add examples for webhook endpoints

Added code examples in Python, JavaScript, and cURL
for all webhook event types.
```

**Refactoring:**
```
refactor(validation): extract schema definitions

Moved validation schemas from inline definitions to
separate files for reusability and maintainability.
```

## Benefits

1. **Automated tooling:** Generate changelogs, determine version bumps
2. **Better navigation:** `git log --grep="^feat"` to find all features
3. **Clearer history:** Understand what changed at a glance
4. **Code reviews:** Reviewers immediately understand commit purpose
5. **Team alignment:** Consistent communication across the team

## Anti-Patterns to Avoid

```
✗ checkpoint
✗ WIP
✗ fix stuff
✗ updates
✗ misc changes
✗ fixing the thing
✗ final commit (narrator: it wasn't)
```

## Quick Reference

```bash
# Common patterns
feat: add <feature>
fix: resolve <bug>
docs: update <documentation>
refactor: restructure <component>
test: add tests for <functionality>
chore: update <dependency>

# With scope
feat(module): add <feature>
fix(component): resolve <bug>

# Breaking change
feat!: remove deprecated API
```

## Tools

- **commitlint:** Enforce commit conventions in CI
- **husky:** Run commitlint on git hooks
- **conventional-changelog:** Generate changelogs
- **semantic-release:** Automate versioning

## Configuration Example

`.commitlintrc.json`:
```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"]
    ],
    "scope-case": [2, "always", "lower-case"],
    "subject-case": [2, "always", "lower-case"]
  }
}
```

## Getting Started

1. Share this guide with your team
2. Decide on project-specific scopes
3. Consider adding commitlint to CI
4. Lead by example in code reviews
5. Be patient - consistency develops over time

---

**Remember:** Every commit tells a story. Make it clear, make it meaningful, make it helpful for your future self and teammates.
