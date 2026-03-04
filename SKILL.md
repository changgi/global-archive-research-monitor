---
name: Global Archive Research Monitor
description: >
  NARA, TNA, NAA, JACAR, DPLA, Europeana
  6개 해외 아카이브 한국 관련 신규 디지털화 자료 검색 스킬
version: 2.0.0
requirements:
  - python3
  - requests
  - beautifulsoup4
---

# Global Archive Research Monitor

## 트리거: "아카이브 검색", "NARA 검색", "신규 자료 확인"

## Instructions

```bash
python3 scripts/main_search.py --all --days 30
python3 scripts/main_search.py --archive nara tna --days 60
python3 scripts/main_search.py --archive nara --rg 59
```
