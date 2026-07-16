# Autonomous Release Conformance Lab

This public repository is a deliberately non-production target for proving the
Mindburn Labs autonomous release permit against real GitHub pull requests.

The default branch is always safe and deterministic. Short-lived test branches
introduce one declared adversarial condition at a time. The organization-level
candidate workflow must reject or deny those branches exactly as specified by
`lab-manifest.json`. No client data, production credentials, deployment targets,
or notification channels belong here.

The lab is evidence, not authority. A passing lab run cannot change an
organization ruleset or mint a production credential.

`pull-request-target-containment.yml` is a public, no-secret probe for GitHub
`pull_request_target` semantics. It reads a declared candidate Markdown
sentinel as data only; it never executes candidate code or writes to GitHub.
