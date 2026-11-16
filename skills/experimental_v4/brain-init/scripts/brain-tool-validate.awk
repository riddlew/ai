# POSIX awk feature graph validator. Input: normalized TSV manifest from brain-tool.sh.
BEGIN {FS="\t"; OFS="\t"; bad=0}
$1=="DOC" {
  i=++count
  feature[i]=$2; id[i]=$3; kind[i]=$4; status[i]=$5
  parents[i]=$6; requirements[i]=$7; deps[i]=$8; hashes[i]=$9
  digest[i]=$10; filename[i]=$11
  key=feature[i] SUBSEP id[i]
  if(key in lookup){print "INVALID " filename[i] ": duplicate id " id[i];bad=1}
  lookup[key]=i
  if(id[i] !~ /^(BRF|SPEC|CMP|PLAN|TASK)-[0-9][0-9][0-9]$/){print "INVALID " filename[i] ": invalid id " id[i];bad=1}
  if(status[i]!="draft"&&status[i]!="approved"&&status[i]!="needs-revision"){print "INVALID "filename[i]": invalid status";bad=1}
  prefix=kind[i]=="brief"?"BRF":kind[i]=="specification"?"SPEC":kind[i]=="component"?"CMP":kind[i]=="implementation-plan"?"PLAN":kind[i]=="task"?"TASK":""
  if(prefix==""||index(id[i],prefix"-")!=1){print "INVALID "filename[i]": incorrect kind";bad=1}
  level[i]=prefix=="BRF"?1:prefix=="SPEC"?2:prefix=="CMP"?3:prefix=="PLAN"?4:5
  next
}
$1=="REQ" {key=$2 SUBSEP $3 SUBSEP $4;if(key in declared){print "INVALID duplicate requirement: "$3"#"$4;bad=1} declared[key]=1;next}
$1=="ERROR" {print "INVALID "$2;bad=1;next}
function entries(s,a, count) {
  if(s=="")return 0
  count=split(s,a,",")
  for(var=1;var<=count;var++)gsub(/^[ \t]+|[ \t]+$/,"",a[var])
  return count
}
function add_error(s) {print "INVALID "s;bad=1}
function check_duplicates(value, file, label, a, count, k, scope, item) {
  scope=++duplicate_epoch
  count=entries(value,a)
  for(k=1;k<=count;k++){
    item=scope SUBSEP a[k]
    if(duplicate_seen[item]++)add_error(file ": duplicate " label ": " a[k])
  }
}
function reach(k, target, j,n,a,z,p,seen) {
  if(k==target)return 1
  if(trail[k]==visit_epoch)return 0
  trail[k]=visit_epoch
  j=lookup[k]
  if(!j)return 0
  n=entries(parents[j],a)
  for(z=1;z<=n;z++)if(reach(feature[j] SUBSEP a[z],target))return 1
  n=entries(deps[j],a)
  for(z=1;z<=n;z++)if(reach(feature[j] SUBSEP a[z],target))return 1
  return 0
}
function cycle(k, a,n,j,z,d) {
  if(active[k]){add_error("dependency cycle: "k);return}
  if(visited[k])return
  active[k]=1;j=lookup[k]
  n=entries(deps[j],a)
  for(z=1;z<=n;z++){d=feature[j] SUBSEP a[z];if(d in lookup)cycle(d)}
  active[k]=0;visited[k]=1
}
END {
  for(i=1;i<=count;i++) {
    k=feature[i] SUBSEP id[i]
    check_duplicates(parents[i],filename[i],"parents")
    check_duplicates(deps[i],filename[i],"depends_on")
    check_duplicates(requirements[i],filename[i],"requirements")
    check_duplicates(hashes[i],filename[i],"parent_hashes")
    m=entries(hashes[i],h)
    for(z=1;z<=m;z++){
      hash_parts=split(h[z],pair,"@")
      if(hash_parts!=2||pair[1]!~/^(BRF|SPEC|CMP|PLAN|TASK)-[0-9][0-9][0-9]$/||
         length(pair[2])!=40||pair[2]!~/^[0-9a-f]+$/)
        add_error(filename[i]": malformed parent hash "h[z])
      allowed=0;n=entries(parents[i],ids)
      for(q=1;q<=n;q++)if(ids[q]==pair[1])allowed=1
      if(!allowed)add_error(filename[i]": parent hash for non-parent "pair[1])
    }
    n=entries(parents[i],a)
    for(j=1;j<=n;j++){
      p=a[j];parent=lookup[feature[i] SUBSEP p]
      if(parent==0){add_error(filename[i]": unknown parent "p);continue}
      if(level[parent]>=level[i])add_error(filename[i]": parent must be earlier: "p)
      if(status[i]=="approved"){
        if(status[parent]!="approved")add_error(filename[i]": unapproved parent "p)
        found=0;m=entries(hashes[i],h)
        for(z=1;z<=m;z++)if(h[z]==p"@"digest[parent])found=1
        if(!found)add_error(filename[i]": stale/missing parent hash: "p)
      }
    }
    if(level[i]==1&&parents[i]!="")add_error(filename[i]": brief cannot have parents")
    n=entries(deps[i],a)
    for(j=1;j<=n;j++){
      p=a[j];d=lookup[feature[i] SUBSEP p]
      if(d==0||level[d]!=level[i]||id[i]==p)add_error(filename[i]": invalid dependency "p)
      else if(status[i]=="approved"&&status[d]!="approved")add_error(filename[i]": unapproved dependency "p)
    }
    n=entries(requirements[i],a)
    for(j=1;j<=n;j++){
      ref=a[j];ref_parts=split(ref,r,"#")
      if(ref_parts!=2||!((feature[i] SUBSEP r[1] SUBSEP r[2]) in declared))add_error(filename[i]": unknown requirement "ref)
      else if(level[i]>=3&&parents[i]!=""){
        supported=0;m=entries(parents[i],pids)
        for(z=1;z<=m;z++){
          parent=lookup[feature[i] SUBSEP pids[z]]
          if(parent==0)continue
          if(pids[z]==r[1])supported=1
          mm=entries(requirements[parent],parentreq)
          for(q=1;q<=mm;q++)if(parentreq[q]==ref)supported=1
        }
        if(!supported)add_error(filename[i]": unsupported requirement "ref)
      }
    }
    if(level[i]>=3&&requirements[i]!=""&&parents[i]=="")add_error(filename[i]": requirement needs parent")
  }
  for(i=1;i<=count;i++)cycle(feature[i] SUBSEP id[i])
  if(check_coverage){
    for(i=1;i<=count;i++)if(level[i]==2&&status[i]=="approved"){
      spec=id[i]
      for(l=3;l<=5;l++){
        participants=0;unfinished=0;covered=""
        for(j=1;j<=count;j++)if(feature[j]==feature[i]&&level[j]==l){
          member=0;n=entries(parents[j],a);for(z=1;z<=n;z++)if(a[z]==spec)member=1
          n=entries(requirements[j],a);for(z=1;z<=n;z++)if(index(a[z],spec"#")==1)member=1
          if(member){participants++;if(status[j]!="approved")unfinished=1;covered=covered","requirements[j]","}
        }
        if(participants&&!unfinished)for(d in declared){
          split(d,parts,SUBSEP)
          if(parts[1]==feature[i]&&parts[2]==spec&&index(covered,","spec"#"parts[3]",")==0)add_error("no approved document covers "spec"#"parts[3])
        }
      }
    }
  }
  if(affected!=""){
    matches=0;seed=""
    for(i=1;i<=count;i++)if(id[i]==affected){matches++;seed=feature[i] SUBSEP id[i];seed_i=i}
    if(matches!=1)add_error("ID not unique or unknown: "affected)
    else for(i=1;i<=count;i++)if(i!=seed_i&&feature[i]==feature[seed_i]){
      visit_epoch++
      if(reach(feature[i] SUBSEP id[i],seed))print "AFFECTED "id[i]" "filename[i]
    }
  }
  if(bad)exit 1
  if(affected=="")print "VALID feature documents"
}