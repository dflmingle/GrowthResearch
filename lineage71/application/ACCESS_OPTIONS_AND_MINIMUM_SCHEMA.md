# Access options and minimum schema — proposals, not accepted terms

No current Uken licence/NDA or data package has been obtained. The following is a request for feasibility discussion, subject to holder and applicant approval.

## Option A: controlled computation

Data remain with the authorized holder. Ask whether vetted code can run in its environment and only approved aggregate results can leave. Confirm staff access, security, code review, disclosure thresholds, allowed output/model export, retention, deletion and any fees before agreement. No claim that such infrastructure already exists.

## Option B: minimal anonymized file

If expressly permitted, request a source-local random player key plus the minimum fields below. No name, email, account credential, advertising identifier, IP or cross-game join key. Do not build a cross-product personal identity mapping.

| Table | Minimum fields | Semantics that must accompany it |
|---|---|---|
| Observation roster | source-local random key;install or first-observed time;observation start/end;exit/censor flag;coverage watermark | Included population, zero-revenue users, entry/exit/missingness and timezone |
| Behaviour | key;event type;event time;available/arrival time if retained;value/unit | Original definitions, sampling, gaps and whether only aggregates exist |
| Revenue | key;transaction/event key if permitted;time;amount;currency;precision;reversal/status | Actual IAP/IAA versus transformed target, scaling, gross/net, refunds and deduplication |
| Historical competition target | field dictionary;target start/end;label-known time;transformation details | Whether 30-day or other targets are complete;unlabeled split is not zero revenue |

If events or arrival times were never retained, ask for an explicit statement. Do not request invented replacements. Player aggregates can support only the narrower tasks justified by their original windows and permitted target semantics.

Admission: licence and intended use allowed;actual files verified;stable source-local key;known observed population;meaningful monetary target;observation and maturity windows;zeros distinguishable from censoring/missingness;no time leakage. Until then: STOP, no training.

Two independent authorized games with comparable definitions would be needed for a later transfer experiment. No same-person association across games is required. This proposal does not claim availability of a second game.
