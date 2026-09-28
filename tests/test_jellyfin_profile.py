from app.profiles.jellyfin import parse_media_filename


def test_parse_movie_filename() -> None:
    parsed = parse_media_filename("Dune.2021.2160p.mkv")

    assert parsed is not None
    assert parsed.media_type == "movie"
    assert parsed.title == "Dune"
    assert parsed.year == 2021
    assert parsed.target_relative_path == "Movies/Dune (2021)/Dune (2021).mkv"


def test_parse_tv_filename() -> None:
    parsed = parse_media_filename("Severance.S01E02.2160p.mkv")

    assert parsed is not None
    assert parsed.media_type == "tv"
    assert parsed.title == "Severance"
    assert parsed.season == 1
    assert parsed.episode == 2
    assert parsed.target_relative_path == "TV/Severance/Season 01/Severance - S01E02.mkv"


def test_parse_unknown_filename_returns_none() -> None:
    assert parse_media_filename("badly_named_file.mkv") is None


def test_parse_parenthesised_movie_filename() -> None:
    parsed = parse_media_filename("Alien (1979).mkv")

    assert parsed is not None
    assert parsed.target_relative_path == "Movies/Alien (1979)/Alien (1979).mkv"


def test_parse_compact_movie_filename() -> None:
    parsed = parse_media_filename("alien1979.mkv")

    assert parsed is not None
    assert parsed.target_relative_path == "Movies/Alien (1979)/Alien (1979).mkv"
