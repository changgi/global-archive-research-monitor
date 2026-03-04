"""archive_base.py"""
import os,json,time,logging,requests
from abc import ABC,abstractmethod
from datetime import datetime
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(name)s] %(message)s")

class ArchiveRecord:
    def __init__(self,archive="",record_id="",title="",date_range="",series="",description="",is_digitized=False,url="",thumbnail_url="",creator="",held_by="",access_status="",date_added="",metadata=None):
        self.archive=archive;self.record_id=record_id;self.title=title
        self.date_range=date_range;self.series=series;self.description=description
        self.is_digitized=is_digitized;self.url=url;self.thumbnail_url=thumbnail_url
        self.creator=creator;self.held_by=held_by;self.access_status=access_status
        self.date_added=date_added or datetime.now().strftime("%Y-%m-%d")
        self.metadata=metadata or {}
    def to_dict(self): return self.__dict__.copy()

class ArchiveSearcher(ABC):
    def __init__(self,config):
        self.config=config;self.name=config.get("name","?")
        self.flag=config.get("flag","");self.enabled=config.get("enabled",True)
        self.base_url=config.get("base_url","");self.keywords=config.get("keywords",[])
        self.logger=logging.getLogger(self.__class__.__name__)
        ae=config.get("api_key_env")
        self.api_key=os.getenv(ae,"") if ae else ""
        self.session=requests.Session()
        self.session.headers["User-Agent"]="ArchiveMonitor/2.0"

    def _request_with_retry(self,method,url,retry_count=3,delay=2.0,**kw):
        for i in range(retry_count):
            try:
                r=self.session.request(method,url,timeout=30,**kw)
                if r.status_code==200: return r
                if r.status_code==429: time.sleep(delay*(i+2))
            except Exception as e:
                self.logger.error(str(e))
                if i<retry_count-1: time.sleep(delay)
        return None

    @abstractmethod
    def search(self,keywords=None,days_back=30,extra_params=None): pass

    def search_all_keywords(self,days_back=30,extra_params=None,request_delay=1.0):
        recs,seen=[],set()
        for kw in self.keywords:
            self.logger.info("검색: "+kw)
            try:
                for r in self.search([kw],days_back,extra_params):
                    if r.record_id not in seen: seen.add(r.record_id);recs.append(r)
            except Exception as e: self.logger.error(str(e))
            time.sleep(request_delay)
        self.logger.info(self.name+": "+str(len(recs))+"건")
        return recs

    def get_status(self):
        return {"name":self.name,"enabled":self.enabled,"has_api_key":bool(self.api_key)}
