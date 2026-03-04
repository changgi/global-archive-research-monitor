"""naa_search.py - NAA RecordSearch scraping"""
import re
from archive_base import ArchiveSearcher, ArchiveRecord
try:
    from bs4 import BeautifulSoup
    HAS=True
except ImportError:
    HAS=False

class NAASearcher(ArchiveSearcher):
    SU="https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/SearchScreens/BasicSearch.aspx"
    def search(self,keywords=None,days_back=30,extra_params=None):
        if not HAS: return []
        keywords=keywords or self.keywords; res=[]
        for kw in keywords:
            p={"kw":kw,"kp":"all"}
            resp=self._request_with_retry("GET",self.SU,params=p)
            if not resp: continue
            try:
                soup=BeautifulSoup(resp.text,"html.parser")
                for it in soup.select("div.item-result,tr.item-row")[:25]:
                    a=it.select_one("a")
                    bm=re.search(r"barcode=(\d+)",str(it))
                    bc=bm.group(1) if bm else ""
                    tt=a.get_text(strip=True) if a else ""
                    if tt:
                        u="https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/DetailsReports/ItemDetail.aspx?Barcode="+bc if bc else ""
                        res.append(ArchiveRecord(archive="NAA",record_id=bc,title=tt,url=u,held_by="National Archives of Australia"))
            except Exception as e: self.logger.error(str(e))
        return res
