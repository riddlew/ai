# V5 POSIX AWK validator. Legacy approval status/hash fields are inert.
BEGIN {FS="\t";bad=0}
$1=="DOC" {
 i=++count; feature[i]=$2; id[i]=$3; kind[i]=$4; parents[i]=$6; reqs[i]=$7; deps[i]=$8; filename[i]=$11; amends[i]=$12; supersedes[i]=$13
 k=feature[i] SUBSEP id[i];if(k in lookup)err(filename[i]": duplicate ID "id[i]);lookup[k]=i
 if(id[i]!~/^(BRF|SPEC|CMP|PLAN|TASK)-[0-9][0-9][0-9]$/)err(filename[i]": invalid ID")
 prefix=kind[i]=="brief"?"BRF":kind[i]=="specification"?"SPEC":kind[i]=="component"?"CMP":kind[i]=="implementation-plan"?"PLAN":kind[i]=="task"?"TASK":""
 if(prefix==""||index(id[i],prefix"-")!=1)err(filename[i]": invalid kind")
 level[i]=prefix=="BRF"?1:prefix=="SPEC"?2:prefix=="CMP"?3:prefix=="PLAN"?4:5
 next
}
$1=="REQ" {k=$2 SUBSEP $3 SUBSEP $4;if(k in declared)err("duplicate requirement " $3 "#" $4);declared[k]=1;next}
$1=="ERROR" {err($2);next}
function err(s){print "INVALID "s;bad=1}
function entries(s,a,n,j){if(s=="")return 0;n=split(s,a,",");for(j=1;j<=n;j++)gsub(/^[ \t]+|[ \t]+$/,"",a[j]);return n}
function dupe(s,file,label, a,n,j,k){n=entries(s,a);delete seen;for(j=1;j<=n;j++)if(seen[a[j]]++)err(file": duplicate "label" "a[j])}
function walk(k,field, i,n,a,j,dep,key){if(active[field SUBSEP k]){err(field" cycle at "k);return}if(done[field SUBSEP k])return;active[field SUBSEP k]=1;i=lookup[k];n=entries(field=="amends"?amends[i]:deps[i],a);for(j=1;j<=n;j++){key=feature[i] SUBSEP a[j];if(key in lookup)walk(key,field)}active[field SUBSEP k]=0;done[field SUBSEP k]=1}
function reaches(k,target, i,n,a,j,dep){if(k==target)return 1;if(trail[k]==epoch)return 0;trail[k]=epoch;i=lookup[k];if(!i)return 0;n=entries(parents[i],a);for(j=1;j<=n;j++)if(reaches(feature[i] SUBSEP a[j],target))return 1;n=entries(deps[i],a);for(j=1;j<=n;j++)if(reaches(feature[i] SUBSEP a[j],target))return 1;n=entries(amends[i],a);for(j=1;j<=n;j++)if(reaches(feature[i] SUBSEP a[j],target))return 1;return 0}
END{
 for(i=1;i<=count;i++){
  dupe(parents[i],filename[i],"parents");dupe(reqs[i],filename[i],"requirements");dupe(deps[i],filename[i],"depends_on");dupe(amends[i],filename[i],"amends");dupe(supersedes[i],filename[i],"supersedes")
  if(level[i]==1&&parents[i]!="")err(filename[i]": brief cannot have parents")
  n=entries(parents[i],a);for(j=1;j<=n;j++){p=lookup[feature[i] SUBSEP a[j]];if(!p)err(filename[i]": unknown parent "a[j]);else if(level[p]>=level[i])err(filename[i]": parent must be earlier "a[j])}
  n=entries(deps[i],a);for(j=1;j<=n;j++){p=lookup[feature[i] SUBSEP a[j]];if(!p||level[p]!=level[i]||id[i]==a[j])err(filename[i]": invalid dependency "a[j])}
  n=entries(reqs[i],a);for(j=1;j<=n;j++){split(a[j],r,"#");if(!((feature[i] SUBSEP r[1] SUBSEP r[2]) in declared))err(filename[i]": unknown requirement "a[j])}
  if((amends[i]=="")!=(supersedes[i]==""))err(filename[i]": amendments require amends and supersedes")
  n=entries(amends[i],a);for(j=1;j<=n;j++){p=lookup[feature[i] SUBSEP a[j]];if(!p||level[p]!=level[i]||id[i]==a[j])err(filename[i]": invalid amendment target "a[j])}
  n=entries(supersedes[i],a);for(j=1;j<=n;j++){
   split(a[j],r,"#");allowed=0;m=entries(amends[i],b);for(q=1;q<=m;q++)if(b[q]==r[1])allowed=1
   if(!allowed||r[2]=="")err(filename[i]": invalid supersession "a[j])
   claim=feature[i] SUBSEP a[j];if(claim in claims)err(filename[i]": conflicting supersession "a[j]);claims[claim]=id[i]
  }
 }
 for(i=1;i<=count;i++){walk(feature[i] SUBSEP id[i],"depends_on");walk(feature[i] SUBSEP id[i],"amends")}
 if(check_coverage){for(i=1;i<=count;i++)if(level[i]==2){spec=id[i];for(l=3;l<=5;l++){parts=0;covered=",";for(j=1;j<=count;j++)if(feature[j]==feature[i]&&level[j]==l){member=0;n=entries(parents[j],a);for(z=1;z<=n;z++)if(a[z]==spec)member=1;n=entries(reqs[j],a);for(z=1;z<=n;z++)if(index(a[z],spec"#")==1)member=1;if(member){parts++;covered=covered reqs[j] ","}}if(parts)for(k in declared){split(k,r,SUBSEP);if(r[1]==feature[i]&&r[2]==spec&&index(covered,spec"#"r[3])==0)err("no document covers "spec"#"r[3])}}}}
 if(affected!=""){hits=0;for(i=1;i<=count;i++)if(id[i]==affected){hits++;root=feature[i] SUBSEP id[i];source=i}if(hits!=1)err("ID not unique or unknown "affected);else for(i=1;i<=count;i++)if(i!=source&&feature[i]==feature[source]){epoch++;if(reaches(feature[i] SUBSEP id[i],root))print "AFFECTED "id[i]" "filename[i]}}
 if(bad)exit 1;if(affected=="")print "VALID feature documents"
}
