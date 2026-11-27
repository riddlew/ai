# Security review details (v5)

Trace the complete relevant trust boundary, identities/roles, inputs, persistence, authorization enforcement, validation and output sinks through actual code, configuration and tests. Consider realistic injection, unsafe deserialization, authentication/authorization gaps, exposure of secrets and sensitive data, replay/concurrency, and unsafe defaults only when relevant. Try to disprove suspected vulnerabilities before reporting them.

Provide precise evidence, exploit conditions, impact and proportionate mitigation, and identify untested assumptions/residual risks. Never access production secrets or perform destructive testing without authorization. User decisions are required for consequential security-boundary changes, but there is no document-approval ceremony. Save a report only when useful/requested and never automatically invoke `brain-update`.
