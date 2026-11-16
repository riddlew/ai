#!/usr/bin/env node
// Built-ins only. Deterministic Brain operations; approvals are never inferred.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import cp from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=path.dirname(fileURLToPath(import.meta.url));
const refs=path.resolve(root,'../references');
const kinds={brief:['01','01-brief','BRF','brief'],specification:['02','02-specifications','SPEC','specification'],component:['03','03-components','CMP','component'],plan:['04','04-implementation-plans','PLAN','implementation-plan'],task:['05','05-tasks','TASK','task']};
function fail(s){throw Error(s)}
const read=p=>fs.readFileSync(p,'utf8'),exists=p=>fs.existsSync(p);
const full=p=>path.resolve(p.startsWith('~')?path.join(os.homedir(),p.slice(1)):p);
const isSlug=s=>/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(s);
function slug(s){if(!isSlug(s))fail('invalid slug: '+s);return s}
function opts(args){let o={parent:[]};const flags=new Set(['apply','check-coverage','pending','estimate','hashes','save-location']);const values=new Set(['brain','repo','tracking','revision','at','main-branch','parent','feature','kind','slug','authorized-root','affected','show-parent-hashes','since','event','detail','branch','report-type','select']);for(let i=0;i<args.length;i++){if(!args[i].startsWith('--'))fail('unexpected argument: '+args[i]);let k=args[i].slice(2);if(flags.has(k)){o[k]=true;continue}if(!values.has(k))fail('unknown option: --'+k);if(!args[i+1]||args[i+1].startsWith('--'))fail('missing value for --'+k);if(k==='parent')o.parent.push(args[++i]);else o[k]=args[++i]}return o}
function req(o,k){if(!o[k])fail('--'+k+' is required');return o[k]}
const brain=o=>full(req(o,'brain'));
function git(repo,...args){let r=cp.spawnSync('git',['-C',repo,...args],{encoding:'utf8'});if(r.status!==0)fail('git '+args.join(' ')+' failed: '+(r.stderr||'').trim());return r.stdout.trim()}
function scope(p,o){if(!o['authorized-root'])fail('--authorized-root is required for --apply');let r=full(o['authorized-root']),d=full(p);if(d!==r&&!d.startsWith(r+path.sep))fail('outside authorized write root: '+p);
 let x=d;while(!exists(x)){let y=path.dirname(x);if(y===x)break;x=y}if(exists(x)){let actual=fs.realpathSync(x);let effective=exists(r)?fs.realpathSync(r):r;if(actual!==effective&&!actual.startsWith(effective+path.sep))fail('symlink escapes authorized root: '+p)}}
function changes(items,o){for(let [p,s] of items){if(o.apply)scope(p,o);if(exists(p)&&(!fs.statSync(p).isFile()||read(p)!==s))fail('existing content differs: '+p)}for(let [p,s] of items){if(exists(p))console.log('UNCHANGED '+p);else if(!o.apply)console.log('CREATE '+p+' (dry-run)');else{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s,{flag:'wx'});console.log('CREATED '+p)}}}
function init(o){let b=brain(o),repo=full(o.repo||'.'),mode=o.tracking||'ignored';if(!['tracked','ignored'].includes(mode))fail('invalid tracking mode');
 let idx=path.join(b,'00_index.md'),original=exists(idx)?read(idx):null,day=o.at||new Date().toISOString().slice(0,10);
 let index=original??('# Project Brain Index\n\nLast synced: '+(o.revision||git(repo,'rev-parse','HEAD'))+' ('+day+')\nGit: '+mode+'\nMain branch: '+(o['main-branch']||'main')+'\n\n## Root files\n\n| File | Purpose | Status |\n|---|---|---|\n\n## Documents\n\n| Path | Purpose | Status |\n|---|---|---|\n');
 let guides=[['USAGE.md','Brain Skills workflow examples and selection guide'],['README.md','Brain Skills catalog and installation reference']],tick=String.fromCharCode(96);
 for(let [f,p] of guides)if(!index.split('\n').some(l=>l.startsWith('| '+tick+f+tick+' |')))index+='| '+tick+f+tick+' | '+p+' | reference |\n';
 let items=[];for(let [f] of guides){let p=path.join(b,f),bundled=read(path.join(refs,f));if(exists(p)&&read(p)!==bundled)console.log('REVIEW existing '+p+': differs from bundled guide; preserved');else items.push([p,bundled])}
 if(original===null)items.unshift([idx,index]);else if(original!==index){if(o.apply)fail('index needs new guide rows; review update before applying');console.log('REVIEW index guide registration (existing index differs)')}
 let policy=path.join(repo,'CLAUDE.local.md'),bundled=read(path.join(refs,'CLAUDE.local.md')),append=null,saved='Project brain: '+b;
 if(exists(policy)){
   let current=read(policy);
   if(current!==bundled)console.log('REVIEW existing CLAUDE.local.md; preserve custom policy');
   if(o['save-location']){
     let lines=current.split('\n').filter(x=>x.startsWith('Project brain:'));
     if(lines.length>1||(lines.length===1&&lines[0]!==saved))fail('conflicting saved Project brain location; review before applying');
     if(!lines.length){append=(current&&!current.endsWith('\n')?'\n':'')+saved+'\n';
       if(o.apply)scope(policy,o);else console.log('APPEND '+policy+': Project brain location (dry-run)')}
   }
 }else items.push([policy,bundled+(o['save-location']?(bundled.endsWith('\n')?'':'\n')+saved+'\n':'')]);
 let ok=(...args)=>cp.spawnSync('git',['-C',repo,...args],{stdio:'ignore'}).status===0;
 let entries=[];
 if(mode==='ignored'&&b===path.join(repo,'.brain')&&!ok('check-ignore','-q','--','.brain/'))entries.push('.brain/');
 if(!ok('ls-files','--error-unmatch','--','CLAUDE.local.md')&&!ok('check-ignore','-q','--','CLAUDE.local.md'))entries.push('CLAUDE.local.md');
 let exclude=null;
 if(entries.length&&o.apply){let common=full(git(repo,'rev-parse','--path-format=absolute','--git-common-dir'));exclude=path.join(common,'info','exclude');scope(exclude,o)}
 changes(items,o);
 if(append&&o.apply){fs.appendFileSync(policy,append);console.log('UPDATED '+policy+': Project brain location')}
 if(exclude){let old=exists(exclude)?read(exclude):'',missing=entries.filter(e=>!old.split('\n').includes(e));if(missing.length){fs.mkdirSync(path.dirname(exclude),{recursive:true});fs.appendFileSync(exclude,(!old||old.endsWith('\n')?'':'\n')+missing.map(e=>e+'\n').join(''));console.log('UPDATED '+exclude)}}}
function docs(area){let found=new Map();for(let [,folder] of Object.values(kinds)){let dir=path.join(area,folder);if(!exists(dir))continue;for(let name of fs.readdirSync(dir).filter(x=>x.endsWith('.md'))){let file=path.join(dir,name),m=read(file).match(/^id:\s*((?:BRF|SPEC|CMP|PLAN|TASK)-\d{3})\s*$/m);if(m){if(found.has(m[1]))fail('duplicate existing ID: '+m[1]);found.set(m[1],{file,folder})}}}return found}
function template(kind,id,parents,feature){let raw=read(path.join(refs,'feature-document-templates.md')),begin=raw.indexOf('## '+kinds[kind][0]+' ');if(begin<0)fail('template missing');let tick=String.fromCharCode(96),fence=tick.repeat(3)+'markdown\n',pos=raw.indexOf(fence,begin);if(pos<0)fail('template block missing');let end=raw.indexOf(tick.repeat(3),pos+fence.length);if(end<0)fail('unterminated template');let text=raw.slice(pos+fence.length,end);
 for(let [k,v] of Object.entries({id,status:'draft',parents:'['+parents.join(', ')+']',requirements:'[]',depends_on:'[]',parent_hashes:'[]'}))text=text.replace(new RegExp('^'+k+':.*$','m'),k+': '+v);
 if(kind==='specification')text=text.replace(/^- (?:REQ-\d{3}|E\d+):.*\n/gm,'');
 return text.replace(/<Feature(?: area)?>/g,feature.split('-').map(s=>s[0].toUpperCase()+s.slice(1)).join(' ')).trimEnd()+'\n'}
function scaffold(o,kind,b,feature,name){
 let base=path.join(root,'scaffolds'),title=name.split('-').map(x=>x[0].toUpperCase()+x.slice(1)).join(' '),target;
 if(kind==='execution')target=path.join(b,'features',feature,'execution.md');
 else if(kind==='planning-index')target=path.join(b,'planning',feature,'INDEX.md');
 else if(kind==='planning-ticket'){
   let dir=path.join(b,'planning',feature),nums=exists(dir)?fs.readdirSync(dir).map(x=>/^(\d+)-.+\.md$/.exec(x)?.[1]).filter(Boolean).map(Number):[];
   target=path.join(dir,String(Math.max(0,...nums)+1).padStart(3,'0')+'-'+name+'.md');
 }else if(kind==='diagnosis'){
   let dir=path.join(b,'diagnoses'),nums=exists(dir)?fs.readdirSync(dir).map(x=>/^(\d+)-.+\.md$/.exec(x)?.[1]).filter(Boolean).map(Number):[];
   target=path.join(dir,String(Math.max(0,...nums)+1).padStart(2,'0')+'-'+name+'.md');
 }else if(kind==='review'){
   let type=o['report-type'];if(!['architecture','code','merge-request','security'].includes(type))fail('invalid or missing --report-type');
   let dir=path.join(b,'reviews',type),nums=exists(dir)?fs.readdirSync(dir).map(x=>/^(\d+)-.+/.exec(x)?.[1]).filter(Boolean).map(Number):[];
   target=path.join(dir,String(Math.max(0,...nums)+1).padStart(2,'0')+'-'+name,'review.md');
 }else fail('unknown kind: '+kind);
 if(exists(target))fail('existing document; refusing overwrite: '+target);
 let file=(kind==='review'?'review':kind)+'.md';
 changes([[target,read(path.join(base,file)).replaceAll('{{TITLE}}',title)]],o);
}
function doc(o){let b=brain(o),f=slug(req(o,'feature')),kind=req(o,'kind'),info=kinds[kind],name=slug(o.slug||f);if(!info){scaffold(o,kind,b,f,name);return}let area=path.join(b,'features',f),known=docs(area),parents=o.parent;
 if(kind==='brief'&&parents.length)fail('brief cannot have parents');if(!['brief','specification'].includes(kind)&&!parents.length)fail('this document needs at least one governing --parent');if(new Set(parents).size!==parents.length)fail('duplicate parent ID');
 for(let p of parents){let x=known.get(p),prior=x?Object.values(kinds).find(k=>k[1]===x.folder)?.[0]:null;if(!prior||Number(prior)>=Number(info[0]))fail('unknown or invalid earlier-level parent: '+p)}
 let nums=[...known.keys()].filter(x=>x.startsWith(info[2]+'-')).map(x=>Number(x.split('-')[1])),n=Math.max(0,...nums)+1;if(n>999)fail('exhausted IDs');
 let id=info[2]+'-'+String(n).padStart(3,'0'),namefile=kind==='brief'?'brief.md':kind==='task'?id+'-'+name+'.md':name+'.md',target=path.join(area,info[1],namefile);if(exists(target))fail('existing document; preserve its ID: '+target);changes([[target,template(kind,id,parents,f)]],o)}
function metadata(text){
 if(!text.startsWith('---\n'))fail('missing frontmatter');
 let e=text.indexOf('\n---',4);if(e<0)fail('unterminated frontmatter');
 let m={},active=null;
 const seq=['parents','requirements','depends_on','parent_hashes'];
 for(let line of text.slice(4,e).split('\n')){
  if(!line.trim()||line.trimStart().startsWith('#'))continue;
  if(line.startsWith('  - ')&&active){m[active].push(line.slice(4).trim().replace(/^['"]|['"]$/g,''));continue}
  let match=line.match(/^([a-z_]+):\s*(.*)$/);if(!match)fail('unsupported frontmatter line: '+line);
  let key=match[1],value=match[2].trim();if(Object.hasOwn(m,key))fail('duplicate metadata key: '+key);
  if(seq.includes(key)){
   if(value===''||value==='[]'){m[key]=[];active=value===''?key:null}
   else if(value.startsWith('[')&&value.endsWith(']')){m[key]=value.slice(1,-1).split(',').map(x=>x.trim().replace(/^['"]|['"]$/g,'')).filter(Boolean);active=null}
   else fail('unsupported list syntax: '+key);
  }else{m[key]=value.replace(/^['"]|['"]$/g,'');active=null}
 }
 return {meta:m,body:text.slice(e+4)}
}
function scan(b){let all=[],root=path.join(b,'features');if(!exists(root))return all;for(let feature of fs.readdirSync(root)){let area=path.join(root,feature);if(!fs.statSync(area).isDirectory())continue;for(let [kind,info] of Object.entries(kinds)){let dir=path.join(area,info[1]);if(!exists(dir))continue;for(let name of fs.readdirSync(dir).filter(x=>x.endsWith('.md'))){let file=path.join(dir,name),m=metadata(read(file));all.push({feature,file,kind,level:Number(info[0]),...m})}}}return all}
function blob(s){let v=Buffer.from(s);return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+v.length+'\0'),v])).digest('hex')}
function validate(o){let all=scan(brain(o)),errors=[];for(let feature of new Set(all.map(x=>x.feature))){let arr=all.filter(x=>x.feature===feature),ids=new Map(),reqs=new Map();
 for(let d of arr){let m=d.meta,info=kinds[d.kind];if(ids.has(m.id))errors.push(d.file+': duplicate id '+m.id);ids.set(m.id,d);if(m.kind!==info[3])errors.push(d.file+': incorrect kind');if(!new RegExp('^'+info[2]+'-\\d{3}$').test(m.id||''))errors.push(d.file+': invalid id');if(!['draft','approved','needs-revision'].includes(m.status))errors.push(d.file+': invalid status');for(let k of ['parents','requirements','depends_on','parent_hashes'])if(!Array.isArray(m[k]))errors.push(d.file+': missing list '+k)}
 for(let d of arr.filter(x=>x.kind==='specification')){let r=[...d.body.matchAll(/^\s*-\s*(REQ-\d{3}):/gm)].map(x=>x[1]);if(new Set(r).size!==r.length)errors.push(d.file+': duplicate declared requirement ID');reqs.set(d.meta.id,new Set(r))}
 for(let d of arr){let m=d.meta;
 for(let key of ['parents','requirements','depends_on','parent_hashes']){
   let values=m[key]||[];
   if(new Set(values).size!==values.length)errors.push(d.file+': duplicate '+key);
 }
 let hashed=new Set();
 for(let value of m.parent_hashes||[]){
   let match=/^((?:BRF|SPEC|CMP|PLAN|TASK)-\d{3})@([0-9a-f]{40})$/.exec(value);
   if(!match){errors.push(d.file+': malformed parent hash '+value);continue}
   if(hashed.has(match[1]))errors.push(d.file+': duplicate parent hash '+match[1]);
   hashed.add(match[1]);
   if(!(m.parents||[]).includes(match[1]))errors.push(d.file+': parent hash for non-parent '+match[1]);
 }
 for(let id of m.parents||[]){let p=ids.get(id);if(!p)errors.push(d.file+': unknown parent '+id);else{if(p.level>=d.level)errors.push(d.file+': parent not earlier '+id);if(m.status==='approved'&&p.meta.status!=='approved')errors.push(d.file+': unapproved parent '+id);if(m.status==='approved'&&!(m.parent_hashes||[]).includes(id+'@'+blob(read(p.file))))errors.push(d.file+': stale/missing parent hash '+id)}}for(let id of m.depends_on||[]){let p=ids.get(id);if(!p||p.level!==d.level||id===m.id)errors.push(d.file+': invalid dependency '+id);else if(m.status==='approved'&&p.meta.status!=='approved')errors.push(d.file+': unapproved dependency '+id)}for(let r of m.requirements||[]){let x=r.match(/^(SPEC-\d{3})#(REQ-\d{3})$/);if(!x||!reqs.get(x[1])?.has(x[2]))errors.push(d.file+': unknown requirement '+r)}}
 let active=new Set(),done=new Set();function visit(id){if(active.has(id)){errors.push('dependency cycle: '+id);return}if(done.has(id))return;active.add(id);for(let dep of ids.get(id)?.meta.depends_on||[])if(ids.has(dep))visit(dep);active.delete(id);done.add(id)}for(let id of ids.keys())visit(id);
 if(o['check-coverage'])for(let spec of arr.filter(x=>x.kind==='specification'&&x.meta.status==='approved'))for(let level of [3,4,5]){let participants=arr.filter(x=>x.level===level&&((x.meta.parents||[]).includes(spec.meta.id)||(x.meta.requirements||[]).some(r=>r.startsWith(spec.meta.id+'#'))));if(!participants.length||participants.some(x=>x.meta.status!=='approved'))continue;let covered=new Set(participants.flatMap(x=>x.meta.requirements||[]));for(let req of reqs.get(spec.meta.id)||[])if(!covered.has(spec.meta.id+'#'+req))errors.push('no approved document covers '+spec.meta.id+'#'+req)}
 }
 if(o['show-parent-hashes']){let target=full(o['show-parent-hashes']),d=all.find(x=>x.file===target);if(!d)fail('document not found: '+target);let hashes=(d.meta.parents||[]).map(id=>{let p=all.find(x=>x.feature===d.feature&&x.meta.id===id);if(!p)fail('unknown parent '+id);return id+'@'+blob(read(p.file))});console.log('parent_hashes: ['+hashes.join(', ')+']');return}
 if(o.affected){let seeds=all.filter(x=>x.meta.id===o.affected);if(seeds.length!==1)fail('ID not unique or unknown: '+o.affected);let seed=seeds[0],seen=new Set([seed.meta.id]);let changed=true;while(changed){changed=false;for(let d of all.filter(x=>x.feature===seed.feature))if(!seen.has(d.meta.id)&&[...(d.meta.parents||[]),...(d.meta.depends_on||[])].some(id=>seen.has(id))){seen.add(d.meta.id);changed=true}}for(let d of all.filter(x=>x.feature===seed.feature&&x!==seed&&seen.has(x.meta.id)).sort((a,b)=>a.meta.id.localeCompare(b.meta.id)))console.log('AFFECTED '+d.meta.id+' '+d.file);return}
 for(let e of errors)console.log('INVALID '+e);if(errors.length)fail(errors.length+' feature-document error(s)');console.log('VALID feature documents')}
function gitState(o){let repo=full(o.repo||'.');if(o.pending){let b=brain(o),branch=o.branch||git(repo,'branch','--show-current');if(!/^[a-zA-Z0-9._/-]+$/.test(branch)||branch.includes('..'))fail('invalid branch');let target=path.join(b,'pending',branch.replaceAll('/','--')+'.md');if(exists(target)){if(!read(target).split('\n').includes('Branch: '+branch))fail('pending filename collision: '+target);console.log('UNCHANGED '+target);return}let day=o.at||new Date().toISOString().slice(0,10);changes([[target,read(path.join(root,'scaffolds/pending.md')).replaceAll('{{BRANCH}}',branch).replaceAll('{{DATE}}',day)]],o);return}console.log('BRANCH '+git(repo,'branch','--show-current'));console.log('HEAD '+git(repo,'rev-parse','HEAD'));for(let [label,args] of [['STATUS',['status','--porcelain','--untracked-files=all']],['STAGED',['diff','--cached','--name-status']],['UNSTAGED',['diff','--name-status']]])for(let l of git(repo,...args).split('\n').filter(Boolean))console.log(label+' '+l);if(o.since){git(repo,'cat-file','-e',o.since+'^{commit}');for(let l of git(repo,'diff','--name-status',o.since,'HEAD').split('\n').filter(Boolean))console.log('COMMITTED '+l)}}
function record(o){let target=path.join(brain(o),'features',slug(req(o,'feature')),'execution.md');if(!exists(target))fail('execution.md does not exist; initialize through brain-implement first: '+target);let event=req(o,'event'),detail=req(o,'detail');if(!isSlug(event)||detail.includes('\n'))fail('invalid event or detail');let text=read(target),entry='- '+event+': '+detail+'\n';if(!text.includes('## Checkpoints'))fail('execution record has no ## Checkpoints heading');if(text.slice(text.indexOf('## Checkpoints')).includes(entry)){console.log('UNCHANGED '+target);return}if(!o.apply){console.log('APPEND '+target+' (dry-run)');return}scope(target,o);fs.appendFileSync(target,(text.endsWith('\n')?'':'\n')+entry);console.log('APPENDED '+target)}
function context(o){
 let b=brain(o);if(!exists(path.join(b,'00_index.md')))fail('not a Brain: '+b);
 if(o.select){let name=o.select;if(path.isAbsolute(name)||name.split(/[\\/]/).includes('..'))fail('invalid context selection');let p=path.join(b,name);
 if(!exists(p)||!fs.statSync(p).isFile())fail('context document missing: '+name);
 let actual=fs.realpathSync(p),base=fs.realpathSync(b);if(!actual.startsWith(base+path.sep))fail('context selection escapes Brain');
 process.stdout.write(read(p));return}
 let files=fs.readdirSync(b).filter(x=>x.endsWith('.md')&&!['README.md','USAGE.md'].includes(x)).map(x=>path.join(b,x));
 if(o.branch){let p=path.join(b,'pending',slug(o.branch.replaceAll('/','--'))+'.md');if(exists(p))files.push(p)}
 if(o.feature){let name=slug(o.feature);files.push(...scan(b).filter(x=>x.feature===name).map(x=>x.file));let p=path.join(b,'features',name,'execution.md');if(exists(p))files.push(p)}
 let total=0;
 for(let f of [...new Set(files)].sort()){let s=read(f),bytes=Buffer.byteLength(s),status=s.match(/^status:\s*(\S+)/m);total+=bytes;
 let extra=o.hashes?'\t'+blob(s):'';
 console.log('DOC '+path.relative(b,f)+'\t'+bytes+'\t'+(status?.[1]||'-')+extra)}
 if(o.estimate)console.log('ESTIMATE bytes='+total+' tokens~='+Math.ceil(total/4)+' (approximate)')
}
function main(){let args=process.argv.slice(2);if(!args.length||['-h','--help'].includes(args[0])){console.log('brain-tool <init|doc|validate|git|record|context> [options]; writes require --apply --authorized-root PATH');return}let family=args.shift();if(['new','list','summary'].includes(args[0]))args.shift();let o=opts(args);let commands={init,doc,validate,git:gitState,record,context};if(!commands[family])fail('unknown command: '+family);commands[family](o)}
try{main()}catch(e){console.error('ERROR '+e.message);process.exitCode=1}
