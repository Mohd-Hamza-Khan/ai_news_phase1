"""Collect and normalize candidate news items from registered RSS/Atom feeds."""

from dataclasses import asdict, dataclass
import datetime
import html
import logging
import re
import time
from typing import Any, Optional

import feedparser
import requests

from scripts.source_registry import Source, get_active_sources

logger = logging.getLogger(__name__)

# Standard browser user-agent to prevent feed endpoints from blocking requests
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 (AI-News-Automation/1.0)"
)
DEFAULT_TIMEOUT_SECONDS = 15


@dataclass
class NewsCandidate:
    """Represents a normalized raw news candidate extracted from a source."""

    title: str
    url: str
    source: str
    published_at: str
    description: str
    category: str

    def to_dict(self) -> dict[str, str]:
        """Convert candidate to dictionary representation."""
        return asdict(self)


def clean_text(raw_text: Optional[str]) -> str:
    """Strip HTML tags, unescape HTML entities, and collapse extra whitespace."""
    if not raw_text:
        return ""
    # Strip HTML tags (replace with empty string, not a space)
    cleaned = re.sub(r"<[^>]+>", "", raw_text)
    # Decode HTML entities (e.g., &amp;, &quot;, &#39;)
    cleaned = html.unescape(cleaned)
    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def normalize_published_date(entry: Any) -> str:
    """
    Extract and convert publication date to UTC ISO 8601 (YYYY-MM-DDTHH:MM:SSZ).
    Returns 'unknown' if no valid date is available. Never guesses missing dates.
    """
    struct_date = getattr(entry, "published_parsed", None) or getattr(
        entry, "updated_parsed", None
    )

    if struct_date and isinstance(struct_date, time.struct_time):
        try:
            dt = datetime.datetime(*struct_date[:6], tzinfo=datetime.timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except (ValueError, OverflowError):
            pass

    return "unknown"


def fetch_feed_content(feed_url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> bytes:
    """Fetch raw feed content using HTTP GET with timeout and user-agent."""
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    response = requests.get(feed_url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.content


def parse_feed_entries(
    content: bytes, source: Source
) -> list[NewsCandidate]:
    """Parse raw XML/RSS/Atom content into normalized NewsCandidate objects."""
    parsed = feedparser.parse(content)

    candidates: list[NewsCandidate] = []
    for entry in getattr(parsed, "entries", []):
        title = clean_text(getattr(entry, "title", ""))
        url = getattr(entry, "link", "").strip()

        # Reject items without usable title or URL
        if not title or not url:
            continue

        published_at = normalize_published_date(entry)

        # Description / summary extraction
        raw_description = (
            getattr(entry, "summary", "")
            or getattr(entry, "description", "")
        )
        description = clean_text(raw_description)

        candidates.append(
            NewsCandidate(
                title=title,
                url=url,
                source=source.name,
                published_at=published_at,
                description=description,
                category=source.category,
            )
        )

    return candidates


def fetch_source_candidates(
    source: Source, timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> list[NewsCandidate]:
    """Fetch and parse candidates for a single source. Handles errors safely."""
    try:
        content = fetch_feed_content(source.feed_url, timeout=timeout)
        candidates = parse_feed_entries(content, source)
        logger.info(
            "Collected %d candidates from '%s'", len(candidates), source.name
        )
        return candidates
    except requests.exceptions.RequestException as exc:
        logger.warning(
            "Network error fetching feed for '%s' (%s): %s",
            source.name,
            source.feed_url,
            exc,
        )
        return []
    except Exception as exc:
        logger.error(
            "Unexpected error processing feed for '%s' (%s): %s",
            source.name,
            source.feed_url,
            exc,
            exc_info=True,
        )
        return []


def collect_all_candidates(
    sources: Optional[list[Source]] = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> list[NewsCandidate]:
    """
    Collect news candidates across all active sources.
    Failed feeds are logged and skipped; successful feeds continue working.
    """
    if sources is None:
        sources = get_active_sources()

    all_candidates: list[NewsCandidate] = []
    for source in sources:
        if not source.enabled:
            continue
        candidates = fetch_source_candidates(source, timeout=timeout)
        all_candidates.extend(candidates)

    logger.info(
        "Total candidates collected across %d sources: %d",
        len(sources),
        len(all_candidates),
    )
    return all_candidates


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    print("Collecting candidate news from active sources...")
    collected = collect_all_candidates()
    print(f"\nSuccessfully collected {len(collected)} candidates.\n")
    for idx, candidate in enumerate(collected[:10], start=1):
        print(f"[{idx}] {candidate.title}")
        print(f"    Source: {candidate.source} ({candidate.category})")
        print(f"    Published: {candidate.published_at}")
        print(f"    URL: {candidate.url}")
        print(f"    Description: {candidate.description[:120]}...\n")
