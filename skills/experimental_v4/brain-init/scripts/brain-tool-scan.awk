# Normalize one feature document into TSV for the POSIX awk graph validator.
# Parameters: -v file=... -v feature=... -v hash=...
BEGIN {inside=0;header=0;errored=0;id="";kind="";status="";parents="";requirements="";depends_on="";parent_hashes="";field=""}
FNR==1 && $0!="---" {print "ERROR\t"file": missing opening frontmatter";errored=1}
errored {next}
!header && $0=="---" {header=1;next}
header && $0=="---" {header=0;inside=1;next}
header {
  if($0 ~ /^[ \t]*$/ || $0 ~ /^[ \t]*#/)next
  if($0 ~ /^[a-z_]+:/){
    field=$0;sub(/:.*/,"",field)
    value=$0;sub(/^[a-z_]+:[ \t]*/,"",value)
    gsub(/^[ \t]+|[ \t]+$/,"",value)
    if(value=="[]")value=""
    else if(value ~ /^\[/ && value ~ /\]$/){value=substr(value,2,length(value)-2);gsub(/, */ ,",",value)}
    else if(field=="parents"||field=="requirements"||field=="depends_on"||field=="parent_hashes"){
      if(value!=""){print "ERROR\t"file": unsupported list syntax";errored=1}
    }
    if(field=="id")id=value
    if(field=="kind")kind=value
    if(field=="status")status=value
    if(field=="parents")parents=value
    if(field=="requirements")requirements=value
    if(field=="depends_on")depends_on=value
    if(field=="parent_hashes")parent_hashes=value
    next
  }
  if($0 ~ /^  - /){
    v=substr($0,5)
    if(field=="parents")parents=parents (parents!=""?",":"") v
    else if(field=="requirements")requirements=requirements (requirements!=""?",":"") v
    else if(field=="depends_on")depends_on=depends_on (depends_on!=""?",":"") v
    else if(field=="parent_hashes")parent_hashes=parent_hashes (parent_hashes!=""?",":"") v
    else {print "ERROR\t"file": unsupported list";errored=1}
    next
  }
  print "ERROR\t"file": unsupported frontmatter: "$0;errored=1
  next
}
inside && kind=="specification" && $0 ~ /^[-*] REQ-[0-9][0-9][0-9]:/ {
  value=$2;sub(/:$/,"",value);print "REQ\t"feature"\t"id"\t"value
}
END {
 if(errored)exit
 if(!inside||id==""||kind==""||status==""){print "ERROR\t"file": missing required frontmatter";exit}
 print "DOC\t"feature"\t"id"\t"kind"\t"status"\t"parents"\t"requirements"\t"depends_on"\t"parent_hashes"\t"hash"\t"file
}