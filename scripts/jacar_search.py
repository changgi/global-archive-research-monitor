"""jacar_search.py - JACAR (Japan Center for Asian Historical Records)"""
from archive_base import ArchiveSearcher, ArchiveRecord
try:
    from bs4 import BeautifulSoup
    HAS=True
except ImportError:
    HAS=False

class JACARSearcher(ArchiveSearcher):
    SU="https://www.jacar.go.jp/DAS/meta/result"
    ORGS={"A":"국립공문서관 (国立公文書館)","B":"외무성 외교사료관 (外務省外交史料館)","C":"방위성 방위연구소 (防衛省防衛研究所)"}

    def search(self,keywords=None,days_back=30,extra_params=None):
        if not HAS: return []
        keywords=keywords or self.keywords; res=[]
        for kw in keywords:
            p={"DEF_XSL":"default","IS_KIND":"SimpleSummary","IS_SCH":kw,
               "IS_TYPE":"meta","IS_START":1,"IS_TAG_S1":"InD","IS_KEY_S1":kw}
            if extra_params and extra_params.get("collection"):
                p["IS_TAG_S2"]="R"; p["IS_KEY_S2"]=extra_params["collection"]
            resp=self._request_with_retry("GET",self.SU,params=p)
            if not resp: continue
            try:
                soup=BeautifulSoup(resp.text,"html.parser")
                for it in soup.select("div.result_item,li.searchResult")[:25]:
                    te=it.select_one("a")
                    re_=it.select_one("span.ref_code,span.reference")
                    ref=re_.get_text(strip=True) if re_ else ""
                    tt=te.get_text(strip=True) if te else ""
                    if tt:
                        u="https://www.jacar.go.jp/DAS/meta/image_"+ref if ref else ""
                        org=self.ORGS.get(ref[0].upper(),"JACAR") if ref else "JACAR"
                        res.append(ArchiveRecord(archive="JACAR",record_id=ref,
                            title=tt,series=ref[:1] if ref else "",
                            is_digitized=True,url=u,held_by=org,
                            metadata={"collection":ref[:1] if ref else ""}))
            except Exception as e: self.logger.error(str(e))
        return res
