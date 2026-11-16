#!/usr/bin/env node
// Conservative Brain context planner: Node built-ins, no packages.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';

const VERSION='# brain-context-map v1';
const EXCLUDED=new Set(['README.md','USAGE.md']);
const MANDATORY=new Set(['00_index.md','03_architecture.md','09_user_decisions.md','open_questions.md','state.md']);
const slug=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const supported=/^[A-Za-z0-9_./ -]+$/;
function fail(message){throw Error(message)}
function safe(value,{directory=false}={}){
 const s=value.replaceAll('\\','/');
 if(!s||s.startsWith('/')||s.includes('\t')||s.includes('\n')||!supported.test(s))fail('invalid relative path');
 const parts=s.replace(/\/$/,'').split('/');
 if(parts.some(p=>!p||p==='.'||p==='..'))fail('invalid relative path');
 return s.replace(/\/$/,'')+(directory&&s.endsWith('/')?'/':'')
}
function blob(value){
 return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+value.length+'\0'),value])).digest('hex')
}
function walk(folder,base,docs){
 for(const ent of fs.readdirSync(folder,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name,'en'))){
  const p=path.join(folder,ent.name),rel=path.relative(base,p).split(path.sep).join('/');
  if(ent.isSymbolicLink())fail('unsafe Brain document: '+rel);
  if(ent.isDirectory()){walk(p,base,docs);continue}
  if(ent.isFile()&&rel.endsWith('.md')&&!EXCLUDED.has(rel))docs.set(rel,fs.readFileSync(p));
 }
}
function inventory(brain){
 if(!fs.existsSync(path.join(brain,'00_index.md')))fail('brain index missing');
 const docs=new Map();walk(brain,brain,docs);return docs
}
const governed=rel=>!rel.startsWith('features/')&&!rel.startsWith('pending/');
function scopeMatch(selectors,features,paths){
 return selectors.split(';').some(item=>{
  if(item.startsWith('feature:'))return features.includes(item.slice(8));
  if(item.startsWith('path:')){const p=item.slice(5);return paths.some(candidate=>candidate===p.replace(/\/$/,'')||(p.endsWith('/')&&candidate.startsWith(p)))}
  return false
 })
}
function parseMap(brain,docs){
 const file=path.join(brain,'context-map.tsv');if(!fs.existsSync(file))return [new Map(),'missing-map'];
 const lines=fs.readFileSync(file,'utf8').split(/\r?\n/);
 if(lines[0]!==VERSION)return [new Map(),'invalid-map-header'];
 const mapping=new Map();
 for(const line of lines.slice(1)){
  if(!line||line.startsWith('#'))continue;
  const parts=line.split('\t');if(parts.length!==4)return [new Map(),'invalid-map-row'];
  const [rel,mode,selectors,hash]=parts;
  try{if(safe(rel)!==rel)return [new Map(),'invalid-map-path']}catch{return [new Map(),'invalid-map-path']}
  if(mapping.has(rel))return [new Map(),'duplicate-map-path'];
  if(mode==='global'){if(selectors!=='-')return [new Map(),'invalid-global-selector']}
  else if(mode==='scoped'){
   if(!selectors||selectors==='-')return [new Map(),'invalid-scope'];
   for(const item of selectors.split(';')){
    if(item.startsWith('feature:')&&slug.test(item.slice(8)))continue;
    if(item.startsWith('path:')){
     try{if(safe(item.slice(5),{directory:true})===item.slice(5))continue}catch{}
    }
    return [new Map(),'invalid-scope']
   }
  }else return [new Map(),'invalid-map-mode'];
  if(!/^[a-f0-9]{40}$/.test(hash))return [new Map(),'invalid-map-hash'];
  if(!docs.has(rel)||blob(docs.get(rel))!==hash)return [new Map(),'stale-map'];
  mapping.set(rel,[mode,selectors]);
 }
 const expected=[...docs.keys()].filter(governed);
 if(mapping.size!==expected.length||expected.some(k=>!mapping.has(k)))return [new Map(),'incomplete-map'];
 return [mapping,'']
}
function plan(brain,docs,features,paths,branch){
 const [mapping,error]=parseMap(brain,docs);let reason=error;
 if(!features.length&&!paths.length)reason ||= 'unknown-scope';
 if(!branch)reason ||= 'unknown-branch';
 if(reason)return ['full',reason,[...docs.keys()].sort()];
 const selected=new Set([...docs.keys()].filter(n=>MANDATORY.has(n)));
 if(branch){let pending='pending/'+branch.replaceAll('/','--')+'.md';if(docs.has(pending))selected.add(pending)}
 for(let feature of features)for(let name of docs.keys())if(name.startsWith('features/'+feature+'/'))selected.add(name);
 for(let [name,[mode,selectors]] of mapping){
  if(mode==='global'||scopeMatch(selectors,features,paths))selected.add(name)
 }
 for(let candidate of paths){
  if(![...mapping.values()].some(([mode,selectors])=>mode==='scoped'&&scopeMatch(selectors,[],[candidate])))
   return ['full','unmapped-code-path',[...docs.keys()].sort()];
 }
 for(let feature of features){
  if(![...docs.keys()].some(n=>n.startsWith('features/'+feature+'/'))&&
     ![...mapping.values()].some(([mode,selectors])=>mode==='scoped'&&scopeMatch(selectors,[feature],[])))
   return ['full','unmapped-feature',[...docs.keys()].sort()];
 }
 const probes=[...paths,...features.map(x=>'features/'+x+'/')];
 for(let [name,content] of docs){
  if(name.startsWith('pending/')&&!selected.has(name))continue;
  let text=content.toString('utf8');
  if(probes.some(p=>text.includes(p)))selected.add(name);
 }
 // Link closure is bidirectional; no semantic guesses about omitted files.
 let changed=true;
 while(changed){
  changed=false;
  for(let [name,content] of docs){
   if(name.startsWith('pending/')&&!selected.has(name))continue;
   let text=content.toString('utf8');
   for(let [other,otherContent] of docs){
    if(other===name||(other.startsWith('pending/')&&!selected.has(other)))continue;
    if(name!=='00_index.md'&&name!=='state.md'&&other!=='00_index.md'&&other!=='state.md' &&
       text.includes(other)&&(selected.has(name)||selected.has(other))){
     if(!selected.has(name)||!selected.has(other)){
      selected.add(name);selected.add(other);changed=true
     }
    }
   }
  }
 }
 return ['selective','mapped-and-linked',[...selected].sort()]
}
function parseArgs(argv){
 if(!argv.length||!['plan','map'].includes(argv[0]))fail('action must be plan or map');
 let options={action:argv[0],features:[],paths:[]};
 for(let i=1;i<argv.length;i++){
  let k=argv[i];if(!['--brain','--branch','--feature','--path'].includes(k))fail('unknown argument: '+k);
  if(i+1>=argv.length||argv[i+1].startsWith('--'))fail('missing argument for '+k);
  let v=argv[++i];if(k==='--feature')options.features.push(v);else if(k==='--path')options.paths.push(v);else options[k.slice(2)]=v;
 }
 if(!options.brain)fail('--brain required');
 for(let feature of options.features)if(!slug.test(feature))fail('invalid feature slug');
 options.paths=options.paths.map(p=>safe(p,{directory:true}));
 if(options.branch&&(!/^[A-Za-z0-9._/-]+$/.test(options.branch)||options.branch.startsWith('/')||options.branch.includes('..')))fail('invalid branch');
 return options
}
function main(){
 const args=parseArgs(process.argv.slice(2)),brain=fs.realpathSync(args.brain);
 const docs=inventory(brain);
 if(args.action==='map'){
  console.log(VERSION);console.log('# Review scope declarations before using selective loading.');
  for(let [name,content] of [...docs].sort(([a],[b])=>a<b?-1:a>b?1:0))if(governed(name))console.log(name+'\tglobal\t-\t'+blob(content));
  return
 }
 const [mode,reason,files]=plan(brain,docs,args.features,args.paths,args.branch);
 console.log('MODE\t'+mode);console.log('REASON\t'+reason);
 for(let file of files)console.log('READ\t'+file);
 const total=[...docs.values()].reduce((n,b)=>n+b.length,0),amount=files.reduce((n,f)=>n+docs.get(f).length,0);
 console.log('BYTES\t'+amount+'\t'+total);
}
try{main()}catch(e){console.error('ERROR '+e.message);process.exitCode=1}
