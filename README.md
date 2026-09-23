# Sports Betting QA Assignment

This repository contains the completed QA take-home assignment covering manual testing, defect reporting, UI automation, API validation, and test strategy.

## Repository Structure

- `test_plan.md` – prioritized manual test scenarios
- `execution_results.md` – test execution results and defect reports
- `strategy_and_recommendations.md` – automation rationale and scaling recommendations
- `automation/` – Selenium, Pytest, and API automation framework
- `Evidence/` – screenshots, videos, and automation execution results

## Automation

The assignment includes two automated tests:

1. End-to-end UI validation of a successful single bet.
2. API validation of reset-balance persistence consistency.

See [automation/README.md](automation/README.md) for setup and execution instructions.

## Test Evidence

Supporting screenshots, recordings, and automated execution output are available in the `Evidence` folder.

## Key Findings

Testing identified multiple issues affecting:

- balance consistency
- receipt accuracy
- past-match betting
- input validation
- repeated bet-placement handling
- filtering behavior

Detailed defects and evidence are documented in [execution_results.md](execution_results.md).
