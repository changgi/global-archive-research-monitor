"""dpla_search.py - DPLA API v2"""
from archive_base import ArchiveSearcher, ArchiveRecord

class DPLASearcher(ArchiveSearcher):
    def search(self, keywords=None, days_back=30, extra_params=None):
        if not self.api_key:
            self.logger.warning("DPLA_API_KEY not set")
            return []
        keywords = keywords or self.keywords
        res = []
        for kw in keywords:
            p = {"q": kw, "page_size": 25, "api_key": self.api_key,
                 "sort_by": "sourceResource.date.begin",
                 "sort_order": "desc"}
            resp = self._request_with_retry(
                "GET", self.base_url + "/items", params=p)
            if not resp:
                continue
            try:
                docs = resp.json().get("docs", [])
            except Exception:
                continue
            for d in docs:
                s = d.get("sourceResource", {})
                rt = s.get("title", [""])
                title = rt[0] if isinstance(rt, list) else str(rt)
                rd = s.get("description", [""])
                desc = rd[0] if isinstance(rd, list) else str(rd)
                dp = d.get("dataProvider", "")
                dpn = dp[0] if isinstance(dp, list) and dp else str(dp)
                dates = s.get("date", [{}])
                dd = dates[0] if isinstance(dates, list) and dates else {}
                ds = dd.get("displayDate", "") if isinstance(dd, dict) else ""
                rc = s.get("creator", [])
                cr = ", ".join(rc) if isinstance(rc, list) else str(rc)
                res.append(ArchiveRecord(
                    archive="DPLA",
                    record_id=d.get("id", ""),
                    title=title,
                    date_range=ds,
                    description=desc[:300],
                    is_digitized=bool(d.get("object", "")),
                    url=d.get("isShownAt", ""),
                    thumbnail_url=d.get("object", ""),
                    creator=cr,
                    held_by=dpn,
                    metadata={"provider": d.get("provider", {}).get("name", "")}))
        return res
