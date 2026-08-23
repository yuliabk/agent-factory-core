"""Deterministic, offline validator for PR-G1 runtime-portability fixtures.

The module intentionally uses only the Python standard library and exposes no
live/provider execution path. It validates local JSON-compatible objects and
returns data without writing files.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from typing import Any, Iterable, Mapping


SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
QUESTION_ID = re.compile(r"^KA-E(0[1-9]|1\d|2[0-5])$")
HEBREW = re.compile(r"[\u0590-\u05FF]")

IDENTITY_FIELDS = (
    "adapter_id",
    "adapter_version",
    "runtime",
    "runtime_plan",
    "configuration_version",
    "agent_release_id",
    "corpus_version",
    "question_set_version",
)

REQUIRED_CAPABILITIES = (
    "knowledge_retrieval",
    "source_provenance",
    "hebrew_io",
    "deterministic_fallback",
    "external_actions_disabled",
    "run_logs_usage",
    "provider_native_limit",
    "export_reconstruction",
    "deletion_retention",
    "tenant_runtime_isolation",
)

ISOLATED_RESOURCES = (
    "credentials",
    "configuration",
    "storage",
    "knowledge",
    "indexes",
    "logs",
    "evidence",
)

DELETION_CLASSES = (
    "documents",
    "chunks",
    "vectors",
    "conversations",
    "logs",
    "runs",
    "backups",
)

RESPONSE_TYPES = {"answer", "fallback", "policy_block", "runtime_error"}
POLICY_RESULTS = {"allowed", "blocked", "unknown"}
CITATION_SUPPORT = {"direct", "partial"}
FORBIDDEN_SECRET_KEYS = {
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "password",
    "secret",
    "client_secret",
    "private_key",
    "authorization",
    "cookie",
}

CANONICAL_FALLBACK_HE = (
    "אין לי מספיק מידע במקורות המאושרים כדי לענות על השאלה. "
    "אפשר לנסח אותה מחדש או להעביר אותה לבדיקה של Yulush."
)


@dataclass(frozen=True)
class CheckResult:
    """One validation result with stable, serializable errors."""

    ok: bool
    errors: tuple[str, ...]

    @classmethod
    def from_errors(cls, errors: Iterable[str]) -> "CheckResult":
        stable = tuple(sorted(set(errors)))
        return cls(ok=not stable, errors=stable)

    def as_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "errors": list(self.errors)}


def _is_object(value: Any) -> bool:
    return isinstance(value, Mapping)


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _non_negative_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _find_secret_paths(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if _is_object(value):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_SECRET_KEYS:
                found.append(child_path)
            found.extend(_find_secret_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_secret_paths(child, f"{path}[{index}]"))
    return found


def validate_adapter(
    adapter: Any, canonical: Mapping[str, str] | None = None
) -> CheckResult:
    """Validate an adapter declaration and fail closed on unknown controls."""

    errors: list[str] = []
    if not _is_object(adapter):
        return CheckResult.from_errors(["adapter must be an object"])

    identity = adapter.get("identity")
    if not _is_object(identity):
        errors.append("identity must be an object")
        identity = {}

    for field in IDENTITY_FIELDS:
        if not isinstance(identity.get(field), str) or not identity[field].strip():
            errors.append(f"identity.{field} must be a non-empty string")

    adapter_version = identity.get("adapter_version")
    if isinstance(adapter_version, str) and not SEMVER.fullmatch(adapter_version):
        errors.append("identity.adapter_version must be SemVer")

    if canonical:
        for field in ("agent_release_id", "corpus_version", "question_set_version"):
            expected = canonical.get(field)
            if expected is not None and identity.get(field) != expected:
                errors.append(f"identity.{field} does not match canonical value")

    capabilities = adapter.get("capabilities")
    if not _is_object(capabilities):
        errors.append("capabilities must be an object")
        capabilities = {}

    for name in REQUIRED_CAPABILITIES:
        capability = capabilities.get(name)
        if not _is_object(capability):
            errors.append(f"capabilities.{name} must be declared")
            continue
        if capability.get("supported") is not True:
            errors.append(f"capabilities.{name}.supported must be true")
        if not isinstance(capability.get("evidence"), str) or not capability["evidence"].strip():
            errors.append(f"capabilities.{name}.evidence must be non-empty")
        if not isinstance(capability.get("limitations"), list):
            errors.append(f"capabilities.{name}.limitations must be an array")
        if not _valid_date(capability.get("verified_at")):
            errors.append(f"capabilities.{name}.verified_at must be an ISO date")

    if adapter.get("data_scope") != "synthetic_only":
        errors.append("data_scope must be synthetic_only")
    if adapter.get("tool_policy") != "deny_all":
        errors.append("tool_policy must be deny_all")

    isolation = adapter.get("isolation")
    if not _is_object(isolation):
        errors.append("isolation must be an object")
        isolation = {}
    for resource in ISOLATED_RESOURCES:
        rule = isolation.get(resource)
        if not _is_object(rule):
            errors.append(f"isolation.{resource} must be declared")
            continue
        if rule.get("dedicated") is not True:
            errors.append(f"isolation.{resource}.dedicated must be true")
        if rule.get("shared_with_other_clients") is not False:
            errors.append(f"isolation.{resource}.shared_with_other_clients must be false")
        if not isinstance(rule.get("boundary_id"), str) or not rule["boundary_id"].strip():
            errors.append(f"isolation.{resource}.boundary_id must be non-empty")

    cost = adapter.get("cost_controls")
    if not _is_object(cost):
        errors.append("cost_controls must be an object")
        cost = {}
    if cost.get("usage_observable") is not True:
        errors.append("cost_controls.usage_observable must be true")
    for field in ("native_unit", "native_currency"):
        if not isinstance(cost.get(field), str) or not cost.get(field, "").strip():
            errors.append(f"cost_controls.{field} must be non-empty")
    for field in ("native_limit", "native_stop_threshold", "normalized_limit_ils", "normalized_stop_threshold_ils"):
        if not _positive_number(cost.get(field)):
            errors.append(f"cost_controls.{field} must be a positive number")
    if _positive_number(cost.get("native_limit")) and _positive_number(cost.get("native_stop_threshold")):
        if cost["native_stop_threshold"] > cost["native_limit"]:
            errors.append("cost_controls.native_stop_threshold cannot exceed native_limit")
    if _positive_number(cost.get("normalized_limit_ils")) and _positive_number(cost.get("normalized_stop_threshold_ils")):
        if cost["normalized_stop_threshold_ils"] > cost["normalized_limit_ils"]:
            errors.append("cost_controls.normalized_stop_threshold_ils cannot exceed normalized_limit_ils")
    if not isinstance(cost.get("conversion_source"), str) or not cost["conversion_source"].strip():
        errors.append("cost_controls.conversion_source must be non-empty")
    if not _valid_date(cost.get("conversion_timestamp")):
        errors.append("cost_controls.conversion_timestamp must be an ISO date")
    if cost.get("conversion_confidence") not in {"verified", "estimated"}:
        errors.append("cost_controls.conversion_confidence cannot be unknown")

    lifecycle = adapter.get("lifecycle")
    if not _is_object(lifecycle):
        errors.append("lifecycle must be an object")
        lifecycle = {}
    if not isinstance(lifecycle.get("export_evidence"), str) or not lifecycle.get("export_evidence", "").strip():
        errors.append("lifecycle.export_evidence must be non-empty")
    if not isinstance(lifecycle.get("retention_policy"), str) or not lifecycle.get("retention_policy", "").strip():
        errors.append("lifecycle.retention_policy must be non-empty")
    deletion = lifecycle.get("deletion_classes")
    if not isinstance(deletion, list):
        errors.append("lifecycle.deletion_classes must be an array")
    else:
        missing = sorted(set(DELETION_CLASSES) - set(deletion))
        if missing:
            errors.append(f"lifecycle.deletion_classes missing: {', '.join(missing)}")

    for path in _find_secret_paths(adapter):
        errors.append(f"secret-bearing field is prohibited: {path}")

    return CheckResult.from_errors(errors)


def validate_question_set(question_set: Any) -> CheckResult:
    """Validate the frozen 25-question synthetic evaluation set."""

    errors: list[str] = []
    if not _is_object(question_set):
        return CheckResult.from_errors(["question_set must be an object"])

    if question_set.get("data_classification") != "synthetic":
        errors.append("data_classification must be synthetic")
    if question_set.get("locale") != "he-IL":
        errors.append("locale must be he-IL")
    if question_set.get("primary_question_count") != 25:
        errors.append("primary_question_count must be 25")
    retries = question_set.get("max_technical_retries")
    if not isinstance(retries, int) or isinstance(retries, bool) or not 0 <= retries <= 5:
        errors.append("max_technical_retries must be an integer from 0 through 5")

    questions = question_set.get("questions")
    if not isinstance(questions, list):
        return CheckResult.from_errors(errors + ["questions must be an array"])
    if len(questions) != 25:
        errors.append("questions must contain exactly 25 entries")

    seen: set[str] = set()
    for index, question in enumerate(questions):
        prefix = f"questions[{index}]"
        if not _is_object(question):
            errors.append(f"{prefix} must be an object")
            continue
        question_id = question.get("question_id")
        if not isinstance(question_id, str) or not QUESTION_ID.fullmatch(question_id):
            errors.append(f"{prefix}.question_id must be KA-E01 through KA-E25")
        elif question_id in seen:
            errors.append(f"duplicate question_id: {question_id}")
        else:
            seen.add(question_id)
        query = question.get("query_he")
        if not isinstance(query, str) or not query.strip():
            errors.append(f"{prefix}.query_he must be non-empty")
        expected = question.get("expected_response_type")
        if expected not in RESPONSE_TYPES:
            errors.append(f"{prefix}.expected_response_type is invalid")
        citations = question.get("allowed_citations")
        if not isinstance(citations, list):
            errors.append(f"{prefix}.allowed_citations must be an array")
        else:
            for citation_index, citation in enumerate(citations):
                if not _valid_source_ref(citation):
                    errors.append(f"{prefix}.allowed_citations[{citation_index}] is invalid")

    expected_ids = {f"KA-E{index:02d}" for index in range(1, 26)}
    missing_ids = sorted(expected_ids - seen)
    if missing_ids:
        errors.append(f"question IDs missing: {', '.join(missing_ids)}")

    for path in _find_secret_paths(question_set):
        errors.append(f"secret-bearing field is prohibited: {path}")
    return CheckResult.from_errors(errors)


def _valid_source_ref(value: Any) -> bool:
    return (
        _is_object(value)
        and isinstance(value.get("source_id"), str)
        and bool(value["source_id"].strip())
        and isinstance(value.get("section_id"), str)
        and bool(value["section_id"].strip())
    )


def validate_fixture(
    fixture: Any,
    questions: Mapping[str, Mapping[str, Any]],
    canonical: Mapping[str, str] | None = None,
    expected_adapter_id: str | None = None,
) -> CheckResult:
    """Validate one synthetic normalized response/evidence fixture."""

    errors: list[str] = []
    if not _is_object(fixture):
        return CheckResult.from_errors(["fixture must be an object"])

    question_id = fixture.get("question_id")
    question = questions.get(question_id) if isinstance(question_id, str) else None
    if question is None:
        errors.append("fixture.question_id does not exist in the frozen question set")

    request = fixture.get("request")
    if not _is_object(request):
        errors.append("fixture.request must be an object")
        request = {}
    if request.get("question_id") != question_id:
        errors.append("fixture.request.question_id must match fixture.question_id")
    for field in ("request_id", "agent_release_id", "question_set_version", "query_he"):
        if not isinstance(request.get(field), str) or not request.get(field, "").strip():
            errors.append(f"fixture.request.{field} must be non-empty")
    if request.get("locale") != "he-IL":
        errors.append("fixture.request.locale must be he-IL")
    if request.get("tool_policy") != "deny_all":
        errors.append("fixture.request.tool_policy must be deny_all")
    if not isinstance(request.get("approved_corpus_version"), str) or not request.get("approved_corpus_version", "").strip():
        errors.append("fixture.request.approved_corpus_version must be non-empty")
    if question and request.get("query_he") != question.get("query_he"):
        errors.append("fixture.request.query_he must match the frozen question")
    if canonical:
        request_to_canonical = {
            "agent_release_id": "agent_release_id",
            "question_set_version": "question_set_version",
            "approved_corpus_version": "corpus_version",
        }
        for request_field, canonical_field in request_to_canonical.items():
            expected = canonical.get(canonical_field)
            if expected is not None and request.get(request_field) != expected:
                errors.append(f"fixture.request.{request_field} does not match canonical value")
    max_retrieval_items = request.get("max_retrieval_items")
    if not isinstance(max_retrieval_items, int) or isinstance(max_retrieval_items, bool) or max_retrieval_items <= 0:
        errors.append("fixture.request.max_retrieval_items must be a positive integer")
    provider_options = request.get("provider_options", {})
    if not _is_object(provider_options):
        errors.append("fixture.request.provider_options must be an object when present")
    else:
        protected = {
            "locale": "he-IL",
            "tool_policy": "deny_all",
            "approved_corpus_version": request.get("approved_corpus_version"),
        }
        for field, canonical_value in protected.items():
            if field in provider_options and provider_options[field] != canonical_value:
                errors.append(f"fixture.request.provider_options cannot override {field}")

    response = fixture.get("response")
    if not _is_object(response):
        errors.append("fixture.response must be an object")
        response = {}
    response_type = response.get("response_type")
    if response_type not in RESPONSE_TYPES:
        errors.append("fixture.response.response_type is invalid")
    if question and response_type != question.get("expected_response_type"):
        errors.append("fixture.response.response_type does not match expected response type")
    answer = response.get("answer_he")
    if not isinstance(answer, str) or not answer.strip() or not HEBREW.search(answer):
        errors.append("fixture.response.answer_he must contain Hebrew text")
    if response.get("policy_result") not in POLICY_RESULTS:
        errors.append("fixture.response.policy_result is invalid")
    if response.get("tool_calls") != []:
        errors.append("fixture.response.tool_calls must be an empty array")

    evidence = fixture.get("evidence")
    if not _is_object(evidence):
        errors.append("fixture.evidence must be an object")
        evidence = {}
    for field in ("run_id", "adapter_id", "provider_run_ref"):
        if not isinstance(evidence.get(field), str) or not evidence.get(field, "").strip():
            errors.append(f"fixture.evidence.{field} must be non-empty")
    if expected_adapter_id is not None and evidence.get("adapter_id") != expected_adapter_id:
        errors.append("fixture.evidence.adapter_id does not match the validated adapter")
    latency = evidence.get("latency_ms")
    if latency is not None and (
        not isinstance(latency, int) or isinstance(latency, bool) or latency < 0
    ):
        errors.append("fixture.evidence.latency_ms must be null or a non-negative integer")
    drift = evidence.get("drift")
    if not _is_object(drift):
        errors.append("fixture.evidence.drift must be an object")
        drift = {}
    if drift.get("detected") is not False:
        errors.append("fixture.evidence.drift.detected must be false")
    if not isinstance(drift.get("details"), list):
        errors.append("fixture.evidence.drift.details must be an array")
    attempt = evidence.get("attempt")
    if not isinstance(attempt, int) or isinstance(attempt, bool) or not 1 <= attempt <= 6:
        errors.append("fixture.evidence.attempt must be an integer from 1 through 6")

    retrieved = evidence.get("retrieved_items")
    if not isinstance(retrieved, list):
        errors.append("fixture.evidence.retrieved_items must be an array")
        retrieved = []
    retrieved_refs = {
        (item.get("source_id"), item.get("section_id"))
        for item in retrieved
        if _valid_source_ref(item)
    }

    citations = response.get("citations")
    if not isinstance(citations, list):
        errors.append("fixture.response.citations must be an array")
        citations = []
    citation_refs: set[tuple[Any, Any]] = set()
    for index, citation in enumerate(citations):
        if not _valid_source_ref(citation):
            errors.append(f"fixture.response.citations[{index}] is invalid")
            continue
        if citation.get("support") not in CITATION_SUPPORT:
            errors.append(f"fixture.response.citations[{index}].support is invalid")
        citation_ref = (citation.get("source_id"), citation.get("section_id"))
        citation_refs.add(citation_ref)
        if citation_ref not in retrieved_refs:
            errors.append(f"unresolved citation: {citation_ref[0]} § {citation_ref[1]}")

    if response_type == "answer":
        if not citations:
            errors.append("answer fixtures require at least one citation")
        if question:
            allowed = {
                (item.get("source_id"), item.get("section_id"))
                for item in question.get("allowed_citations", [])
                if _valid_source_ref(item)
            }
            unexpected = citation_refs - allowed
            if unexpected:
                errors.append("answer fixture contains a citation outside the allowed question sources")
    elif citations:
        errors.append("non-answer fixtures must not contain citations")

    if response_type == "fallback" and answer != CANONICAL_FALLBACK_HE:
        errors.append("fallback fixture must use the canonical Hebrew fallback")

    usage = evidence.get("usage")
    if not _is_object(usage):
        errors.append("fixture.evidence.usage must be an object")
        usage = {}
    if not isinstance(usage.get("native_unit"), str) or not usage.get("native_unit", "").strip():
        errors.append("fixture.evidence.usage.native_unit must be non-empty")
    if not _non_negative_number(usage.get("native_quantity")):
        errors.append("fixture.evidence.usage.native_quantity must be non-negative")
    if not _non_negative_number(usage.get("native_cost")):
        errors.append("fixture.evidence.usage.native_cost cannot be unknown")
    if not isinstance(usage.get("native_currency"), str) or not usage.get("native_currency", "").strip():
        errors.append("fixture.evidence.usage.native_currency cannot be unknown")

    normalized = evidence.get("normalized_cost")
    if not _is_object(normalized):
        errors.append("fixture.evidence.normalized_cost must be an object")
        normalized = {}
    if not _non_negative_number(normalized.get("amount_ils")):
        errors.append("fixture.evidence.normalized_cost.amount_ils cannot be unknown")
    if not isinstance(normalized.get("conversion_source"), str) or not normalized.get("conversion_source", "").strip():
        errors.append("fixture.evidence.normalized_cost.conversion_source cannot be unknown")
    if not _valid_date(normalized.get("conversion_timestamp")):
        errors.append("fixture.evidence.normalized_cost.conversion_timestamp must be an ISO date")
    if normalized.get("confidence") not in {"verified", "estimated"}:
        errors.append("fixture.evidence.normalized_cost.confidence cannot be unknown")

    for path in _find_secret_paths(fixture):
        errors.append(f"secret-bearing field is prohibited: {path}")
    return CheckResult.from_errors(errors)


def run_dry_validation(adapter: Any, question_set: Any, fixtures: Any) -> dict[str, Any]:
    """Return a deterministic dry report; never execute questions or external calls."""

    canonical = {}
    if _is_object(question_set):
        canonical = {
            field: question_set.get(field)
            for field in ("agent_release_id", "corpus_version", "question_set_version")
            if isinstance(question_set.get(field), str)
        }
    adapter_check = validate_adapter(adapter, canonical)
    question_check = validate_question_set(question_set)

    fixture_list = fixtures if isinstance(fixtures, list) else []
    fixture_container_error = None if isinstance(fixtures, list) else "fixtures must be an array"
    question_map: dict[str, Mapping[str, Any]] = {}
    if _is_object(question_set) and isinstance(question_set.get("questions"), list):
        question_map = {
            question["question_id"]: question
            for question in question_set["questions"]
            if _is_object(question) and isinstance(question.get("question_id"), str)
        }

    fixture_reports = []
    if fixture_container_error:
        fixture_reports.append(
            {"fixture_id": None, "status": "blocked", "errors": [fixture_container_error]}
        )
    else:
        for index, fixture in enumerate(fixture_list):
            expected_adapter_id = None
            if _is_object(adapter) and _is_object(adapter.get("identity")):
                candidate_adapter_id = adapter["identity"].get("adapter_id")
                if isinstance(candidate_adapter_id, str):
                    expected_adapter_id = candidate_adapter_id
            check = validate_fixture(fixture, question_map, canonical, expected_adapter_id)
            fixture_id = fixture.get("fixture_id") if _is_object(fixture) else None
            fixture_reports.append(
                {
                    "fixture_id": fixture_id or f"fixture-{index + 1}",
                    "status": "pass" if check.ok else "fail",
                    "errors": list(check.errors),
                }
            )

    cost_errors: list[str] = []
    native_quantity_total = 0.0
    normalized_cost_total_ils = 0.0
    if _is_object(adapter) and _is_object(adapter.get("cost_controls")):
        cost_controls = adapter["cost_controls"]
        expected_native_unit = cost_controls.get("native_unit")
        expected_native_currency = cost_controls.get("native_currency")
        for fixture in fixture_list:
            if not _is_object(fixture) or not _is_object(fixture.get("evidence")):
                continue
            evidence = fixture["evidence"]
            usage = evidence.get("usage")
            normalized = evidence.get("normalized_cost")
            if _is_object(usage):
                if usage.get("native_unit") != expected_native_unit:
                    cost_errors.append("fixture native_unit does not match adapter cost controls")
                if usage.get("native_currency") != expected_native_currency:
                    cost_errors.append("fixture native_currency does not match adapter cost controls")
                if _non_negative_number(usage.get("native_quantity")):
                    native_quantity_total += float(usage["native_quantity"])
            if _is_object(normalized) and _non_negative_number(normalized.get("amount_ils")):
                normalized_cost_total_ils += float(normalized["amount_ils"])
        native_stop = cost_controls.get("native_stop_threshold")
        normalized_stop = cost_controls.get("normalized_stop_threshold_ils")
        if _positive_number(native_stop) and native_quantity_total > native_stop:
            cost_errors.append("synthetic fixture usage exceeds native stop threshold")
        if _positive_number(normalized_stop) and normalized_cost_total_ils > normalized_stop:
            cost_errors.append("synthetic fixture cost exceeds normalized stop threshold")

    blocked = not adapter_check.ok or not question_check.ok or fixture_container_error is not None
    failed = any(item["status"] == "fail" for item in fixture_reports) or bool(cost_errors)
    overall = "blocked" if blocked else "fail" if failed else "pass"
    lifecycle = "preflight_passed" if overall == "pass" else "planned"

    questions = []
    if _is_object(question_set) and isinstance(question_set.get("questions"), list):
        questions = [
            {"question_id": item.get("question_id"), "runtime_status": "not_run"}
            for item in question_set["questions"]
            if _is_object(item)
        ]

    digest_input = {
        "adapter": deepcopy(adapter),
        "question_set": deepcopy(question_set),
        "fixtures": deepcopy(fixtures),
    }
    dry_run_id = "dry-" + hashlib.sha256(
        json.dumps(digest_input, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "schema_version": "1.0.0",
        "mode": "offline_dry_validation",
        "dry_run_id": dry_run_id,
        "overall_verdict": overall,
        "lifecycle_state": lifecycle,
        "external_calls": 0,
        "runtime_questions_executed": 0,
        "adapter_validation": adapter_check.as_dict(),
        "question_set_validation": question_check.as_dict(),
        "fixture_validation": fixture_reports,
        "cost_validation": {
            "ok": not cost_errors,
            "native_quantity_total": native_quantity_total,
            "normalized_cost_total_ils": normalized_cost_total_ils,
            "errors": sorted(set(cost_errors)),
        },
        "questions": questions,
    }
