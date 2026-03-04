"""report_generator.py - 한국어 브리핑 보고서 생성"""
import os, json
from datetime import datetime

class ReportGenerator:
    FLAGS = {"NARA":"\U0001f1fa\U0001f1f8","TNA":"\U0001f1ec\U0001f1e7","NAA":"\U0001f1e6\U0001f1fa",
             "JACAR":"\U0001f1ef\U0001f1f5","DPLA":"\U0001f1fa\U0001f1f8","Europeana":"\U0001f1ea\U0001f1fa"}
    NAMES = {"NARA":"미국 국립기록관리청","TNA":"영국 국립공문서관","NAA":"호주 국립기록관",
             "JACAR":"일본 아시아역사자료센터","DPLA":"미국 디지털공공도서관","Europeana":"유럽 디지털 문화유산"}

    def __init__(self, config=None):
        self.config = config or {}

    def generate(self, rba, sp=None):
        now = datetime.now()
        total = sum(len(v) for v in rba.values())
        digi = sum(1 for rr in rba.values() for r in rr if r.is_digitized)
        active = [k for k, v in rba.items() if v]

        L = []
        L.append("=" * 60)
        L.append("")
        L.append("  \U0001f5c2\ufe0f 해외 아카이브 한국 관련 자료 브리핑")
        L.append("  " + now.strftime("%Y.%m.%d %H:%M"))
        L.append("")
        L.append("=" * 60)
        L.append("")

        # 종합 요약
        L.append("\U0001f4ca 종합 요약")
        L.append("  - 검색 아카이브: " + str(len(rba)) + "개")
        L.append("  - 신규 발견 자료: " + str(total) + "건")
        L.append("  - 디지털화 자료: " + str(digi) + "건")
        if active:
            L.append("  - 결과 있는 아카이브: " + ", ".join(active))
        L.append("")

        if total == 0:
            L.append("\u2705 검색 완료. 금일 신규 자료가 없습니다.")
            L.append("")
            return "\n".join(L)

        # 아카이브별 결과
        for arch, recs in rba.items():
            flag = self.FLAGS.get(arch, "\U0001f3db\ufe0f")
            name = self.NAMES.get(arch, arch)
            L.append("-" * 60)
            L.append("")
            L.append(flag + " " + arch + " - " + name + " (" + str(len(recs)) + "건)")
            L.append("")

            if not recs:
                L.append("  신규 자료 없음")
                L.append("")
                continue

            for i, r in enumerate(recs[:15], 1):
                tag = "\U0001f4c4" if r.is_digitized else "\U0001f4cb"
                line = "  " + str(i) + ". " + tag + " " + r.title[:80]
                L.append(line)
                if r.series:
                    L.append("     시리즈: " + r.series)
                if r.date_range:
                    L.append("     날짜: " + r.date_range)
                if r.held_by:
                    L.append("     소장: " + r.held_by)
                if r.url:
                    L.append("     \U0001f517 " + r.url)
                L.append("")

            if len(recs) > 15:
                L.append("  ... 외 " + str(len(recs) - 15) + "건")
                L.append("")

        # TOP 하이라이트
        all_r = [r for rr in rba.values() for r in rr]
        dig_recs = [r for r in all_r if r.is_digitized]
        top = (dig_recs or all_r)[:5]

        if top:
            L.append("-" * 60)
            L.append("")
            L.append("\U0001f50d 주목할 자료 TOP " + str(len(top)))
            L.append("")
            for i, r in enumerate(top, 1):
                flag = self.FLAGS.get(r.archive, "")
                L.append("  " + str(i) + ". " + flag + " [" + r.archive + "] " + r.title[:70])
                if r.url:
                    L.append("     " + r.url)
                L.append("")

        # 검색 조건
        L.append("-" * 60)
        L.append("")
        L.append("\U0001f4cb 검색 조건")
        L.append("  - 검색일시: " + now.strftime("%Y-%m-%d %H:%M:%S"))
        if sp:
            if sp.get("days_back"):
                L.append("  - 검색 기간: 최근 " + str(sp["days_back"]) + "일")
            if sp.get("keywords"):
                kws = ", ".join(sp["keywords"])
                L.append("  - 추가 키워드: " + kws)
        L.append("  - 생성: Global Archive Research Monitor v2.0")
        L.append("")

        return "\n".join(L)

    def save_report(self, text, output_dir="./output"):
        os.makedirs(output_dir, exist_ok=True)
        fn = "archive_briefing_" + datetime.now().strftime("%Y%m%d_%H%M") + ".md"
        fp = os.path.join(output_dir, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(text)
        return fp

    def save_json(self, rba, output_dir="./output"):
        os.makedirs(output_dir, exist_ok=True)
        fn = "archive_data_" + datetime.now().strftime("%Y%m%d_%H%M") + ".json"
        fp = os.path.join(output_dir, fn)
        data = {a: [r.to_dict() for r in rs] for a, rs in rba.items()}
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return fp
