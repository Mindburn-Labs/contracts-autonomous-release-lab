from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_WORKFLOW = """name: Pull Request Target Containment Probe

on:
  pull_request_target:
    types: [opened, synchronize, reopened]
    branches: [main]
    paths:
      - containment-probes/**

permissions:
  contents: read

jobs:
  candidate-data-only:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout candidate as data
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          path: candidate
          fetch-depth: 1
          persist-credentials: false

      - name: Verify trusted event and data-only checkout
        shell: bash
        env:
          EVENT_NAME: ${{ github.event_name }}
          BASE_REF: ${{ github.event.pull_request.base.ref }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          TRUSTED_SHA: ${{ github.sha }}
          WORKFLOW_REF: ${{ github.workflow_ref }}
        run: |
          set -euo pipefail
          test "$EVENT_NAME" = pull_request_target
          test "$BASE_REF" = main
          test -n "$HEAD_SHA"
          test "$(git -C candidate rev-parse HEAD)" = "$HEAD_SHA"
          test "$TRUSTED_SHA" != "$HEAD_SHA"
          test "$WORKFLOW_REF" = "Mindburn-Labs/contracts-autonomous-release-lab/.github/workflows/pull-request-target-containment.yml@refs/heads/main"
          if git -C candidate config --local --get-regexp '^(credential\\.|http\\..*\\.extraheader)' >/dev/null; then
            echo "::error::Candidate checkout retained Git credentials"
            exit 1
          fi
          sentinel=containment-probes/CONTAINMENT_PROBE_V1.md
          mode="$(git -C candidate ls-files -s -- "$sentinel" | awk 'NR == 1 { print $1 }')"
          test "$mode" = 100644
          for path in candidate candidate/containment-probes "candidate/$sentinel"; do
            test ! -L "$path"
          done
          grep -Fxq 'CONTAINMENT_PROBE_V1' "candidate/$sentinel"
          printf 'trusted_sha=%s candidate_sha=%s\\n' "$TRUSTED_SHA" "$HEAD_SHA"
"""


class PullRequestTargetContainmentTests(unittest.TestCase):
    def test_probe_stays_public_and_data_only(self) -> None:
        workflow = (ROOT / ".github/workflows/pull-request-target-containment.yml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(workflow, EXPECTED_WORKFLOW)
