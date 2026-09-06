# Synthetic Reference Agent

This directory contains the smallest non-business reference Agent Definition used by the C6 synthetic end-to-end gate.

It exists only to prove the complete Core path without provider, customer, domain, network, secret or production-storage dependencies.

The AgentManifest requests only the capabilities, tools and permissions needed by the deterministic synthetic plan. Client/environment values, policy, Registry implementations and runtime authority remain outside the reusable Agent definition.
