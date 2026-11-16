# POSIX awk implementation of the conservative Brain context plan.
# Input lines are tab-delimited tagged DOC, MAP, FEATURE, PATH, BRANCH, NO_MAP, BAD_HEADER.
BEGIN { FS="\t"; OFS="\t"; map_error=""; docs_count=0; feature_count=0; path_count=0; branch="" }
$1=="DOC" {
  name=$2;digest[name]=$3;size[name]=$4+0;docs[++docs_count]=name
  known[name]=1;total+=size[name]
  if(name !~ /^features\// && name !~ /^pending\//)expected[name]=1
  next
}
$1=="MAP" {
  name=$2;mode=$3;selectors=$4;hash=$5
  if(name in mapping){map_error="duplicate-map-path";next}
  if(name ~ /^\// || name ~ /(^|\/)\.\.(\/|$)/ || name ~ /(^|\/)\.(\/|$)/ || name !~ /^[A-Za-z0-9_./ -]+$/){map_error="invalid-map-path";next}
  if(mode=="global"){if(selectors!="-"){map_error="invalid-global-selector";next}}
  else if(mode=="scoped"){
    if(selectors==""||selectors=="-"){map_error="invalid-scope";next}
    count=split(selectors,parts,";")
    for(i=1;i<=count;i++){
      if(parts[i] ~ /^feature:[a-z0-9]+(-[a-z0-9]+)*$/)continue
      if(parts[i] ~ /^path:[A-Za-z0-9_./ -]+$/ && parts[i] !~ /\.\./)continue
      map_error="invalid-scope"
    }
  }else{map_error="invalid-map-mode";next}
  if(length(hash)!=40||hash !~ /^[0-9a-f]+$/){map_error="invalid-map-hash";next}
  if(!(name in known)||digest[name]!=hash){map_error="stale-map";next}
  mapping[name]=mode;scopes[name]=selectors
  next
}
$1=="FEATURE" {features[++feature_count]=$2;next}
$1=="PATH" {paths[++path_count]=$2;next}
$1=="BRANCH" {branch=$2;next}
$1=="NO_MAP" {map_error="missing-map";next}
$1=="BAD_HEADER" {map_error="invalid-map-header";next}
$1=="BAD_ROW" {map_error="invalid-map-row";next}
function selector_match(selectors,f,p, a,n,j,v) {
  n=split(selectors,a,";")
  for(j=1;j<=n;j++){
    v=a[j]
    if(substr(v,1,8)=="feature:" && f!="" && substr(v,9)==f)return 1
    if(substr(v,1,5)=="path:" && p!=""){
      v=substr(v,6)
      if(p==v || p==substr(v,1,length(v)-1)&&substr(v,length(v),1)=="/")return 1
      if(substr(v,length(v),1)=="/"&&substr(p,1,length(v))==v)return 1
    }
  }
  return 0
}
function relevant(selectors, j) {
  for(j=1;j<=feature_count;j++)if(selector_match(selectors,features[j],""))return 1
  for(j=1;j<=path_count;j++)if(selector_match(selectors,"",paths[j]))return 1
  return 0
}
function root_mandatory(name) {
 return name=="00_index.md"||name=="03_architecture.md"||name=="09_user_decisions.md"||name=="open_questions.md"||name=="state.md"
}
function read_text(name, file, line, text) {
  file=brain "/" name;text=""
  while((getline line < file)>0)text=text line "\n"
  close(file)
  return text
}
END {
  reason=map_error
  if(reason=="")for(name in expected)if(!(name in mapping)){reason="incomplete-map";break}
  if(reason=="")for(name in mapping)if(!(name in expected)){reason="incomplete-map";break}
  if(reason==""&&feature_count==0&&path_count==0)reason="unknown-scope"
  if(reason==""&&branch=="")reason="unknown-branch"

  if(reason==""){
    for(i=1;i<=docs_count;i++){
      name=docs[i]
      if(root_mandatory(name))selected[name]=1
      if(branch!=""&&name=="pending/"branch_to_file(branch)".md")selected[name]=1
      for(j=1;j<=feature_count;j++)if(index(name,"features/"features[j]"/")==1)selected[name]=1
    }
    for(name in mapping)if(mapping[name]=="global"||relevant(scopes[name]))selected[name]=1
    for(i=1;i<=path_count;i++){
      found=0
      for(name in mapping)if(mapping[name]=="scoped"&&selector_match(scopes[name],"",paths[i])){found=1;break}
      if(!found){reason="unmapped-code-path";break}
    }
    if(reason=="")for(i=1;i<=feature_count;i++){
      found=0
      for(j=1;j<=docs_count;j++)if(index(docs[j],"features/"features[i]"/")==1){found=1;break}
      if(!found)for(name in mapping)if(mapping[name]=="scoped"&&selector_match(scopes[name],features[i],"")){found=1;break}
      if(!found){reason="unmapped-feature";break}
    }
    if(reason==""){
      for(i=1;i<=docs_count;i++) {
        name=docs[i]
        if(index(name,"pending/")==1&&!selected[name])continue
        text[name]=read_text(name)
      }
      for(i=1;i<=docs_count;i++){
        name=docs[i]
        if(index(name,"pending/")==1&&!selected[name])continue
        for(j=1;j<=path_count;j++)if(index(text[name],paths[j])>0)selected[name]=1
        for(j=1;j<=feature_count;j++)if(index(text[name],"features/"features[j]"/")>0)selected[name]=1
      }
      changed=1
      while(changed){
        changed=0
        for(i=1;i<=docs_count;i++){
          name=docs[i]
          if(index(name,"pending/")==1&&!selected[name])continue
          for(j=1;j<=docs_count;j++){
            other=docs[j]
            if(other==name||(index(other,"pending/")==1&&!selected[other]))continue
            if(name!="00_index.md"&&name!="state.md"&&other!="00_index.md"&&other!="state.md" &&
               index(text[name],other)>0&&(selected[name]||selected[other])){
              if(!selected[name]||!selected[other]){
                selected[name]=1;selected[other]=1;changed=1
              }
            }
          }
        }
      }
    }
  }
  mode=reason==""?"selective":"full"
  if(mode=="selective")reason="mapped-and-linked"
  print "MODE",mode
  print "REASON",reason
  amount=0
  for(i=1;i<=docs_count;i++){
    name=docs[i]
    if(mode=="full"||selected[name]){print "READ",name;amount+=size[name]}
  }
  print "BYTES",amount,total
}
function branch_to_file(value) {
 gsub(/\//,"--",value)
 return value
}
