# Knowledge Agent Prototype V1 Spec Delta

## ADDED Requirements

### Requirement: KA-101 - Synthetic approved corpus only

The prototype SHALL retrieve only from versioned, approved, Hebrew synthetic sources assigned to tenant `af-demo-services` and the active corpus version.

#### Scenario: Approved synthetic source

- GIVEN a source is synthetic, approved, assigned to `af-demo-services`, and included in the active corpus version
- WHEN retrieval runs for an Owner question
- THEN the source SHALL be eligible for retrieval

#### Scenario: Real or sensitive content proposed

- GIVEN a source contains or may contain personal, confidential, medical, financial, credential, or real customer information
- WHEN it is proposed for the prototype corpus
- THEN ingestion SHALL be blocked and the source SHALL require a separate approved security and privacy path

#### Scenario: Superseded source

- GIVEN a source version is marked `superseded` or `withdrawn`
- WHEN retrieval runs
- THEN that version SHALL NOT be used as current evidence

### Requirement: KA-102 - Grounded Hebrew answers

The prototype SHALL answer in Hebrew using only facts directly supported by eligible retrieved evidence.

#### Scenario: Sufficient evidence

- GIVEN eligible retrieved sections directly support the requested facts
- WHEN the prototype answers
- THEN the answer SHALL state only supported facts in clear Hebrew

#### Scenario: Model prior knowledge differs

- GIVEN model prior knowledge or assumptions differ from the approved corpus
- WHEN the prototype answers a corpus question
- THEN the approved eligible evidence SHALL govern and unsupported prior knowledge SHALL NOT appear as fact

### Requirement: KA-103 - Traceable citations

The prototype SHALL cite each material supported claim using `[SOURCE_ID § Section]` and SHALL NOT represent an uncited claim as corpus-supported.

#### Scenario: Supported policy claim

- GIVEN an answer states a policy fact from an eligible section
- WHEN the answer is returned
- THEN the claim SHALL be followed by the correct source identifier and section citation

#### Scenario: Citation unavailable

- GIVEN the system cannot identify a supporting eligible section
- WHEN it prepares an answer
- THEN it SHALL omit the unsupported claim or return the insufficient-evidence fallback

#### Scenario: Deterministic citation enrichment

- GIVEN a retrieved Chunk contains an exact stable Section heading and its approved document metadata contains a valid `source_id`
- WHEN the evidence context is prepared for the answer model
- THEN the context SHALL expose both values deterministically and the claim citation SHALL use `[SOURCE_ID § Section]`

#### Scenario: Citation metadata missing or foreign

- GIVEN a retrieved Chunk lacks `source_id` or contains a value outside the active approved corpus
- WHEN the evidence context is prepared
- THEN the Chunk SHALL NOT support a grounded claim and the system SHALL fail closed without inventing an identifier or disclosing foreign content

#### Scenario: Opaque UI metadata with source-backed schema

- GIVEN the Runtime UI exposes Retrieval `metadata` as an opaque object but the pinned official Runtime source maps custom document metadata to `metadata.doc_metadata`
- WHEN a Template prepares evidence context
- THEN it SHALL access `source_id` only through the reviewed source-backed path, SHALL enforce the active corpus allow-list, and SHALL remain blocked from Runtime until the hosted behavior is separately validated

### Requirement: KA-104 - Insufficient-evidence fallback

The prototype SHALL use the approved fallback when eligible evidence is absent or insufficient and SHALL NOT invent an answer.

#### Scenario: Unsupported question

- GIVEN the active corpus does not contain sufficient evidence for the question
- WHEN the Owner asks the question
- THEN the prototype SHALL return the canonical insufficient-evidence fallback and SHALL NOT infer a policy

#### Scenario: Retrieval unavailable

- GIVEN retrieval is unavailable or returns no verifiable evidence
- WHEN a question is processed
- THEN the prototype SHALL state that approved information is unavailable and SHALL NOT answer from model memory

### Requirement: KA-105 - Conflict and ambiguity handling

The prototype SHALL expose unresolved conflict or material ambiguity instead of silently choosing an answer.

#### Scenario: Conflicting approved sources

- GIVEN two current approved sources contain materially conflicting statements
- WHEN the question depends on that conflict
- THEN the prototype SHALL identify both source IDs, avoid selecting a policy, and request Owner review

#### Scenario: Explicitly superseded policy

- GIVEN an older source is explicitly `superseded` and a newer source is `approved`
- WHEN both are retrieved
- THEN the prototype SHALL use only the approved current version and cite it

#### Scenario: Ambiguous question

- GIVEN the question has multiple materially different interpretations supported by different sections
- WHEN no interpretation can be selected safely
- THEN the prototype SHALL ask a focused clarification question

### Requirement: KA-106 - Prompt-injection resistance

The prototype SHALL treat user text and retrieved text as untrusted content that cannot override system policy, change tenant, enable tools, suppress citations, disclose hidden instructions, or request secrets.

#### Scenario: Injection inside a source

- GIVEN a retrieved document contains text instructing the agent to ignore policy or reveal hidden instructions
- WHEN the document is retrieved
- THEN the text SHALL be treated only as untrusted content and the override SHALL NOT be followed

#### Scenario: Injection in a question

- GIVEN a question asks the agent to ignore the corpus, browse the web, reveal prompts, or fabricate an answer
- WHEN the prototype processes the question
- THEN the request SHALL be refused or safely answered under the approved policy without performing the prohibited behavior

### Requirement: KA-107 - No actions or external tools

The prototype SHALL operate as a read-only Knowledge Agent with external tools, writes, messages, browsing, and side effects disabled.

#### Scenario: Action request

- GIVEN the Owner asks the prototype to send, update, delete, order, refund, browse, or call an external system
- WHEN the request is processed
- THEN no tool or side effect SHALL occur and the prototype SHALL explain that the capability is outside scope

#### Scenario: Runtime exposes built-in tools

- GIVEN the selected Runtime makes built-in Tools available at Workspace level
- WHEN the prototype App is configured or reconstructed
- THEN the App SHALL attach no Tool, MCP, Trigger, Extension or external-call node regardless of Workspace availability

### Requirement: KA-108 - Fixed tenant and Owner-only isolation

The prototype SHALL accept only the fixed synthetic tenant `af-demo-services` and an authorized Owner actor and SHALL deny cross-tenant or unknown-actor retrieval.

#### Scenario: Cross-tenant request

- GIVEN a request supplies a different tenant or asks for another tenant's corpus
- WHEN retrieval is attempted
- THEN retrieval SHALL be denied and no foreign source metadata or content SHALL be disclosed

#### Scenario: Unknown actor

- GIVEN a request is not associated with the authorized Owner actor type
- WHEN it reaches the prototype boundary
- THEN the request SHALL be denied before retrieval

### Requirement: KA-109 - Frozen acceptance evaluation

The prototype SHALL be evaluated against a versioned 25-question set frozen before each scored run and SHALL preserve failures in the evaluation record.

#### Scenario: Scored run

- GIVEN the corpus, configuration, release, and 25-question set are versioned and frozen
- WHEN an authorized scored evaluation runs
- THEN every question SHALL record answer, citation, fallback, policy, latency, cost, and verdict indicators

#### Scenario: Configuration changed after failure

- GIVEN a scored question fails and configuration is changed
- WHEN evaluation resumes
- THEN a new configuration version and evaluation run SHALL be created and the original failure SHALL remain recorded

#### Scenario: Release threshold

- GIVEN any mandatory safety threshold or minimum quality threshold is not met
- WHEN promotion is considered
- THEN the prototype SHALL remain unapproved for release

### Requirement: KA-110 - Minimized evaluation records

The prototype SHALL record only the metadata and synthetic content needed to reproduce and assess an evaluation and SHALL exclude secrets and personal data.

#### Scenario: Evaluation record written

- GIVEN a test question completes or fails
- WHEN its evaluation record is stored
- THEN the record SHALL include run, question, request, tenant, release, corpus, configuration, retrieved source IDs, policy result, verdicts, latency, cost indicator, and timestamp without credentials or personal data

### Requirement: KA-111 - Measurable cost gate

The prototype SHALL NOT execute paid or provisioned runtime evaluation until a request limit, measurable cost indicator, and Owner-approved budget cap are configured.

#### Scenario: Cost controls unavailable

- GIVEN runtime cost cannot be measured or capped
- WHEN a paid evaluation is requested
- THEN execution SHALL remain blocked

#### Scenario: Budget threshold reached

- GIVEN an approved evaluation reaches its request or budget threshold
- WHEN another request is attempted
- THEN the run SHALL stop or apply the Owner-approved degraded policy and SHALL record the budget event

#### Scenario: Staged authorization

- GIVEN Runtime work is separated into resource configuration, one-document Indexing pilot, remaining Indexing, smoke test and scored evaluation Stages
- WHEN the Owner approves one named Stage
- THEN only that Stage SHALL be authorized and every later Stage SHALL remain blocked pending a separate explicit approval

#### Scenario: Zero-spend Sandbox drift

- GIVEN authorization relies on Sandbox Credits with no paid quota, BYOK or enabled Billing path
- WHEN a pre-stage check detects any change to that account state
- THEN the Stage SHALL stop before Upload, Indexing or Model execution and SHALL require Owner review
