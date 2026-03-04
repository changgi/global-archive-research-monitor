"""europeana_search.py - Europeana REST API"""
from archive_base import ArchiveSearcher, ArchiveRecord

class EuropeanaSearcher(ArchiveSearcher):
    SU = "https://api.europeana.eu/record/v2/search.json"

    def search(self, keywords=None, days_back=30, extra_params=None):
        if not self.api_key:
            self.logger.warning("EUROPEANA_API_KEY not set")
            return []
        keywords = keywords or self.keywords
        res = []
        for kw in keywords:
            p = {"query": kw, "rows": 25, "wskey": self.api_key,
                 "sort": "timestamp_update+desc", "profile": "standard"}
            resp = self._request_with_retry("GET", self.SU, params=p)
            if not resp:
                continue
            try:
                items = resp.json().get("items", [])
            except Exception:
                continue
            for it in items:
                rt = it.get("title", [""])
                title = rt[0] if isinstance(rt, list) else str(rt)
                rd = it.get("dcDescription", [""])
                desc = rd[0] if isinstance(rd, list) else str(rd)
                yr = it.get("year", [""])
                ds = str(yr[0]) if yr else ""
                rdp = it.get("dataProvider", [""])
                dp = rdp[0] if isinstance(rdp, list) and rdp else str(rdp)
                rp = it.get("edmPreview", [""])
                th = rp[0] if isinstance(rp, list) and rp else ""
                res.append(ArchiveRecord(
                    archive="Europeana",
                    record_id=it.get("id", ""),
                    title=title,
                    date_range=ds,
                    description=desc[:300] if desc else "",
                    is_digitized=True,
                    url=it.get("guid", "https://www.europeana.eu/item" + it.get("id", "")),
                    thumbnail_url=th,
                    held_by=dp,
                    metadata={"type": it.get("type", "")}))
        return res
