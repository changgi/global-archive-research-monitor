"""nara_search.py - NARA Catalog API v2"""
from archive_base import ArchiveSearcher, ArchiveRecord

class NARASearcher(ArchiveSearcher):
    def search(self, keywords=None, days_back=30, extra_params=None):
        keywords = keywords or self.keywords
        results = []
        for kw in keywords:
            p = {"q": kw, "resultTypes": "item,fileUnit",
                 "rows": 25, "sort": "naIdSort desc"}
            if extra_params and extra_params.get("rg"):
                p["q"] = kw + ' recordGroupNumber:"' + extra_params["rg"] + '"'
            h = {"Content-Type": "application/json"}
            if self.api_key:
                h["x-api-key"] = self.api_key
            resp = self._request_with_retry(
                "GET", self.base_url + "/records/search",
                params=p, headers=h)
            if not resp:
                continue
            try:
                hits = resp.json().get("body", {}).get("hits", {}).get("hits", [])
            except Exception:
                continue
            for x in hits:
                s = x.get("_source", {})
                ph = s.get("physicalOccurrences", [{}])
                fac = ph[0].get("facilityName", "") if ph else ""
                results.append(ArchiveRecord(
                    archive="NARA",
                    record_id=str(s.get("naId", "")),
                    title=s.get("title", ""),
                    date_range=s.get("inclusiveDates", ""),
                    series=s.get("parentSeriesTitle", ""),
                    description=s.get("scopeAndContentNote", "")[:300],
                    is_digitized=s.get("hasDigitalObjects", False),
                    url="https://catalog.archives.gov/id/" + str(s.get("naId", "")),
                    creator=s.get("creatingOrganizationName", ""),
                    held_by="National Archives at " + fac if fac else "NARA",
                    access_status=s.get("accessRestrictionStatus", ""),
                    metadata={"rg": s.get("recordGroupNumber", ""),
                              "level": s.get("level", "")}))
        return results

    def search_by_record_group(self, rg, days_back=30):
        return self.search(["Korea"], days_back, {"rg": rg})
