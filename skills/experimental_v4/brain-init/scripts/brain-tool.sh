#!/bin/sh
# POSIX shell fallback; no Python, Node, jq, or npm packages.
set -eu
HERE=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REFS=$HERE/../references
die() { printf 'ERROR %s\n' "$*" >&2; exit 1; }
need() { [ -n "$2" ] || die "--$1 is required"; }
slug() { case "$1" in ''|*[!a-z0-9-]*|*-|-*|*--) die "invalid slug: $1";; esac; }
abs() {
  case "$1" in /*) target=$1;; *) target=$PWD/$1;; esac
  suffix=
  ancestor=$target
  while [ ! -d "$ancestor" ]; do
    tail_name=$(basename "$ancestor")
    suffix="/$tail_name$suffix"
    next=$(dirname "$ancestor")
    [ "$next" != "$ancestor" ] || die "cannot canonicalize path: $1"
    ancestor=$next
  done
  physical=$(CDPATH= cd -- "$ancestor" && pwd -P) || die "cannot canonicalize path: $1"
  printf '%s%s\n' "$physical" "$suffix"
}
guard() {
  [ ! -L "$1" ] || die "symlink file is not an authorized write target: $1"
  [ -n "$AUTHORIZED" ] || die '--authorized-root is required for --apply'
  case "$1" in "$AUTHORIZED"|"$AUTHORIZED"/*) :;; *) die "outside authorized write root: $1";; esac
  root_real=$(CDPATH= cd -- "$AUTHORIZED" 2>/dev/null && pwd -P) ||
    die "authorized write root missing: $AUTHORIZED"
  parent=$(dirname "$1")
  while [ ! -d "$parent" ]; do
    next=$(dirname "$parent")
    [ "$next" != "$parent" ] || die "invalid destination: $1"
    parent=$next
  done
  parent_real=$(CDPATH= cd -- "$parent" 2>/dev/null && pwd -P) ||
    die "invalid destination parent: $parent"
  case "$parent_real" in "$root_real"|"$root_real"/*) :;;
    *) die "symlink escapes authorized root: $1";; esac
}
put() {
  target=$1; source=$2
  [ "$APPLY" != 1 ] || guard "$target"
  if [ -e "$target" ]; then
    [ -f "$target" ] && cmp -s "$source" "$target" || die "existing content differs: $target"
    printf 'UNCHANGED %s\n' "$target"
  elif [ "$APPLY" != 1 ]; then printf 'CREATE %s (dry-run)\n' "$target"
  else
    mkdir -p "$(dirname "$target")"
    (set -C; cat "$source" > "$target") || die "concurrent creation: $target"
    printf 'CREATED %s\n' "$target"
  fi
}
next_number() {
  dir=$1;max=0
  for child in "$dir"/[0-9]*-*; do
    [ -e "$child" ] || continue
    name=$(basename "$child");digits=${name%%-*}
    case "$digits" in ''|*[!0-9]*) continue;; esac
    value=$(awk -v n="$digits" 'BEGIN{printf "%d",n+0}')
    [ "$value" -le "$max" ] || max=$value
  done
  printf '%s\n' "$((max+1))"
}
scaffold() {
  kind=$1;feature=$2;name=$3
  title=$(printf '%s' "$name" | awk -F- '{for(i=1;i<=NF;i++){w=$i;printf "%s%s",i==1?"":" ",toupper(substr(w,1,1)) substr(w,2)}printf "\n"}')
  case "$kind" in
    execution) target=$BRAIN/features/$feature/execution.md;;
    planning-index) target=$BRAIN/planning/$feature/INDEX.md;;
    planning-ticket)
      dir=$BRAIN/planning/$feature
      n=$(next_number "$dir")
      [ -n "$n" ] || n=1
      num=$(printf '%03d' "$n");target=$dir/$num-$name.md;;
    diagnosis)
      dir=$BRAIN/diagnoses
      n=$(next_number "$dir")
      [ -n "$n" ] || n=1
      num=$(printf '%02d' "$n");target=$dir/$num-$name.md;;
    review)
      case "$REPORTTYPE" in architecture|code|merge-request|security) :;; *) die 'invalid or missing --report-type';; esac
      dir=$BRAIN/reviews/$REPORTTYPE
      n=$(next_number "$dir")
      [ -n "$n" ] || n=1
      num=$(printf '%02d' "$n");target=$dir/$num-$name/review.md;;
    *) die "unknown kind: $kind";;
  esac
  [ ! -e "$target" ] || die "existing document; refusing overwrite: $target"
  tmp=$(mktemp);trap 'rm -f "$tmp"' 0 HUP INT TERM
  input=$HERE/scaffolds/$kind.md
  [ -f "$input" ] || die "missing scaffold: $input"
  sed "s/{{TITLE}}/$title/g" "$input" > "$tmp"
  put "$target" "$tmp"
}
emit_context_doc() {
  f=$1
  rel=$2
  bytes=$(wc -c < "$f" | tr -d ' ')
  status=$(sed -n 's/^status: //p' "$f" | head -1)
  [ -n "$status" ] || status=-
  if [ "$HASHES" = 1 ]; then
    digest=$(git hash-object "$f") || die 'Git required for context fingerprints'
    printf 'DOC %s\t%s\t%s\t%s\n' "$rel" "$bytes" "$status" "$digest"
  else
    printf 'DOC %s\t%s\t%s\n' "$rel" "$bytes" "$status"
  fi
  if [ "$ESTIMATE" = 1 ]; then printf '%s\n' "$bytes" >> "$SUMFILE";fi
}
family=help
if [ "$#" -gt 0 ]; then family=$1;shift;fi
case "$family" in help|--help|-h) echo 'brain-tool <init|doc|validate|git|record|context> [options]';exit 0;; esac
case "${1:-}" in new|list|summary) shift;; esac
SAVELOCATION=0 PENDING=0 HASHES=0 ESTIMATE=0 SELECT= BRAIN= FEATURE= KIND= NAME= REPO=. AUTHORIZED= APPLY=0 TRACKING=ignored REVISION= DATE= MAIN=main PARENTS= SINCE= AFFECTED= HASHFILE= COVERAGE=0 EVENT= DETAIL= BRANCH= REPORTTYPE=
while [ "$#" -gt 0 ]; do
  arg=$1;shift
  case "$arg" in
    --apply) APPLY=1;; --save-location) SAVELOCATION=1;; --check-coverage) COVERAGE=1;; --pending) PENDING=1;; --estimate) ESTIMATE=1;; --hashes) HASHES=1;;
    --brain|--feature|--kind|--slug|--repo|--authorized-root|--tracking|--revision|--at|--main-branch|--parent|--since|--affected|--show-parent-hashes|--event|--detail|--branch|--report-type|--select)
      [ "$#" -gt 0 ] || die "missing value for $arg"
      v=$1;shift
      case "$arg" in
        --brain) BRAIN=$v;; --feature) FEATURE=$v;; --kind) KIND=$v;; --slug) NAME=$v;;
        --repo) REPO=$v;; --authorized-root) AUTHORIZED=$v;; --tracking) TRACKING=$v;;
        --revision) REVISION=$v;; --at) DATE=$v;; --main-branch) MAIN=$v;;
        --parent) PARENTS="$PARENTS $v";; --since) SINCE=$v;; --affected) AFFECTED=$v;;
        --show-parent-hashes) HASHFILE=$v;; --event) EVENT=$v;; --detail) DETAIL=$v;; --branch) BRANCH=$v;; --report-type) REPORTTYPE=$v;; --select) SELECT=$v;;
      esac;;
    *) die "unknown argument: $arg";;
  esac
done
REPO=$(abs "$REPO")
[ -z "$BRAIN" ] || BRAIN=$(abs "$BRAIN")
[ -z "$AUTHORIZED" ] || AUTHORIZED=$(abs "$AUTHORIZED")
tick=$(printf '\140')
case "$family" in
init)
  need brain "$BRAIN"
  case "$TRACKING" in ignored|tracked) :;; *) die 'tracking must be ignored or tracked';; esac
  tmp=$(mktemp -d);trap 'rm -rf "$tmp"' 0 HUP INT TERM
  index=$BRAIN/00_index.md
  if [ -f "$index" ]; then cp "$index" "$tmp/index"
  else
    [ -n "$REVISION" ] || REVISION=$(git -C "$REPO" rev-parse HEAD) || die 'Git HEAD unavailable'
    [ -n "$DATE" ] || DATE=$(date -u '+%Y-%m-%d')
    {
      printf '# Project Brain Index\n\nLast synced: %s (%s)\nGit: %s\nMain branch: %s\n\n' "$REVISION" "$DATE" "$TRACKING" "$MAIN"
      printf '## Root files\n\n| File | Purpose | Status |\n|---|---|---|\n\n## Documents\n\n| Path | Purpose | Status |\n|---|---|---|\n'
      printf '| %sUSAGE.md%s | Brain Skills workflow examples and selection guide | reference |\n' "$tick" "$tick"
      printf '| %sREADME.md%s | Brain Skills catalog and installation reference | reference |\n' "$tick" "$tick"
    } > "$tmp/index"
  fi
  if [ -f "$index" ]; then
    grep -F "USAGE.md$tick |" "$index" >/dev/null && grep -F "README.md$tick |" "$index" >/dev/null ||
      { [ "$APPLY" != 1 ] || die 'index missing guide rows; review before applying'; echo 'REVIEW index guide registration'; }
  fi
  for name in README.md USAGE.md; do
    target=$BRAIN/$name
    if [ -e "$target" ] && ! cmp -s "$REFS/$name" "$target"; then
      printf 'REVIEW existing %s: differs from bundled guide; preserved\n' "$target"
    fi
  done
  policy=$REPO/CLAUDE.local.md
  if [ "$SAVELOCATION" = 1 ]; then
    location="Project brain: $BRAIN"
    if [ -f "$policy" ]; then
      matches=$(grep -c '^Project brain:' "$policy" || :)
      if [ "$matches" -gt 1 ] || { [ "$matches" -eq 1 ] && ! grep -Fx "$location" "$policy" >/dev/null; }; then
        die 'conflicting saved Project brain location; review before applying'
      fi
      if [ "$matches" -eq 0 ] && [ "$APPLY" = 1 ]; then guard "$policy";fi
    fi
  fi
  # Ignore an untracked personal policy even when the Brain itself is tracked.
  exclude_entries=
  if [ "$TRACKING" = ignored ] && [ "$BRAIN" = "$REPO/.brain" ] &&
     ! git -C "$REPO" check-ignore -q -- .brain/ >/dev/null 2>&1; then
    exclude_entries=".brain/"
  fi
  if ! git -C "$REPO" ls-files --error-unmatch -- CLAUDE.local.md >/dev/null 2>&1 &&
     ! git -C "$REPO" check-ignore -q -- CLAUDE.local.md >/dev/null 2>&1; then
    exclude_entries="${exclude_entries}${exclude_entries:+
}CLAUDE.local.md"
  fi
  # Check Git admin authorization before creating or installing any Brain files.
  if [ "$APPLY" = 1 ] && [ -n "$exclude_entries" ]; then
    common=$(git -C "$REPO" rev-parse --path-format=absolute --git-common-dir) ||
      die 'Git metadata unavailable'
    excluded=$common/info/exclude
    guard "$excluded"
  fi
  [ -f "$index" ] || put "$index" "$tmp/index"
  for name in USAGE.md README.md; do
    target=$BRAIN/$name
    if [ -e "$target" ] && ! cmp -s "$REFS/$name" "$target"; then
      : # Differing user guide is preserved and reported in preflight.
    else
      put "$target" "$REFS/$name"
    fi
  done
  if [ ! -e "$policy" ]; then
    if [ "$SAVELOCATION" = 1 ]; then
      cp "$REFS/CLAUDE.local.md" "$tmp/policy"
      printf '\n%s\n' "$location" >> "$tmp/policy"
      put "$policy" "$tmp/policy"
    else put "$policy" "$REFS/CLAUDE.local.md";fi
  else
    if ! cmp -s "$policy" "$REFS/CLAUDE.local.md"; then
      echo 'REVIEW existing CLAUDE.local.md; preserve custom policy'
    fi
    if [ "$SAVELOCATION" = 1 ] && [ "$matches" -eq 0 ]; then
      if [ "$APPLY" = 1 ]; then
        printf '\n%s\n' "$location" >> "$policy"
        printf 'UPDATED %s: Project brain location\n' "$policy"
      else printf 'APPEND %s: Project brain location (dry-run)\n' "$policy";fi
    fi
  fi
  if [ "$APPLY" = 1 ] && [ -n "$exclude_entries" ]; then
    mkdir -p "$(dirname "$excluded")"
    updated=0
    oldend=
    if [ -s "$excluded" ]; then
      oldend=$(tail -c 1 "$excluded" | od -An -tu1 | tr -d ' ')
    fi
    if [ -s "$excluded" ] && [ "$oldend" != 10 ]; then printf '\n' >> "$excluded";fi
    oldIFS=$IFS
    IFS='
'
    for entry in $exclude_entries; do
      IFS=$oldIFS
      if [ ! -e "$excluded" ] || ! grep -Fx "$entry" "$excluded" >/dev/null; then
        printf '%s\n' "$entry" >> "$excluded"
        updated=1
      fi
      IFS='
'
    done
    IFS=$oldIFS
    [ "$updated" -eq 0 ] || printf 'UPDATED %s\n' "$excluded"
  fi
  ;;
doc)
  need brain "$BRAIN";need feature "$FEATURE";need kind "$KIND";slug "$FEATURE"
  [ -n "$NAME" ] || NAME=$FEATURE;slug "$NAME"
  case "$KIND" in
    execution|planning-index|planning-ticket|diagnosis|review) scaffold "$KIND" "$FEATURE" "$NAME";exit 0;;
    brief) num=01;folder=01-brief;prefix=BRF;;
    specification) num=02;folder=02-specifications;prefix=SPEC;;
    component) num=03;folder=03-components;prefix=CMP;;
    plan) num=04;folder=04-implementation-plans;prefix=PLAN;;
    task) num=05;folder=05-tasks;prefix=TASK;;
    *) die "unknown kind: $KIND";;
  esac
  [ "$KIND" != brief ] || [ -z "$PARENTS" ] || die 'brief cannot have parents'
  case "$KIND" in brief|specification) :;; *) [ -n "$PARENTS" ] || die 'missing parent';; esac
  tmp=$(mktemp -d);trap 'rm -rf "$tmp"' 0 HUP INT TERM
  area=$BRAIN/features/$FEATURE
  : > "$tmp/ids"
  for dir in 01-brief 02-specifications 03-components 04-implementation-plans 05-tasks;do
    for f in "$area/$dir"/*.md;do [ -f "$f" ] || continue
      awk -v folder="$dir" '/^id: / {print $2,folder;exit}' "$f" >> "$tmp/ids"
    done
  done
  awk '{if(seen[$1]++)exit 1}' "$tmp/ids" || die 'duplicate existing ID'
  for parent in $PARENTS; do
    [ "$(printf '%s\n' $PARENTS | grep -Fx -c "$parent")" -eq 1 ] ||
      die "duplicate parent ID: $parent"
  done
  for parent in $PARENTS;do
    prior=$(awk -v x="$parent" '$1==x {print $2}' "$tmp/ids")
    case "$prior:$num" in
      01-brief:02|01-brief:03|01-brief:04|01-brief:05|02-specifications:03|02-specifications:04|02-specifications:05|03-components:04|03-components:05|04-implementation-plans:05) :;;
      *) die "unknown or invalid parent: $parent";;
    esac
  done
  next=$(awk -v pre="$prefix" '$1 ~ ("^"pre"-[0-9][0-9][0-9]$") {split($1,a,"-");if(a[2]+0>m)m=a[2]+0} END{print m+1}' "$tmp/ids")
  [ "$next" -le 999 ] || die 'exhausted IDs'
  id=$(printf '%s-%03d' "$prefix" "$next")
  case "$KIND" in brief) filename=brief.md;;task)filename=$id-$NAME.md;;*)filename=$NAME.md;;esac
  target=$area/$folder/$filename
  [ ! -e "$target" ] || die "existing document: $target"
  awk -v num="$num" -v id="$id" -v parents="$PARENTS" -v kind="$KIND" -v feature="$FEATURE" '
    BEGIN {fence=sprintf("%c%c%c",96,96,96);list="[";n=split(parents,a," ");for(i=1;i<=n;i++)if(a[i]!=""){if(list!="[")list=list", ";list=list a[i]}list=list"]"}
    /^## / && $2==num{active=1;next}
    active && index($0,fence"markdown")==1 {inside=1;next}
    active && inside && index($0,fence)==1 {exit}
    active && inside{
      if($0~/^id: /){print "id: "id;next}
      if($0~/^status: /){print "status: draft";next}
      if($0~/^parents: /){print "parents: "list;next}
      if($0~/^(requirements|depends_on|parent_hashes): /){split($0,b,":");print b[1]": []";next}
      if(kind=="specification"&&$0~/^- (REQ-[0-9][0-9][0-9]|E[0-9]+): /)next
      title=feature;gsub(/-/," ",title);parts=split(title,words," ");title="";for(w=1;w<=parts;w++)title=title (w>1?" ":"") toupper(substr(words[w],1,1)) substr(words[w],2);gsub(/<Feature area>|<Feature>/,title);print
    }' "$REFS/feature-document-templates.md" > "$tmp/doc"
  [ -s "$tmp/doc" ] || die 'missing template'
  put "$target" "$tmp/doc"
  ;;
git)
  if [ "$PENDING" = 1 ];then
    need brain "$BRAIN"
    [ -n "$BRANCH" ] || BRANCH=$(git -C "$REPO" branch --show-current)
    case "$BRANCH" in ''|*..*|*[!a-zA-Z0-9._/-]*) die 'invalid branch';; esac
    mapped=$(printf '%s' "$BRANCH" | sed 's|/|--|g')
    target=$BRAIN/pending/$mapped.md
    if [ -f "$target" ];then
      grep -Fx "Branch: $BRANCH" "$target" >/dev/null || die "pending filename collision: $target"
      printf 'UNCHANGED %s\n' "$target";exit 0
    fi
    [ -n "$DATE" ] || DATE=$(date -u '+%Y-%m-%d')
    tmp=$(mktemp);trap 'rm -f "$tmp"' 0 HUP INT TERM
    sed -e "s|{{BRANCH}}|$BRANCH|g" -e "s|{{DATE}}|$DATE|g" "$HERE/scaffolds/pending.md" > "$tmp"
    put "$target" "$tmp"
    exit 0
  fi
  printf 'BRANCH %s\n' "$(git -C "$REPO" branch --show-current)"
  printf 'HEAD %s\n' "$(git -C "$REPO" rev-parse HEAD)"
  git -C "$REPO" status --porcelain --untracked-files=all | sed 's/^/STATUS /'
  git -C "$REPO" diff --cached --name-status | sed 's/^/STAGED /'
  git -C "$REPO" diff --name-status | sed 's/^/UNSTAGED /'
  if [ -n "$SINCE" ]; then
    git -C "$REPO" cat-file -e "$SINCE^{commit}" || die 'invalid revision'
    git -C "$REPO" diff --name-status "$SINCE" HEAD | sed 's/^/COMMITTED /'
  fi
  ;;
record)
  need brain "$BRAIN";need feature "$FEATURE";need event "$EVENT";need detail "$DETAIL"
  slug "$FEATURE";slug "$EVENT"
  target=$BRAIN/features/$FEATURE/execution.md
  [ -f "$target" ] || die "execution record missing: $target"
  grep -Fx '## Checkpoints' "$target" >/dev/null || die 'missing Checkpoints heading'
  entry="- $EVENT: $DETAIL"
  if grep -Fx -- "$entry" "$target" >/dev/null; then printf 'UNCHANGED %s\n' "$target";exit 0;fi
  if [ "$APPLY" != 1 ]; then printf 'APPEND %s (dry-run)\n' "$target";exit 0;fi
  guard "$target";printf '%s\n' "$entry" >> "$target";printf 'APPENDED %s\n' "$target"
  ;;
context)
  need brain "$BRAIN";[ -f "$BRAIN/00_index.md" ] || die "not a Brain: $BRAIN"
  if [ -n "$SELECT" ]; then
    case "$SELECT" in /*|..|../*|*/../*|*/..) die 'invalid context selection';; esac
    target=$BRAIN/$SELECT
    [ -f "$target" ] || die "context document missing: $SELECT"
    [ ! -L "$target" ] || die "context selection escapes Brain"
    root_real=$(CDPATH= cd -- "$BRAIN" && pwd -P) || die 'Brain inaccessible'
    parent_real=$(CDPATH= cd -- "$(dirname "$target")" && pwd -P) || die 'document parent inaccessible'
    case "$parent_real" in "$root_real"|"$root_real"/*) :;; *) die 'context selection escapes Brain';; esac
    cat "$target";exit 0
  fi
  SUMFILE=$(mktemp);trap 'rm -f "$SUMFILE"' 0 HUP INT TERM
  : > "$SUMFILE"
  for p in "$BRAIN"/*.md;do
    [ -f "$p" ] || continue
    case "$p" in */README.md|*/USAGE.md)continue;;esac
    emit_context_doc "$p" "$(basename "$p")"
  done
  if [ -n "$BRANCH" ]; then
    safe=$(printf '%s' "$BRANCH" | sed 's|/|--|g')
    case "$safe" in ''|*..*|*[!a-zA-Z0-9._-]*) die 'invalid branch';; esac
    f=$BRAIN/pending/$safe.md
    [ ! -f "$f" ] || emit_context_doc "$f" "pending/$safe.md"
  fi
  if [ -n "$FEATURE" ]; then
    slug "$FEATURE";dir=$BRAIN/features/$FEATURE
    if [ -d "$dir" ]; then
      find "$dir" -type f -name '*.md' | LC_ALL=C sort | while IFS= read -r p;do
        n=$(printf '%s' "$p" | sed "s|^$BRAIN/||")
        emit_context_doc "$p" "$n"
      done
    fi
  fi
  if [ "$ESTIMATE" = 1 ]; then
    awk '{total+=$1} END {printf "ESTIMATE bytes=%d tokens~=%d (approximate)\n",total,int((total+3)/4)}' "$SUMFILE"
  fi
  ;;
validate)
  need brain "$BRAIN"
  tmp=$(mktemp -d);trap 'rm -rf "$tmp"' 0 HUP INT TERM
  : > "$tmp/manifest"
  if [ -d "$BRAIN/features" ]; then
    find "$BRAIN/features" -type f -name '*.md' | LC_ALL=C sort | while IFS= read -r p; do
      case "$p" in */01-brief/*|*/02-specifications/*|*/03-components/*|*/04-implementation-plans/*|*/05-tasks/*) :;; *) continue;; esac
      feature=$(basename "$(dirname "$(dirname "$p")")")
      sha=$(git hash-object "$p") || die 'Git required for document hashes'
      awk -v file="$p" -v feature="$feature" -v hash="$sha" -f "$HERE/brain-tool-scan.awk" "$p"
    done > "$tmp/manifest"
  fi
  if [ -n "$HASHFILE" ]; then
    [ -f "$HASHFILE" ] || die "document not found: $HASHFILE"
    ref=$(awk -F '\t' -v f="$HASHFILE" '$1=="DOC" && $11==f {print $6}' "$tmp/manifest")
    result=
    oldIFS=$IFS;IFS=,
    for parent in $ref; do
      IFS=$oldIFS
      parent=$(printf '%s' "$parent" | tr -d ' ')
      [ -n "$parent" ] || continue
      hash=$(awk -F '\t' -v id="$parent" '$1=="DOC" && $3==id {print $10}' "$tmp/manifest")
      [ -n "$hash" ] || die "unknown parent: $parent"
      result="$result$( [ -z "$result" ] || printf ', ' )$parent@$hash"
      IFS=,
    done
    IFS=$oldIFS
    printf 'parent_hashes: [%s]\n' "$result"
    exit 0
  fi
  awk -F '\t' -v check_coverage="$COVERAGE" -v affected="$AFFECTED" -f "$HERE/brain-tool-validate.awk" "$tmp/manifest" || die 'feature-document error(s)'
  ;;
*) die "unknown command: $family";;
esac
