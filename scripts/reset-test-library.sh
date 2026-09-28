#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-dev-data/media}"

rm -rf "$ROOT"
mkdir -p \
  "$ROOT/01-clean/Alien (1979)" \
  "$ROOT/02-needs-renaming" \
  "$ROOT/03-tv" \
  "$ROOT/04-ambiguous" \
  "$ROOT/05-collisions/Alien (1979)" \
  "$ROOT/06-weird" \
  "$ROOT/07-ignore"

touch "$ROOT/01-clean/Alien (1979)/Alien (1979).mkv"

touch "$ROOT/02-needs-renaming/alien1979.mkv"
touch "$ROOT/02-needs-renaming/The.Matrix.1999.REMUX.mkv"
touch "$ROOT/02-needs-renaming/Dune.2021.2160p.mkv"

touch "$ROOT/03-tv/Severance.S01E01.mkv"
touch "$ROOT/03-tv/Severance.S01E02.mkv"

touch "$ROOT/04-ambiguous/alien.mkv"
touch "$ROOT/04-ambiguous/dune.mkv"

touch "$ROOT/05-collisions/Alien (1979)/Alien (1979).mkv"
touch "$ROOT/05-collisions/Alien.1979.mkv"

touch "$ROOT/06-weird/movie final FINAL.mkv"
touch "$ROOT/06-weird/Some.Movie.[1080p].[x265].mkv"
touch "$ROOT/06-weird/badly_named_file.mkv"

touch "$ROOT/07-ignore/poster.jpg"
touch "$ROOT/07-ignore/notes.txt"
touch "$ROOT/07-ignore/.hidden"

find "$ROOT" -print | sort
