# Order Service Retry Design

## Overview

In today's fast-paced distributed world, reliability is more important than ever. This document describes how the Order Service handles failures when it calls the Payments API. In short, the service retries failed calls up to 5 times before giving up, which makes it robust and resilient.

## Background

Distributed systems are inherently unreliable. Networks partition, services restart, and requests time out. Industry best practices recommend that every service implement some form of retry logic to handle these transient failures gracefully. Our team has carefully considered these best practices while designing this solution, and we believe it represents a significant step forward for the reliability of our platform.

## Retry Behavior

When a call to the Payments API fails, the Order Service waits before trying again. The wait grows exponentially with each attempt, starting from a base delay of 200 ms, so the second retry waits longer than the first. This exponential backoff approach is a well-known and battle-tested pattern that helps prevent overwhelming a struggling downstream service.

## Configuration

Retry behavior can be configured through environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `RETRY_MAX` | `3` | Maximum number of retry attempts |
| `RETRY_BASE_MS` | `200` | Base delay for exponential backoff, in milliseconds |

These variables give operators the flexibility they need to tune the system.

## Error Handling

If every retry fails, the order message is moved to the dead-letter queue `orders-dlq` so that no orders are lost. It is worth noting that each backoff delay also includes random jitter of ±20%, which spreads retries out and avoids thundering-herd problems. This robust approach ensures that our system remains reliable even under adverse conditions.

## Future Work

We plan to add a circuit breaker in Q3. Once implemented, it would stop calling the Payments API after 50 consecutive failures. This is not built yet.

## FAQ

**Are all errors retried?**
No. Client errors (4xx) are not retried, because retrying them would not help. The one exception is 429 Too Many Requests, which is retried with the same backoff.

**Do we honor the Retry-After header on 503 responses?**
This is still an open question. The team has not decided yet.

**How long do messages stay in the dead-letter queue?**
Messages are kept in `orders-dlq` for 7 days.

## Conclusion

In conclusion, this retry design makes the Order Service significantly more reliable, scalable, and robust. By leveraging industry best practices such as exponential backoff, we ensure a seamless experience for our customers.
