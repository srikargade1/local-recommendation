# Intuit Recruiter Interview — Prep Notes
**Format:** 15 min screen-share walkthrough + 15 min Q&A
**Evaluated on:** Communication, Ownership, AI as a tool

---

## Elevator Pitch (30 seconds)

> "I built a full-stack local recommendation app that goes beyond a basic search.
> Instead of typing keywords into a form, you describe what you want in plain English —
> 'a cozy coffee shop, nothing too loud, I'm working remotely' — and the app uses AI
> at two stages: once to understand your intent and extract search filters, and again
> to intelligently re-rank the results and explain why each place was surfaced.
> It's deployed live, containerized with Docker, and ships automatically via CI/CD."

---

## 15-Minute Walkthrough Script

### [0:00–1:30] Set the scene — the problem

> "When you search Google Maps for 'quiet coffee shop near me open now,' you get
> 40 results ranked by distance. There's no understanding of what 'quiet' means,
> no penalty for chain restaurants, no explanation of why one place is ranked above another.
> I wanted to build something that actually understood what you were looking for."

### [1:30–4:00] Live demo

- Open the live app: **https://frontend-r0o4.onrender.com**
- Type a rich natural language query: `"cozy independent coffee shop, not too loud, I'm trying to work"`
- Point out as results load:
  - Each card shows a **photo**, **category tags**, **open/closed badge**
  - Each card has an **AI explanation** (the purple bar): *"Ranked #1 because it's a locally-owned cafe 4 minutes away that matches your quiet workspace preference"*
  - Travel times for walking, driving, transit
  - Thumbs up/down feedback buttons
- Then type in the **Refine box**: `"actually, something even closer"`
  - Show it re-runs with context — the new results are biased toward proximity

### [4:00–7:00] Walk the pipeline

Open `backend/core/pipeline.py`. Walk each step in plain English:

1. **Parse prompt** — natural language → structured JSON filters + preferences object
2. **Build query** — filters map to Foursquare API parameters
3. **Fetch places** — Foursquare returns up to 20 raw candidates
4. **Format** — normalize the raw API response into a clean internal schema
5. **Enrich travel times** — Google Maps Distance Matrix (batched — 3 calls, not 60)
6. **Filter** — apply hard constraints: walk time, drive time, chains, open status
7. **Score + sort** — initial ranking using dynamic weights
8. **LLM re-rank** — send top 10 to GPT with the original query; get back a ranked list with explanations
9. **Photos** — parallel photo fetches (one per place, non-blocking)
10. **Add direction links** — Google Maps deep links per result

> "Every step is a single-purpose function. That separation came from a suggestion
> by Claude when I asked how to structure this — and it made debugging dramatically easier."

### [7:00–10:00] The two AI layers — the key highlight

**Layer 1 — Query parsing** (`llm_parser.py`, `parse_prompt_to_filters`):

> "Instead of a form with 10 checkboxes, I send the user's plain-English prompt to
> GPT and ask it to return a JSON object: query terms, price range, open-now preference,
> whether to exclude chains. But I also added a 'preferences' object — things like
> 'does the user care about proximity?' or 'do they want local indie spots?' —
> which feeds directly into step 7."

**Layer 2 — Re-ranking with explanation** (`llm_parser.py`, `rerank_with_explanation`):

> "The initial scoring algorithm uses weighted rules — distance, chain penalty,
> category match. That works fine, but it can't understand 'cozy' or 'romantic'
> or 'good for a first date.' So after scoring, I send the top 10 candidates back
> to GPT with the original query and let it re-rank them with full context.
> It also writes a one-line explanation for each place, which shows up in the UI.
> That's the purple bar you see on each card."

**Why two stages?**

> "Coarse retrieval first — Foursquare is fast and returns 20 candidates cheaply.
> Fine re-ranking second — the LLM does the nuanced judgment on a small set.
> This is actually how production recommendation systems work: broad retrieval,
> then precision re-ranking."

### [10:00–12:00] Where I used AI to build it

> "I used Claude throughout the build. A few specific examples:

> 1. **Pipeline structure** — I asked Claude to help me design the backend as a
>    series of composable steps. It suggested the single-responsibility module layout
>    I ended up using. I reviewed each function, adjusted the logic, and caught
>    a few cases where the suggested filtering was too aggressive.

> 2. **Batching the Maps API** — I noticed the app was slow. Claude pointed out that
>    Google's Distance Matrix API supports multiple destinations per request.
>    I hadn't realized that. We went from 60 API calls per search to 3.

> 3. **The feedback loop** — I had the idea for thumbs-up/down, but wasn't sure
>    how to persist it simply. Claude suggested writing to a JSON file on the backend
>    as a starting point — easy to demo, easy to swap for a database later.

> I didn't accept everything. For example, Claude initially suggested doing the
> photo fetching synchronously. I pushed back and we implemented it with
> ThreadPoolExecutor to parallelize the requests."

### [12:00–14:00] DevOps and deployment

> "Both services are containerized with Docker, wired together with Docker Compose
> locally. In production, they deploy separately to Render. I set up GitHub Actions
> so that pushing to main automatically triggers a deploy — no manual steps."

Open `.github/workflows/deploy.yml` briefly.

> "It's minimal — just two curl commands to Render's deploy hooks. But it means
> every merge to main is live within a few minutes."

### [14:00–15:00] What I'd do next

> "A few things I'd improve:

> 1. **Feedback loop → weight tuning** — Right now thumbs-up/down is collected
>    but not yet acted on. The next step would be to periodically analyze that data
>    and adjust the scoring weights for specific query types.

> 2. **Map view** — I'd replace the card list with results pinned on an interactive map.
>    Much more useful for navigating between options.

> 3. **Move the Google Maps key server-side** — Currently the frontend passes it
>    in the request body. That's not ideal for production security."

---

## Likely Recruiter Questions + Prepared Answers

**"Walk me through how the AI is used."**
> "In two places. First, to parse the user's natural language query into structured
> search parameters — that drives the Foursquare API call. Second, to re-rank the
> top results with full awareness of the original query and generate a plain-English
> explanation for each result. The first is about extraction; the second is about judgment."

**"What did you build yourself vs. what did AI write?"**
> "The architecture is mine — I designed the pipeline stages, decided what data to
> collect from each API, and defined what the scoring algorithm should consider.
> AI helped me write individual functions faster and pointed out optimizations I'd
> missed, like the batched Maps API calls. I reviewed and tested every piece.
> When something didn't behave right — and there were several cases — I debugged
> it myself and corrected the AI's suggestion."

**"What was the hardest part?"**
> "Getting the 'open now' filtering right. My first version checked whether the word
> 'open' appeared in Foursquare's hours display string — which is completely unreliable.
> Foursquare actually returns a `closed_bucket` field with values like 'VeryLikelyOpen'
> that's much more reliable. I only discovered that by reading their API docs carefully."

**"What would you do differently?"**
> "I'd build the feedback loop into the scoring from day one rather than bolting it on.
> And I'd store results in a proper database rather than JSON files — I used files
> as a fast starting point but a real product would need queryable storage."

**"How does the scoring algorithm work?"**
> "There are two layers. The first is a weighted formula: distance penalizes far places,
> chain status penalizes non-local spots, category keyword match adds a bonus, and rating
> adds another. But those weights are now dynamic — if you say 'close to me' in your
> query, the LLM extracts a 'prioritize proximity' preference and the distance weight
> doubles. The second layer is LLM re-ranking, which can reason about things the
> formula can't — like 'cozy' or 'good for a date.'"

**"Tell me about a time AI suggested something wrong."**
> "During the photo fetching, Claude's first suggestion was to fetch photos sequentially
> — one HTTP request, wait for response, next request. With 20 places that would add
> several seconds of latency. I pointed that out and we switched to using Python's
> ThreadPoolExecutor to parallelize all 20 fetches. Response time was much better."

**"How does the refinement feature work?"**
> "When you type in the 'Refine' box, the app doesn't start over. It builds a
> conversation history — your original query, a summary of the results — and passes
> that to GPT alongside the new query. So 'something quieter' is understood in the
> context of what you already searched for. The LLM extracts different filters
> without losing the intent from the first query."

---

## Key Phrases to Use Naturally

- *"AI suggested X, but I decided Y because..."* — shows ownership
- *"I noticed the app was slow, so I traced it to..."* — shows engineering instinct
- *"The first version did X, which was fragile, so I changed it to..."* — shows iteration
- *"This is actually how production recommendation systems work — coarse retrieval, then fine re-ranking"* — shows depth

---

## Files to Have Open During Demo

| Moment | File to show |
|--------|-------------|
| Pipeline overview | `backend/core/pipeline.py` |
| LLM parsing | `backend/core/llm_parser.py` (parse_prompt_to_filters) |
| LLM re-ranking | `backend/core/llm_parser.py` (rerank_with_explanation) |
| Dynamic scoring | `backend/core/scoring.py` (build_weights) |
| Batched Maps | `backend/core/maps.py` |
| CI/CD | `.github/workflows/deploy.yml` |
| Live UI | https://frontend-r0o4.onrender.com |

---

## Before the Interview

- [ ] Deploy the latest code to Render and verify the live demo works end to end
- [ ] Test the refine flow: initial query → refine → confirm different results
- [ ] Test the feedback buttons: thumbs up → "Thanks!" confirmation appears
- [ ] Test with photos: verify at least some cards show images
- [ ] Rotate the Render deploy hook keys in `.github/workflows/deploy.yml` — move them to GitHub Secrets
- [ ] Have all the files listed above open in tabs, ready to switch to
- [ ] Run through the walkthrough out loud at least once — aim for 13 minutes to leave buffer
