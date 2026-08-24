# Automated Travel Proposal PoC v1 - Spec Delta

## ADDED Requirements

### Requirement: ATP-101 - Synthetic structured travel request

The PoC SHALL accept only synthetic travel requests that conform to a versioned canonical schema and contain no real passenger, customer, credential, payment, loyalty, passport, booking, or PNR data.

#### Scenario: Valid synthetic request

- GIVEN a request contains synthetic origin, destination, dates, traveler counts, budget, preferences, constraints, currency, and language
- WHEN intake validation runs
- THEN the request SHALL receive a pseudonymous `request_id`
- AND SHALL be eligible for read-only planning

#### Scenario: Required field is missing

- GIVEN destination, dates, traveler count, or currency is missing or invalid
- WHEN intake validation runs
- THEN provider search SHALL NOT start
- AND the system SHALL return focused clarification questions

#### Scenario: Real or sensitive data is supplied

- GIVEN a request contains a real name, contact detail, passport, loyalty number, payment detail, booking reference, PNR, credential, or other personal or confidential value
- WHEN intake validation runs
- THEN the PoC SHALL reject or redact the value according to the approved test policy
- AND SHALL NOT send the value to a provider or model

### Requirement: ATP-102 - Allow-listed read-only provider adapters

The PoC SHALL route searches only through versioned, allow-listed adapters for approved non-production provider environments and SHALL expose no booking or mutation operation.

#### Scenario: Approved flight test adapter

- GIVEN `Duffel Test` has been separately approved and configured for the PoC
- WHEN a valid synthetic flight request is executed
- THEN the flight adapter SHALL invoke only approved search or offer-read operations
- AND SHALL label every returned record `environment=test`

#### Scenario: Approved hotel evaluation adapter

- GIVEN `Hotelbeds Evaluation` has been separately approved and configured for the PoC
- WHEN a valid synthetic hotel request is executed
- THEN the hotel adapter SHALL invoke only approved availability, rate-check, or content-read operations
- AND SHALL label every returned record `environment=evaluation`

#### Scenario: Mutation operation is requested

- GIVEN a workflow attempts `book`, `order`, `hold`, `payment`, `cancel`, `refund`, `ticket`, `PNR`, `message`, or another external mutation
- WHEN policy enforcement evaluates the operation
- THEN the operation SHALL be denied before any provider call
- AND the denial SHALL be recorded in minimized audit evidence

#### Scenario: Unapproved provider is selected

- GIVEN a request targets Travel Booster, Amadeus, Google Travel, SerpApi, Expedia, Skyscanner, Booking.com, Production, or another provider not approved for this PoC
- WHEN adapter selection runs
- THEN the request SHALL fail closed
- AND SHALL identify the missing approval without requesting a credential

### Requirement: ATP-103 - Canonical evidence normalization

The PoC SHALL normalize provider results into versioned `FlightOfferEvidence` and `HotelOfferEvidence` records without discarding source identity, test-environment status, currency, timestamps, restrictions, or missing fields.

#### Scenario: Flight evidence is normalized

- GIVEN an approved provider returns a flight offer
- WHEN the adapter maps the response
- THEN the canonical record SHALL include provider, provider offer reference, environment, searched-at timestamp, expiry when supplied, currency, total amount, itinerary segments, duration, stops, included baggage when supplied, and raw-evidence reference

#### Scenario: Hotel evidence is normalized

- GIVEN an approved provider returns a hotel result
- WHEN the adapter maps the response
- THEN the canonical record SHALL include provider, provider property and rate references, environment, searched-at timestamp, currency, total amount, stay dates, room and board information when supplied, cancellation summary when supplied, and raw-evidence reference

#### Scenario: Material field is missing

- GIVEN a provider result lacks currency, total amount, travel dates, source identity, or environment identity
- WHEN normalization runs
- THEN the result SHALL NOT be represented as a complete priced option
- AND the missing fields SHALL remain explicit rather than inferred

#### Scenario: Provider response contains instructions

- GIVEN a provider field contains text that attempts to change policy, call another tool, reveal a secret, or override system instructions
- WHEN normalization runs
- THEN the text SHALL be treated as untrusted data
- AND SHALL NOT alter workflow policy or permissions

### Requirement: ATP-104 - Evidence-bound ranking and itinerary planning

The PoC SHALL rank only normalized eligible evidence against the explicit synthetic request and SHALL distinguish provider facts, deterministic calculations, planner assumptions, and unsupported information.

#### Scenario: Eligible alternatives are available

- GIVEN at least two eligible flight or hotel options satisfy mandatory constraints
- WHEN ranking runs
- THEN the PoC SHALL provide a deterministic score breakdown for material criteria
- AND SHALL preserve at least one reasonable alternative when available

#### Scenario: No option satisfies mandatory constraints

- GIVEN normalized options exist but none satisfies a mandatory budget, date, traveler, or routing constraint
- WHEN planning runs
- THEN the PoC SHALL state that no eligible option was found
- AND SHALL NOT silently relax the constraint

#### Scenario: POI evidence is unavailable

- GIVEN Google Places, Google Routes, or another live POI source is not approved
- WHEN a daily itinerary is generated
- THEN the PoC SHALL use only the approved synthetic destination fixture
- AND SHALL label the itinerary content as synthetic test content

#### Scenario: Evidence is insufficient

- GIVEN provider evidence or approved fixture evidence cannot support a material recommendation
- WHEN the draft is prepared
- THEN the PoC SHALL omit the unsupported claim or return `INSUFFICIENT_EVIDENCE`
- AND SHALL NOT answer from model memory as if the fact were verified

### Requirement: ATP-105 - Traceable Hebrew proposal draft

The PoC SHALL produce a Hebrew draft for agent review in which every priced option is traceable to normalized evidence and every non-provider assumption is visibly labeled.

#### Scenario: Complete draft

- GIVEN eligible evidence supports a travel proposal
- WHEN the PoC generates the draft
- THEN the draft SHALL include request summary, selected flight and hotel options, daily itinerary, alternatives, estimated total, assumptions, exclusions, source references, search timestamps, and agent-review status

#### Scenario: Test price is displayed

- GIVEN a price originated in a test or evaluation environment
- WHEN it appears in the draft
- THEN it SHALL be marked `מחיר ניסוי - לא למכירה`
- AND SHALL include currency, provider, search time, and availability disclaimer

#### Scenario: Currency conversion is unavailable

- GIVEN options use multiple currencies and no approved conversion source and timestamp are available
- WHEN the total is prepared
- THEN the PoC SHALL present separate currency totals
- AND SHALL NOT invent or silently apply an exchange rate

#### Scenario: Draft is requested in another language

- GIVEN the PoC language scope is Hebrew-only
- WHEN another output language is requested
- THEN the PoC SHALL state the PoC language limitation
- AND SHALL NOT silently produce an untested commercial draft

### Requirement: ATP-106 - Human review and zero external side effects

The PoC SHALL terminate at a reviewable draft and SHALL require a later separately approved workflow before any external message, booking, payment, publication, or account-changing action.

#### Scenario: Agent receives a draft

- GIVEN a proposal draft is complete
- WHEN the workflow finishes
- THEN the draft SHALL be marked `DRAFT / AGENT REVIEW REQUIRED`
- AND no external recipient SHALL receive it

#### Scenario: User asks to send the proposal

- GIVEN a user asks the PoC to email, WhatsApp, publish, or otherwise send the draft
- WHEN policy enforcement evaluates the request
- THEN the PoC SHALL refuse the action
- AND SHALL identify that a dedicated approved channel change is required

#### Scenario: User asks to book an option

- GIVEN a user asks the PoC to reserve, hold, order, ticket, pay, or cancel
- WHEN policy enforcement evaluates the request
- THEN the PoC SHALL refuse before any external call
- AND SHALL retain only minimized denial evidence

### Requirement: ATP-107 - Quota, cost, and financial gates

The PoC SHALL enforce approved request, provider-call, retry, model-usage, and monetary ceilings before execution and SHALL treat missing or stale cost data as unknown rather than zero.

#### Scenario: Provider quota is available

- GIVEN a separately approved execution stage defines a remaining daily request allowance
- WHEN a provider call is planned
- THEN the workflow SHALL reserve one call against the stage allowance before execution
- AND SHALL record the measured result after execution

#### Scenario: Evaluation quota would be exceeded

- GIVEN the next Hotelbeds Evaluation call would exceed the approved daily or stage ceiling
- WHEN orchestration evaluates the call
- THEN the call SHALL be blocked
- AND the draft SHALL expose partial-results status

#### Scenario: Billing is required

- GIVEN a provider, Google Cloud project, or model configuration requires enabling Billing, adding Payment, or accepting paid overage
- WHEN the PoC reaches that step
- THEN work SHALL stop for explicit Owner financial approval
- AND SHALL NOT enable Billing or create a payment method

#### Scenario: Retry is considered

- GIVEN a read-only provider call fails transiently
- WHEN retry policy evaluates the failure
- THEN at most the separately approved retry count SHALL be attempted
- AND each retry SHALL count toward provider and cost ceilings

### Requirement: ATP-108 - Provider failure and partial-result behavior

The PoC SHALL handle provider timeout, malformed response, empty result, rate limit, authentication failure, and unavailability without fabricating offers or hiding degraded coverage.

#### Scenario: One provider fails

- GIVEN one approved provider fails and another returns eligible evidence
- WHEN the draft is prepared
- THEN the PoC MAY produce a partial draft
- AND SHALL name the unavailable category and coverage limitation

#### Scenario: All providers fail

- GIVEN all required provider searches fail or return no eligible evidence
- WHEN planning runs
- THEN the PoC SHALL return a no-result fallback
- AND SHALL NOT produce a priced recommendation

#### Scenario: Authentication fails

- GIVEN a provider returns an authentication or authorization error
- WHEN the error is handled
- THEN the workflow SHALL stop calls to that provider for the request
- AND logs SHALL record only the credential reference and error category, never the secret value

#### Scenario: Malformed or unexpected schema

- GIVEN a provider response cannot be validated against the pinned adapter schema
- WHEN normalization runs
- THEN the response SHALL be quarantined from ranking
- AND adapter drift SHALL be raised for Owner review

### Requirement: ATP-109 - Tenant isolation, secrets, and minimized audit

The PoC SHALL isolate configuration, credentials, evidence, caches, logs, quotas, and evaluations per tenant and environment, even though the first PoC uses one synthetic tenant.

#### Scenario: Synthetic tenant execution

- GIVEN an approved PoC stage runs for tenant `travel-poc-synthetic`
- WHEN adapters, planner, or audit components access state
- THEN they SHALL use only that tenant and the approved non-production environment

#### Scenario: Foreign tenant reference appears

- GIVEN evidence, cache, credential reference, or configuration belongs to another tenant
- WHEN validation runs
- THEN the request SHALL fail closed
- AND foreign content SHALL NOT appear in output or logs

#### Scenario: Secret handling

- GIVEN a future approved stage creates provider credentials
- WHEN the workflow uses them
- THEN secrets SHALL remain in the environment credential store
- AND SHALL NOT appear in Git, OpenSpec, prompts, screenshots, exports, logs, or draft output

#### Scenario: Audit event is recorded

- GIVEN an intake decision, provider call, policy denial, normalization result, ranking decision, fallback, or draft completion occurs
- WHEN audit evidence is written
- THEN it SHALL include `tenant_id`, `request_id`, pseudonymous `actor_id`, `agent_release_id`, action, policy decision, adapter, result category, timestamp, environment, latency, usage, and cost indicator
- AND SHALL exclude full prompts, full provider payloads, secrets, and personal data by default

### Requirement: ATP-110 - Runtime and provider configuration remain separately gated

The PoC specification SHALL NOT authorize runtime provisioning, account registration, credential creation, provider execution, model calls, Botpress changes, or publication.

#### Scenario: Specification is approved

- GIVEN the Owner approves this OpenSpec package
- WHEN planning tasks are completed
- THEN implementation SHALL remain blocked
- AND a separate bounded implementation gate SHALL be required

#### Scenario: Botpress is proposed

- GIVEN Botpress remains under `INCIDENT-HOLD` because unknown Bots exist
- WHEN a Runtime or interface is selected for this PoC
- THEN Botpress SHALL remain excluded
- AND no unknown Bot SHALL be opened, reused, modified, executed, published, exported, or deleted through this change

#### Scenario: Google integration is proposed

- GIVEN Google Places or Routes requires a billed Google Cloud project
- WHEN the integration is proposed
- THEN it SHALL require a separate architecture, privacy, quota, and financial approval gate
- AND it SHALL NOT be enabled by this change

#### Scenario: Provider account registration is proposed

- GIVEN Duffel or Hotelbeds account registration requires personal or authentication data
- WHEN a registration stage is later approved
- THEN the Owner SHALL enter those values herself
- AND Codex SHALL NOT read, store, or reproduce passwords, verification codes, tokens, or personal registration data

#### Scenario: Approved Docker Desktop in-place upgrade

- GIVEN the Owner separately approves `G3-Docker-Upgrade-Pilot`
- WHEN the host upgrade is performed
- THEN only an official checksum-matched and validly signed Docker Desktop package SHALL be used
- AND the existing Docker data disk SHALL remain present without reset, uninstall, deletion, export, copy, or content inspection
- AND no n8n resource, credential, provider connection, or provider API call SHALL be created or executed
- AND any requirement for reset, uninstall, destructive migration, or unverifiable data preservation SHALL fail closed and require a separate Owner gate

#### Scenario: Approved Docker VMM retry after upgrade

- GIVEN the Owner separately approves `G3-Docker-VMM-Retry-4.87`
- WHEN Docker VMM is selected through the official Docker Desktop UI on version `4.87.0`
- THEN only a new Docker VMM system data disk MAY be created
- AND the existing `docker_data.vhdx` SHALL NOT be deleted, copied, exported, mounted, or inspected
- AND no n8n resource, credential, provider connection, or provider API call SHALL be created or executed
- AND if the VMM backend is not persistent and daemon readiness cannot be verified, the result SHALL be `FAIL / VMM-BACKEND-BLOCKED` and further remediation SHALL require a separate Owner gate

#### Scenario: Approved offline Docker data backup

- GIVEN the Owner separately approves `G3-Docker-Offline-Backup` and explicitly selects the backup target
- WHEN Docker Desktop and WSL are fully stopped
- THEN only `docker_data.vhdx` MAY be copied without overwriting an existing backup
- AND the source and copy SHALL have matching SHA-256 values before a repair or reinstall gate can be considered
- AND the destination filesystem protection state SHALL be disclosed to the Owner
- AND no repair, uninstall, reset, n8n resource, credential, provider connection, or provider API call SHALL occur in this gate

#### Scenario: Approved Docker reinstall and restore

- GIVEN the Owner separately approves `G3-Docker-Reinstall`
- WHEN the validated offline backup and official signed installer are available while Docker Desktop and WSL are stopped
- THEN Docker Desktop MAY be uninstalled and reinstalled only at the approved version
- AND `docker_data.vhdx` MAY be restored only from the checksum-matched backup
- AND the backup copy SHALL remain intact after restoration
- AND no factory reset, WSL unregister, n8n resource, credential, provider connection, or provider API call SHALL occur
- AND failed restoration or daemon readiness SHALL stop further remediation and require a separate Owner gate

#### Scenario: Approved Windows integrity remediation

- GIVEN the Owner separately approves `G3-Windows-Integrity-Remediation`
- WHEN elevated Windows integrity tools run
- THEN only `DISM /RestoreHealth` and `sfc /scannow` MAY repair Windows components
- AND a Windows restart MAY occur only if the tools or pending state require it
- AND the Docker offline backup SHALL remain present before and after remediation
- AND no factory reset, WSL unregister, VHDX deletion, n8n resource, credential, provider connection, or provider API call SHALL occur
- AND failure of Windows repair or post-restart Docker readiness SHALL stop further remediation and require a separate Owner gate

#### Scenario: Integrity repair requires a restart

- GIVEN `DISM /RestoreHealth` has completed successfully and `sfc /scannow` repairs an operating-system driver
- WHEN a pending file-replacement state remains
- THEN the approved Windows restart MAY be used to apply the repair
- AND Docker readiness verification SHALL occur only after the restart
- AND no Docker data disk, n8n resource, credential, or provider connection SHALL be changed

#### Scenario: Vsock assessment proposes a privilege-only pilot

- GIVEN a read-only assessment proves that Docker's WSL distro is running but its `C:` DrvFS share is empty after `UtilConnectVsock` fails
- WHEN a potential elevation-boundary issue is identified
- THEN a separate Owner gate SHALL be required before Docker Desktop is stopped or relaunched elevated
- AND the pilot SHALL change no Docker setting, VHDX, n8n resource, credential, or provider connection

#### Scenario: Privilege pilot cannot close an unresponsive backend

- GIVEN the Owner has approved the privilege-only pilot
- WHEN Docker's documented normal shutdown remains blocked by the unresponsive backend
- THEN Docker SHALL NOT be force-stopped without a separate Owner gate
- AND elevated relaunch SHALL NOT occur while the existing Docker processes remain running
- AND no Docker setting, VHDX, n8n resource, credential, or provider connection SHALL be changed

#### Scenario: Elevated Docker retains the Plan9 failure

- GIVEN a separately approved force-quit pilot has stopped Docker and WSL cleanly
- WHEN Docker Desktop is relaunched through UAC and the local daemon check times out with the same Plan9/vsock failure
- THEN the system SHALL classify the elevation hypothesis as disproven
- AND Docker and WSL SHALL be stopped after the bounded check
- AND any Windows or WSL component change SHALL require a separate Owner gate

#### Scenario: WSL feature repair finds no disabled component

- GIVEN the Owner approves `G3-WSL-Feature-Repair` for an elevated feature-state check
- WHEN Windows Subsystem for Linux, VirtualMachinePlatform, and HypervisorPlatform are all Enabled
- THEN no feature toggle or restart SHALL occur under that gate
- AND the Plan9/vsock blocker SHALL remain documented as unresolved
- AND a feature-cycle or advanced WSL change SHALL require a separate Owner gate

#### Scenario: Approved WSL feature cycle

- GIVEN the Owner separately approves `G3-WSL-Feature-Cycle` and the Docker backup is present
- WHEN Windows Subsystem for Linux and VirtualMachinePlatform are disabled together
- THEN Windows SHALL restart before either feature is enabled again
- AND a second Windows restart SHALL occur after both features are re-enabled
- AND no Docker reset, uninstall, VHDX deletion, n8n resource, credential, or provider connection SHALL occur

### Requirement: ATP-111 - Local credential-store readiness before materialization

The PoC SHALL NOT materialize a Hotelbeds credential until the selected local `n8n self-hosted Community` store passes a documented readiness verification for host isolation, key custody, access control, persistence minimization, backup and restore, and dynamic-signature containment.

#### Scenario: Local store topology is provisioned

- GIVEN a separately approved provisioning stage creates the PoC credential-store instance
- WHEN network exposure and instance configuration are verified
- THEN the editor and service ports SHALL be reachable only from the Owner-controlled host through loopback
- AND local browser-to-instance traffic SHALL use HTTPS with a locally trusted certificate whose private key is protected outside the repository and database volume
- AND public API, API playground, external webhooks, instance MCP, user invitations, workflow sharing, templates, and diagnostic telemetry SHALL be disabled
- AND outbound provider traffic SHALL remain blocked until `G5-Hotelbeds-Network-Smoke`

#### Scenario: Encryption key is prepared

- GIVEN the local n8n instance needs an instance encryption key
- WHEN key custody is configured
- THEN the key SHALL be supplied from an Owner-readable protected file outside the repository, database volume, logs, prompts, and database backup set
- AND the key SHALL NOT be printed, exported, copied into OpenSpec, or generated through a command visible to Codex
- AND failure to load the expected key SHALL stop provisioning without creating a provider credential

#### Scenario: Owner access is configured

- GIVEN the local instance is ready for login
- WHEN access settings are reviewed
- THEN exactly one Owner account SHALL exist and SHALL use 2FA
- AND no additional user, shared project, shared workflow, shared credential, public API key, or remote administrative path SHALL exist
- AND Server CLI access SHALL be limited to the Owner-controlled OS context
- AND decrypted credential export SHALL be prohibited

#### Scenario: Execution persistence is configured

- GIVEN a future approved workflow processes a provider request
- WHEN success, error, manual, or progress execution data would normally be persisted
- THEN full execution payload persistence SHALL be disabled for every execution type
- AND sensitive request headers, signatures, credentials, and provider payloads SHALL NOT be written to item data, error details, logs, traces, or audit evidence
- AND only the minimized audit fields required by ATP-109 MAY be retained

#### Scenario: Backup and restore are verified before real credentials

- GIVEN the credential store has been provisioned without a Hotelbeds credential
- WHEN backup and restore readiness is tested
- THEN the test SHALL use a synthetic dummy credential only
- AND the encrypted database backup and the instance encryption key SHALL be stored separately
- AND restore SHALL reproduce only expected metadata without emitting the dummy value in terminal output, logs, screenshots, or files outside the restored store
- AND the documented PoC objectives SHALL be `RPO <= 24 hours`, `RTO <= 1 business day`, and backup expiry within 7 days

#### Scenario: Dynamic Hotelbeds signature path is reviewed

- GIVEN a first-party Hotelbeds credential/node is proposed in a separately approved implementation stage
- WHEN its security contract is reviewed before any real credential is entered
- THEN it SHALL accept `api_key` and `secret` only through the n8n credential interface
- AND SHALL compute `X-Signature` just-in-time inside the node
- AND SHALL allow only the approved Evaluation hostname and read-only endpoint set
- AND SHALL NOT return the credential fields or signature to workflow data, expressions, a Code node, error output, logs, or exports

#### Scenario: Any readiness control fails

- GIVEN one or more readiness controls are missing, unverifiable, or drift from the approved configuration
- WHEN the readiness decision is evaluated
- THEN the result SHALL be `NO-GO / MATERIALIZATION-BLOCKED`
- AND no Hotelbeds value SHALL be read, copied, stored, bound, or used
