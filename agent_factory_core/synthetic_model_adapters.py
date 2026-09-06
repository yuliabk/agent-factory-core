from __future__ import annotations

from .model_router import (
    ModelAdapterOutput,
    ModelAdapterSpec,
    ModelRegistration,
    ModelRequest,
)


def _units(text: str) -> int:
    stripped = text.strip()
    return 0 if not stripped else len(stripped.split())


def build_deterministic_model_adapter() -> ModelRegistration:
    spec = ModelAdapterSpec(
        implementation_id="model.synthetic.primary.v1",
        version="1",
        supported_profiles=("balanced", "economy"),
        allowed_data_classifications=("internal",),
        minimum_trust_profile="internal",
    )

    def handler(request: ModelRequest) -> ModelAdapterOutput:
        text = f"primary:{request.input_text}"
        return ModelAdapterOutput(
            text=text,
            input_units=_units(request.input_text),
            output_units=_units(text),
        )

    return ModelRegistration(spec=spec, handler=handler)


def build_stub_model_adapter() -> ModelRegistration:
    spec = ModelAdapterSpec(
        implementation_id="model.synthetic.stub.v1",
        version="1",
        supported_profiles=("balanced", "economy"),
        allowed_data_classifications=("internal",),
        minimum_trust_profile="internal",
    )

    def handler(request: ModelRequest) -> ModelAdapterOutput:
        text = f"stub:{request.input_text}"
        return ModelAdapterOutput(
            text=text,
            input_units=_units(request.input_text),
            output_units=_units(text),
        )

    return ModelRegistration(spec=spec, handler=handler)
