#!/bin/sh
# Conservative Brain context selection, POSIX shell/awk/Git only.
set -eu
HERE=$(CDPATH= cd -- "$(dirname "$0")" && pwd -P)
fail() { printf 'ERROR %s\n' "$*" >&2; exit 1; }
brain=
branch=
action=${1:-}
case "$action" in plan|map) shift;; *) fail 'action must be plan or map';; esac
tmp=$(mktemp -d) || fail 'cannot create temporary directory'
trap 'rm -rf "$tmp"' 0
trap 'exit 1' 1 2 3 15
: > "$tmp/options"
while [ "$#" -gt 0 ]; do
  key=$1; shift
  case "$key" in --brain|--branch|--feature|--path) :;; *) fail "unknown argument: $key";; esac
  [ "$#" -gt 0 ] || fail "missing argument for $key"
  value=$1; shift
  case "$value" in --*) fail "missing argument for $key";; esac
  case "$key" in
    --brain) brain=$value;;
    --branch)
      case "$value" in ''|/*|*..*|*[!A-Za-z0-9._/-]*) fail 'invalid branch';; esac
      branch=$value;;
    --feature)
      case "$value" in ''|*[!a-z0-9-]*|-*|*-|*--) fail 'invalid feature slug';; esac
      printf 'FEATURE\t%s\n' "$value" >> "$tmp/options";;
    --path)
      case "$value" in ''|/*|..|../*|*/../*|*/..|./*|*/./*|*//*|*[!A-Za-z0-9_./\ -]*) fail 'invalid relative path';; esac
      printf 'PATH\t%s\n' "$value" >> "$tmp/options";;
  esac
done
[ -n "$brain" ] || fail '--brain required'
brain=$(CDPATH= cd -- "$brain" && pwd -P) || fail 'Brain inaccessible'
[ -f "$brain/00_index.md" ] || fail 'brain index missing'

# Reject links instead of accidentally omitting potentially applicable documents.
if [ -n "$(find "$brain" -type l -print -quit)" ];then fail 'unsafe symlink in Brain';fi

: > "$tmp/docs"
find "$brain" -type f -name '*.md' | LC_ALL=C sort | while IFS= read -r full;do
  rel=${full#"$brain"/}
  case "$rel" in README.md|USAGE.md) continue;; esac
  sha=$(git hash-object "$full") || fail 'Git required for content fingerprints'
  bytes=$(wc -c < "$full" | tr -d ' ')
  printf 'DOC\t%s\t%s\t%s\n' "$rel" "$sha" "$bytes"
done > "$tmp/docs"

[ -f "$brain/context-map.tsv" ] || { map_missing=1; }
if [ "$action" = map ];then
  printf '# brain-context-map v1\n'
  printf '# Review scope declarations before using selective loading.\n'
  awk -F '\t' '$1=="DOC"&&$2 !~ /^features\//&&$2 !~ /^pending\// {print $2 "\tglobal\t-\t" $3}' "$tmp/docs"
  exit 0
fi
cat "$tmp/docs" > "$tmp/plan"
if [ "${map_missing:-0}" = 1 ];then
  printf 'NO_MAP\n' >> "$tmp/plan"
else
  { IFS= read -r header || :; [ "$header" = '# brain-context-map v1' ]; } < "$brain/context-map.tsv" ||
    printf 'BAD_HEADER\n' >> "$tmp/plan"
  awk -F '\t' 'NR>1 && $0!="" && $0 !~ /^#/ {
    if(NF!=4)print "BAD_ROW";
    else print "MAP\t" $1 "\t" $2 "\t" $3 "\t" $4
  }' "$brain/context-map.tsv" >> "$tmp/plan"
fi
cat "$tmp/options" >> "$tmp/plan"
[ -z "$branch" ] || printf 'BRANCH\t%s\n' "$branch" >> "$tmp/plan"
awk -v brain="$brain" -f "$HERE/brain-context-plan.awk" "$tmp/plan"
