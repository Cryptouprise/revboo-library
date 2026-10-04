# Muse · ads operations and measurement contract

Muse is an extensible agent tag with role `media_buyer`. Creative agents retain their own creator/editor tags. `operated_by` records who runs an ad; operation does not change who created it. This dashboard currently uses local JSON imports. No Meta, CRM or Muse account has been connected. The dashboard never launches, pauses or changes budgets.

## Before launching
Record account, currency, account timezone, campaign/adset/ad IDs, exact immutable creative asset_id/hash, objective, optimization event, audience, placement policy, offer/destination, budget limit, dates, named approver and tracking checks. User approval of a creative is not unlimited spending authority. Muse must follow the user's actual campaign/spend authorization. No authorization is conveyed by this document alone.

## Dashboard import
Use catalog/metrics-template.json. One row per account/ad/date in the account timezone, totals across placements (no overlapping placement breakdowns in this file). Dates are YYYY-MM-DD. Every row must reference a registered exact export. An ad changing creative needs a new platform ad ID or explicit non-overlapping mapping. One currency, timezone and attribution definition per file. No PII. Import replaces the in-memory dataset; it never adds duplicate rows to an earlier import. Blank metrics are null, observed zero is 0. Do not put fabricated sample results in a real import.

Meta fields: spend, impressions, views_3s, thruplays, outbound_clicks, landing_page_views, meta_leads. CRM fields: qualified_leads, booked_calls, held_calls, new_customers, collected_revenue. Assign each CRM outcome once to the exact acquisition ad and acquisition date, deduplicate leads/customers by private stable IDs upstream and include crm_deduped=true only after doing so. Do not import email/phone into this public dashboard. Store source exports and a reconciliation log privately.

The CRM cohort is by acquisition date, while Meta results follow the stated platform attribution setting. These are separate measures. Do not add Meta attributed leads to CRM qualified leads, or Meta attributed revenue to collected revenue. Mature delayed cohorts before choosing a winner. imported_at, source_updated_at and crm_mature_through must be truthful ISO timestamps/dates.

## Measures
- CPM = spend / impressions * 1000.
- Hook rate = 3-second views / impressions; compare similar placement/length/objective and label definition.
- Hold proxy = ThruPlays / 3-second views; not a literal unique-person survival probability. If denominators zero/missing, unknown.
- Outbound CTR = outbound clicks / impressions. Landing page arrival = LPV / outbound clicks.
- Cost per qualified lead = spend / deduplicated CRM qualified leads.
- Held-call rate = held / booked; close rate = new customers / held calls.
- Media CAC = ALL relevant media spend / distinct new customers, including audience-building spend. Fully loaded CAC additionally includes production, tools, sales costs; not currently computed.
- Collected revenue / media spend is cash-revenue-to-spend, not margin, profit, lifetime value or causal ROAS.
- Never sum daily/ad-level unique reach into unique campaign reach. Frequency/audience size require separate correctly scoped exports; absent in this first importer.
- Null is unknown. An aggregate requiring any missing row value is withheld to avoid presenting partial totals as complete.

## Two strategies to compare
A: Direct prospecting → relevant free-ad offer, optimize to the actual lead/sales outcome available in the account.
B: Prospecting video → qualified engagement pool → follow-up creative with proof/process → same offer.
Randomized assignment or a suitable holdout is needed for causal comparison. Simple observed totals are directional and can be confounded by audience, geography, budget, time and attribution. Avoid audience overlap where the account supports it. Count B's audience-building AND retargeting spend in its outcome cost. Keep creative/offers and observation windows comparable. Do not starve a small audience across many ad sets.

Initial audience candidates for Muse to verify in the actual account: 10-second viewers if offered; ThruPlay; 50%/75% viewers of similar-length clips; engaged site visitors. Test a recent window such as 7 or 30 days based on volume and sales cycle, not as a universal rule. Exclude existing converters/customers as appropriate. Confirm the audience is an actual delivery restriction where required, not merely a suggestion subject to expansion. Do not claim an audience has been created until verified.

Meta's indexed official ThruPlay guidance defines a 15-second view or approximately complete view of a shorter video; it is not a universal '15+ seconds' condition. Full help page retrieval encountered a sign-in/block wall on 2026-10-04. Exact video-audience options and settings must be confirmed in Ads Manager. Sources: https://www.facebook.com/business/help/2051461368219124 ; https://www.facebook.com/business/help/1796060333844808 . Secondary corroboration: https://www.jonloomer.com/glossary/video-engagement-custom-audience/ . No claim of lower costs from retargeting is established for RevBoo yet.

## Decision log and feedback
Muse supplies observation, cohort/window, data freshness, sample size, attribution caveat, hypothesis, recommended creative change, spend requested, authorizer and outcome. Do not auto-declare winners from low CPL, views or a handful of leads. Return specific briefs to creative agents (e.g., strong opening but few outbound clicks: test offer/CTA while holding hook constant). Benchmarks belong to the account; this first dashboard uses no invented global score or arbitrary pause thresholds.

## Safe shared operation
Use the shared IDs and workflow. Keep all account metrics, customer information and tokens in private storage. Public GitHub holds the dashboard code/schema and already-public creative catalog only. Each agent needs its own authorized API/connector access. If no access, import an approved export; say not connected. Data in the browser resets when refreshed unless the user downloads an export. No automatic synchronization is installed.
