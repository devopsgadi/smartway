---
name: log-redaction
description: Rules for scrubbing PII, secrets, and customer data from logs and records. Use before reasoning over or outputting any log line, ticket text, or config.
---
# Log Redaction

Replace before use/output:
| Pattern | Replace with |
|---|---|
| Account / card numbers (12–19 digits) | `[ACCT]` |
| SSN-like `\d{3}-\d{2}-\d{4}` | `[SSN]` |
| Emails | `[EMAIL]` |
| Phone numbers | `[PHONE]` |
| Bearer / JWT / API keys / passwords / connection strings | `[SECRET]` |
| Customer names in payloads | `[NAME]` |
| Client IPs (keep internal pod/node IPs) | `[IP]` |

Never copy secrets from k8s Secrets, Key Vault, or env vars. Reference by name only.
