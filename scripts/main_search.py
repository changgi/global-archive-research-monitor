#!/usr/bin/env python3
import os,sys,json,argparse,logging
from collections import OrderedDict
SD=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,SD)
from nara_search import NARASearcher
from tna_search import TNASearcher
from naa_search import NAASearcher
from jacar_search import JACARSearcher
from dpla_search import DPLASearcher
from europeana_search import EuropeanaSearcher
from report_generator import ReportGenerator
logging.basicConfig(level=logging.INFO)
log=logging.getLogger('Main')
CLS=OrderedDict([('nara',NARASearcher),('tna',TNASearcher),('naa',NAASearcher),('jacar',JACARSearcher),('dpla',DPLASearcher),('europeana',EuropeanaSearcher)])

def load_config(p=None):
    if not p: p=os.path.join(SD,'..','config','settings.json')
    return json.load(open(os.path.abspath(p),encoding='utf-8'))

def load_env():
    ep=os.path.join(SD,'..', '.env')
    if os.path.exists(ep):
        for ln in open(ep, encoding='utf-8'):
            ln=ln.strip()
            if ln and not ln.startswith('#') and '=' in ln:
                k,_,v=ln.partition('=')
                os.environ.setdefault(k.strip(),v.strip())

def run(archives=None,days=30,extra_kw=None,rg=None,series=None,config=None):
    if not config: config=load_config()
    ac=config.get('archives',{})
    delay=config.get('general',{}).get('request_delay_seconds',1.0)
    targets=[a.lower() for a in archives] if archives else list(CLS.keys())
    results=OrderedDict()
    for key in targets:
        if key not in CLS: continue
        cfg=ac.get(key,{})
        if not cfg.get('enabled',True): results[key.upper()]=[]; continue
        if extra_kw:
            m=list(cfg.get('keywords',[]))
            m.extend(extra_kw)
            cfg['keywords']=m
        S=CLS[key](cfg)
        st=S.get_status()
        ae=cfg.get('api_key_env')
        if ae and not st['has_api_key']:
            log.warning(key+': no API key')
            results[key.upper()]=[]; continue
        log.info('Searching: '+cfg.get('name',key))
        ep={}
        if rg and key=='nara': ep['rg']=rg
        if series and key=='tna': ep['series']=series
        try:
            recs=S.search_all_keywords(days_back=days,extra_params=ep or None,request_delay=delay)
            dn=key.upper()
            if key=='jacar': dn='JACAR'
            elif key=='europeana': dn='Europeana'
            results[dn]=recs
        except Exception as e:
            log.error(key+' fail: '+str(e))
            results[key.upper()]=[]
    return results

def main():
    pa=argparse.ArgumentParser(description='Archive Search')
    pa.add_argument('--all',action='store_true')
    pa.add_argument('--archive',nargs='+',choices=list(CLS.keys()))
    pa.add_argument('--days',type=int,default=30)
    pa.add_argument('--keyword',nargs='+')
    pa.add_argument('--rg',type=str)
    pa.add_argument('--series',type=str)
    pa.add_argument('--config',type=str)
    pa.add_argument('--output',type=str,default='./output')
    pa.add_argument('--json',action='store_true')
    pa.add_argument('--quiet',action='store_true')
    a=pa.parse_args()
    load_env()
    cfg=load_config(a.config)
    if not a.all and not a.archive: pa.print_help(); sys.exit(1)
    arcs=a.archive if a.archive else None
    log.info('Archive Search - last '+str(a.days)+' days')
    results=run(archives=arcs,days=a.days,extra_kw=a.keyword,rg=a.rg,series=a.series,config=cfg)
    rpt=ReportGenerator(cfg.get('report',{}))
    report=rpt.generate(results,{'days_back':a.days,'keywords':a.keyword})
    if not a.quiet: print(report)
    path=rpt.save_report(report,a.output)
    log.info('Saved: '+path)
    if a.json:
        jp=rpt.save_json(results,a.output)
        log.info('JSON: '+jp)
    total=sum(len(v) for v in results.values())
    log.info('Done! '+str(total)+' records')
    return results

if __name__=='__main__': main()
