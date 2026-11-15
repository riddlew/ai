#!/bin/sh
# POSIX shell fallback; no Python, Node, jq, or npm packages.
set -eu
HERE=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REFS=$HERE/../references
die() { printf 'ERROR %s\n' "$*" >&2; exit 1; }
need() { [ -n "$2" ] || die "--$1 is required"; }
slug() { case "$1" in ''|*[!a-z0-9-]*|*-|-*|*--) die "invalid slug: $1";; esac; }
abs() { case "$1" in /*) printf '%s\n' "$1";; *) printf '%s/%s\n' "$PWD" "$1";; esac; }
guard() {
  [ -n "$AUTHORIZED" ] || die '--authorized-root is required for --apply'
  case "$1" in "$AUTHORIZED"|"$AUTHORIZED"/*) :;; *) die "outside authorized write root: $1";; esac
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
scaffold() {
  kind=$1;feature=$2;name=$3
  title=$(printf '%s' "$name" | awk -F- '{for(i=1;i<=NF;i++){w=$i;printf "%s%s",i==1?"":" ",toupper(substr(w,1,1)) substr(w,2)}printf "\n"}')
  case "$kind" in
    execution) target=$BRAIN/features/$feature/execution.md;;
    planning-index) target=$BRAIN/planning/$feature/INDEX.md;;
    planning-ticket)
      dir=$BRAIN/planning/$feature
      n=$(find "$dir" -maxdepth 1 -name '[0-9]*-*.md' -type f 2>/dev/null | awk -F/ '{split($NF,a,"-");if(a[1]+0>m)m=a[1]+0}END{print m+1}')
      [ -n "$n" ] || n=1
      num=$(printf '%03d' "$n");target=$dir/$num-$name.md;;
    diagnosis)
      dir=$BRAIN/diagnoses
      n=$(find "$dir" -maxdepth 1 -name '[0-9]*-*.md' -type f 2>/dev/null | awk -F/ '{split($NF,a,"-");if(a[1]+0>m)m=a[1]+0}END{print m+1}')
      [ -n "$n" ] || n=1
      num=$(printf '%02d' "$n");target=$dir/$num-$name.md;;
    review)
      case "$REPORTTYPE" in architecture|code|merge-request|security) :;; *) die 'invalid or missing --report-type';; esac
      dir=$BRAIN/reviews/$REPORTTYPE
      n=$(find "$dir" -maxdepth 1 -name '[0-9]*-*' 2>/dev/null | awk -F/ '{split($NF,a,"-");if(a[1]+0>m)m=a[1]+0}END{print m+1}')
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
family=help
if [ "$#" -gt 0 ]; then family=$1;shift;fi
case "$family" in help|--help|-h) echo 'brain-tool <init|doc|validate|git|record|context> [options]';exit 0;; esac
case "${1:-}" in new|list|summary) shift;; esac
PENDING=0 BRAIN= FEATURE= KIND= NAME= REPO=. AUTHORIZED= APPLY=0 TRACKING=ignored REVISION= DATE= MAIN=main PARENTS= SINCE= AFFECTED= HASHFILE= COVERAGE=0 EVENT= DETAIL= BRANCH= REPORTTYPE=
while [ "$#" -gt 0 ]; do
  arg=$1;shift
  case "$arg" in
    --apply) APPLY=1;; --check-coverage) COVERAGE=1;; --pending) PENDING=1;;
    --brain|--feature|--kind|--slug|--repo|--authorized-root|--tracking|--revision|--at|--main-branch|--parent|--since|--affected|--show-parent-hashes|--event|--detail|--branch|--report-type)
      [ "$#" -gt 0 ] || die "missing value for $arg"
      v=$1;shift
      case "$arg" in
        --brain) BRAIN=$v;; --feature) FEATURE=$v;; --kind) KIND=$v;; --slug) NAME=$v;;
        --repo) REPO=$v;; --authorized-root) AUTHORIZED=$v;; --tracking) TRACKING=$v;;
        --revision) REVISION=$v;; --at) DATE=$v;; --main-branch) MAIN=$v;;
        --parent) PARENTS="$PARENTS $v";; --since) SINCE=$v;; --affected) AFFECTED=$v;;
        --show-parent-hashes) HASHFILE=$v;; --event) EVENT=$v;; --detail) DETAIL=$v;; --branch) BRANCH=$v;; --report-type) REPORTTYPE=$v;;
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
    [ ! -e "$target" ] || cmp -s "$REFS/$name" "$target" || die "existing content differs: $target"
  done
  [ -f "$index" ] || put "$index" "$tmp/index"
  put "$BRAIN/USAGE.md" "$REFS/USAGE.md"
  put "$BRAIN/README.md" "$REFS/README.md"
  if [ ! -e "$REPO/CLAUDE.local.md" ]; then put "$REPO/CLAUDE.local.md" "$REFS/CLAUDE.local.md"
  elif ! cmp -s "$REPO/CLAUDE.local.md" "$REFS/CLAUDE.local.md"; then
    echo 'REVIEW existing CLAUDE.local.md; preserve custom policy'
  fi
  if [ "$APPLY" = 1 ] && [ "$TRACKING" = ignored ]; then
    common=$(git -C "$REPO" rev-parse --path-format=absolute --git-common-dir) || die 'Git metadata unavailable'
    excluded=$common/info/exclude;guard "$excluded"
    if [ ! -e "$excluded" ] || ! grep -Fx '.brain/' "$excluded" >/dev/null; then
      mkdir -p "$(dirname "$excluded")";printf '.brain/\n' >> "$excluded";printf 'UPDATED %s\n' "$excluded"
    fi
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
    sed -e "s/{{BRANCH}}/$BRANCH/g" -e "s/{{DATE}}/$DATE/g" "$HERE/scaffolds/pending.md" > "$tmp"
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
  for p in "$BRAIN"/*.md;do
    [ -f "$p" ] || continue
    case "$p" in */README.md|*/USAGE.md)continue;;esac
    name=$(basename "$p");size=$(wc -c < "$p" | tr -d ' ')
    status=$(sed -n 's/^status: //p' "$p" | head -1);[ -n "$status" ] || status=-
    printf 'DOC %s\t%s\t%s\n' "$name" "$size" "$status"
  done
  if [ -n "$BRANCH" ]; then
    safe=$(printf '%s' "$BRANCH" | sed 's|/|--|g');slug "$safe"
    f=$BRAIN/pending/$safe.md
    [ ! -f "$f" ] || printf 'DOC pending/%s.md\t%s\t-\n' "$safe" "$(wc -c < "$f" | tr -d ' ')"
  fi
  if [ -n "$FEATURE" ]; then
    slug "$FEATURE";dir=$BRAIN/features/$FEATURE
    if [ -d "$dir" ]; then
      find "$dir" -type f -name '*.md' | LC_ALL=C sort | while IFS= read -r p;do
        n=$(printf '%s' "$p" | sed "s|^$BRAIN/||")
        bytes=$(wc -c < "$p" | tr -d ' ')
        status=$(sed -n 's/^status: //p' "$p" | head -1);[ -n "$status" ] || status=-
        printf 'DOC %s\t%s\t%s\n' "$n" "$bytes" "$status"
      done
    fi
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
