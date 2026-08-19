# Agent Factory Governance Specification

Status: Current baseline

## Requirements

### Requirement AF-GOV-001 - Approved specification before implementation

The project SHALL require an approved OpenSpec change before implementation work begins.

#### Scenario - Unapproved implementation request

- GIVEN an active change has not received Owner approval
- WHEN an implementation task is requested
- THEN Codex SHALL stop and request approval without modifying implementation files

### Requirement AF-GOV-002 - Safe MVP data

The project SHALL use only synthetic, public, or explicitly approved non-sensitive data during the MVP.

#### Scenario - Sensitive sample data

- GIVEN a dataset contains personal, medical, financial, or confidential information
- WHEN it is proposed for MVP testing
- THEN the dataset SHALL be rejected or replaced with synthetic data

### Requirement AF-GOV-003 - External skill governance

The project SHALL register and review every external skill before import or execution.

#### Scenario - Candidate skill

- GIVEN a useful skill is found in an external repository
- WHEN the skill has no pinned revision, license record, or security scan
- THEN its status SHALL remain `Candidate` and it SHALL NOT be executed

