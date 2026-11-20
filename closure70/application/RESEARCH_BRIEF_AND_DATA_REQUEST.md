# GrowthResearch data request brief — applicant review required

Status: prepared, not submitted; no licence or NDA accepted.

Applicant/entity, affiliation, contact, commercial purpose, authorised researchers and infrastructure: **to be supplied accurately by the applicant**. No university affiliation, ethical clearance, or non-commercial status is presumed.

Purpose: independently test whether behaviour known at a fixed post-install observation point predicts later observed game revenue. This is not an attempt to recover Axon/Vector weights, evaluate their actual production effects, or construct cross-game personal identities.

First request: documentation and permission feasibility, not raw user data. Please identify the data controller, original competition task, retention/access status, permitted purpose, licence/NDA, and whether controlled computation rather than transfer is possible.

Minimum analytical data, subject to explicit approval:

| Table | Requested fields | Required semantic contract |
|---|---|---|
| Cohort/coverage | game_id, game-local random subject key, install_time, broad country/platform, observed_from/to, coverage_watermark, exit/missing reason | Include zero-revenue installs; identify incomplete observation, deletion and sampling; no real-world identity |
| Historical behaviour | local event_id/type, event_time, available_at, received_at, session/progression/ad counts, app/rule version | Define the last permitted feature time; no events that became available after prediction |
| Revenue | economic_event_id, IAA/IAP, time, amount, currency, precision, refund/status, FX/accounting definition | Real receipts vs catalogue price vs proxy; paid/fulfilled and mirrored SDK events deduplicated; scaling disclosed |
| Labels/definitions | D7/D28 window, timezone, maturity, non-payer inclusion, late-arrival policy | Fixed horizon; true zero distinguished from unobserved; no lifetime/period total mislabelled D28 |

Not requested: GAID/IDFA, email/phone, names, raw IP, precise location, login credentials, private third-party data, or user-level cross-product linkage. Existing anonymous IDs remain confined to the source game and must not enable external matching.

Proposed analysis after admission: fixed time-out split, user separation, early-behaviour versus early-real-revenue baselines, calibration and high-value recall with uncertainty. No training until licence, files, observation coverage and target maturity are verified. A second independently authorised game would enable parameter/aggregate transfer without joining individual people.

Security, access list, storage region, retention, deletion, disclosure controls, model artefact handling, publication and review periods are negotiation items; do not insert invented commitments. Prefer minimal anonymised extracts or provider-controlled computation. Aggregate reporting alone does not override underlying data permission.

Fallback: if original data are unavailable, request only a dictionary, example schema without real rows, window/scaling definitions, and a written statement of restrictions. Do not ask a participant to recover and forward a prohibited copy.
