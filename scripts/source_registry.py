"""Registry of news sources and feeds for AI news discovery."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Source:
    """Represents a tracked news source or RSS/Atom feed."""

    id: str
    name: str
    category: str
    feed_url: str
    official_url: str
    enabled: bool = True


# Default registered news sources
SOURCES: list[Source] = [
    Source(
        id="openai",
        name="OpenAI Newsroom",
        category="Company / Official",
        feed_url="https://openai.com/news/rss.xml",
        official_url="https://openai.com/news/",
        enabled=True,
    ),
    Source(
        id="anthropic",
        name="Anthropic News",
        category="Company / Official",
        feed_url="https://anthropic.com/feed.xml",
        official_url="https://www.anthropic.com/news",
        enabled=True,
    ),
    Source(
        id="deepmind",
        name="Google DeepMind",
        category="Research / Company",
        feed_url="https://deepmind.google/blog/rss.xml",
        official_url="https://deepmind.google/discover/blog/",
        enabled=True,
    ),
    Source(
        id="huggingface",
        name="Hugging Face Blog",
        category="Open Source / Community",
        feed_url="https://huggingface.co/blog/feed.xml",
        official_url="https://huggingface.co/blog",
        enabled=True,
    ),
    Source(
        id="arxiv",
        name="arXiv cs.AI",
        category="Research",
        feed_url="https://rss.arxiv.org/rss/cs.AI",
        official_url="https://arxiv.org/list/cs.AI/recent",
        enabled=True,
    ),
    Source(
        id="economic_times",
        name="Economic Times AI",
        category="Technology News",
        feed_url="https://economictimes.indiatimes.com/tech/artificial-intelligence/rss",
        official_url="https://economictimes.indiatimes.com/tech/artificial-intelligence",
        enabled=True,
    ),
]


def get_all_sources() -> list[Source]:
    """Return all configured sources regardless of enabled state."""
    return list(SOURCES)


def get_active_sources() -> list[Source]:
    """Return only enabled sources."""
    return [source for source in SOURCES if source.enabled]


def get_source_by_id(source_id: str) -> Optional[Source]:
    """Retrieve a source by its identifier slug."""
    for source in SOURCES:
        if source.id == source_id:
            return source
    return None
