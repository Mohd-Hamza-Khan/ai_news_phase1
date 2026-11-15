# AI News Repository Automation

Latest daily AI news, research breakthroughs, and engineering insights automatically updated.

<!-- AI_NEWS_START -->
*No news stories published yet. Daily automation will populate this section.*
<!-- AI_NEWS_END -->

---

## Project Overview & Architecture

This repository automates the discovery, verification, summarization, and publication of daily artificial intelligence news from trusted primary sources (OpenAI, Anthropic, Google DeepMind, Hugging Face, arXiv cs.AI, Economic Times AI).

### Implementation Phases

- [x] **Phase 1 — Project Foundation & OpenRouter Connection** (Completed & Tested)
- [x] **Phase 2 — News Source Registry & Feed Collection** (Completed & Tested)
- [ ] **Phase 3 — Cleaning, Verification, Deduplication & Selection**
- [ ] **Phase 4 — OpenRouter Research Summaries & Structured Validation**
- [ ] **Phase 5 — README Update & Archive Management (`news.md`)**
- [ ] **Phase 6 — GitHub Actions Daily Automation (`9:00 AM IST`)**
- [ ] **Phase 7 — Testing, Reliability & Maintenance**

---

## Quick Start & Local Setup

1. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Configure environment (`.env`):**
   Copy `.env.example` to `.env` and fill in your OpenRouter credentials:
   ```env
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
   ```

## Documentation
- See [source.md](source.md) for tracked news sources and RSS feeds.
- See [news.md](news.md) for historical archives.
