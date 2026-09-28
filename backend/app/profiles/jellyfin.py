import re
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class ParsedMedia:
    media_type: str
    title: str
    target_relative_path: str
    confidence: float
    reason: str
    season: int | None = None
    episode: int | None = None
    year: int | None = None


TV_PATTERN = re.compile(
    r"^(?P<title>.+?)[.\s_-]+S(?P<season>\d{1,2})E(?P<episode>\d{1,2})",
    re.IGNORECASE,
)
MOVIE_PATTERN = re.compile(
    r"^(?P<title>.+?)[.\s_-]*\(?(?P<year>19\d{2}|20\d{2})\)?(?:[.\s_-]|$)"
)


def parse_media_filename(filename: str) -> ParsedMedia | None:
    stem = PurePosixPath(filename).stem

    tv_match = TV_PATTERN.search(stem)
    if tv_match:
        title = clean_title(tv_match.group("title"))
        season = int(tv_match.group("season"))
        episode = int(tv_match.group("episode"))
        episode_code = f"S{season:02d}E{episode:02d}"
        return ParsedMedia(
            media_type="tv",
            title=title,
            season=season,
            episode=episode,
            target_relative_path=(
                f"TV/{title}/Season {season:02d}/{title} - {episode_code}{PurePosixPath(filename).suffix}"
            ),
            confidence=0.92,
            reason=f"Detected TV episode pattern {episode_code}",
        )

    movie_match = MOVIE_PATTERN.search(stem)
    if movie_match:
        title = clean_title(movie_match.group("title"))
        year = int(movie_match.group("year"))
        return ParsedMedia(
            media_type="movie",
            title=title,
            year=year,
            target_relative_path=f"Movies/{title} ({year})/{title} ({year}){PurePosixPath(filename).suffix}",
            confidence=0.9,
            reason=f"Detected movie title and year {year}",
        )

    return None


def clean_title(raw_title: str) -> str:
    words = re.sub(r"[._-]+", " ", raw_title).strip().split()
    return " ".join(capitalise_word(word) for word in words)


def capitalise_word(word: str) -> str:
    if word.isupper():
        return word
    return word[:1].upper() + word[1:].lower()
