"""tna_search.py - TNA Discovery API"""
from archive_base import ArchiveSearcher, ArchiveRecord

class TNASearcher(ArchiveSearcher):
    def search(self, keywords=None, days_back=30, extra_params=None):
        keywords = keywords or self.keywords
        results = []
        for kw in keywords:
            p = {"sps.searchQuery": kw,
                 "sps.resultsPageSize": 25,
                 "sps.sortByOption": "DATE_DESCENDING"}
            if extra_params and extra_params.get("series"):
                p["sps.catalogueLevels"] = "Level7"
            if extra_params and extra_params.get("digitized_only"):
                p["sps.digitalisedFilter"] = "true"
            resp = self._request_with_retry(
                "GET", self.base_url + "/search/records",
                params=p, headers={"Accept": "application/json"})
            if not resp:
                continue
            try:
                recs = resp.json().get("records", [])
            except Exception:
                continue
            for r in recs:
                results.append(ArchiveRecord(
                    archive="TNA",
                    record_id=r.get("id", ""),
                    title=r.get("title", ""),
                    date_range=r.get("coveringDates", ""),
                    series=r.get("reference", ""),
                    description=r.get("description", "")[:300],
                    is_digitized=r.get("isDigitised", False),
                    url="https://discovery.nationalarchives.gov.uk/details/r/" + r.get("id", ""),
                    creator=r.get("creatorName", ""),
                    held_by=r.get("heldBy", "The National Archives"),
                    access_status=r.get("closureStatus", "Open"),
                    metadata={"dept": r.get("department", "")}))
        return results

    def search_by_series(self, ref, days_back=30):
        return self.search(["Korea"], days_back, {"series": ref})
