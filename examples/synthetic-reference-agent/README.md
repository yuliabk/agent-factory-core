# Synthetic Reference Agent

This directory contains the smallest non-business reference definition used by the C6 synthetic end-to-end gate.

It proves the complete Core path without external providers, customer data, secrets, network calls, production storage or domain-specific business logic.

Files:

- `agent-manifest.json` - reusable Agent definition using only the accepted minimal AgentManifest contract.
- `client-instance-config.json` - sandbox tenant/environment instance values for the synthetic gate.
- `platform-policy.json` - strict policy covering the synthetic runtime/eval/release path.

The runtime Registry implementations remain test-owned Core fixtures; the Agent definition never selects concrete model/provider/capability implementations.
