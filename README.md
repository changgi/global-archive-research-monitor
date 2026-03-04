# 🗂️ Global Archive Research Monitor v2.0

## 해외 아카이브 한국 관련 기록물 자동 발굴 시스템

6개 해외 아카이브의 한국 관련 기록물을 자동으로 검색하고,
신규 디지털화 자료를 감지하여 한국어 브리핑 보고서를 생성합니다.

---

## 🌏 지원 아카이브

| 아카이브 | 국가 | 접근 방식 | 주요 한국 관련 기록 |
|---------|------|----------|-------------------|
| **NARA** | 🇺🇸 미국 | Catalog API v2 | 한국전쟁, 외교문서, RG 59/84/338 등 |
| **TNA** | 🇬🇧 영국 | Discovery API | FO/CO/WO 시리즈, 한국전쟁 참전 |
| **NAA** | 🇦🇺 호주 | RecordSearch 스크래핑 | 한국전쟁 참전기록, 이민기록 |
| **JACAR** | 🇯🇵 일본 | 아시아역사자료센터 스크래핑 | 조선총독부, 외무성, 방위성 기록 |
| **DPLA** | 🇺🇸 미국 | DPLA API v2 | 미국 소재 한국 관련 디지털 컬렉션 |
| **Europeana** | 🇪🇺 유럽 | REST API | 유럽 소재 한국 관련 문화유산 |

## ⚡ 빠른 시작

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. API 키 설정
cp .env.example .env
nano .env  # NARA, DPLA, Europeana 키 입력

# 3. 전체 아카이브 검색 (최근 30일)
python3 scripts/main_search.py --all --days 30
```

## 🔧 주요 실행 명령어

```bash
# 특정 아카이브만 검색
python3 scripts/main_search.py --archive nara tna --days 60

# NARA 특정 Record Group (예: RG 59 국무부)
python3 scripts/main_search.py --archive nara --rg 59 --days 30

# TNA 특정 시리즈 (예: FO 371 외무부)
python3 scripts/main_search.py --archive tna --series "FO 371"

# 추가 키워드로 검색
python3 scripts/main_search.py --all --keyword "comfort women" --days 90

# JSON 데이터도 함께 저장
python3 scripts/main_search.py --all --days 30 --json
```

## 📂 프로젝트 구조

```
archive-skill/
├── SKILL.md              # OpenClaw 스킬 정의
├── SOUL.md               # AI 에이전트 페르소나
├── HEARTBEAT.md          # 자동 실행 스케줄 (매일/주간/월간)
├── .env.example          # API 키 템플릿
├── requirements.txt      # Python 의존성
├── config/
│   └── settings.json     # 검색 키워드, RG, 시리즈 등 전체 설정
├── scripts/
│   ├── archive_base.py   # 기본 클래스 (ArchiveRecord, ArchiveSearcher)
│   ├── nara_search.py    # 🇺🇸 NARA Catalog API v2
│   ├── tna_search.py     # 🇬🇧 TNA Discovery API
│   ├── naa_search.py     # 🇦🇺 NAA RecordSearch (스크래핑)
│   ├── jacar_search.py   # 🇯🇵 JACAR (스크래핑)
│   ├── dpla_search.py    # 🇺🇸 DPLA API v2
│   ├── europeana_search.py # 🇪🇺 Europeana REST API
│   ├── report_generator.py # 한국어 브리핑 보고서 생성
│   └── main_search.py    # 통합 오케스트레이터
└── docs/
    └── SETUP.md          # 상세 설치/설정 가이드
```

## 🔑 API 키 발급

| 아카이브 | 발급 방법 | 비용 |
|---------|----------|------|
| NARA | Catalog_API@nara.gov 이메일 | 무료 (월 10,000건) |
| DPLA | https://pro.dp.la/developers/policies#get-a-key | 무료 |
| Europeana | https://pro.europeana.eu/pages/get-api | 무료 |
| TNA / NAA / JACAR | 키 불필요 | - |

## 📊 보고서 출력 예시

```
============================================================

  🗂️ 해외 아카이브 한국 관련 자료 브리핑
  2026.03.04 08:00

============================================================

📊 종합 요약
  - 검색 아카이브: 6개
  - 신규 발견 자료: 47건
  - 디지털화 자료: 23건

------------------------------------------------------------

🇺🇸 NARA - 미국 국립기록관리청 (15건)

  1. 📄 Despatch from the Ambassador in Korea...
     시리즈: RG 59 General Records of the Department of State
     🔗 https://catalog.archives.gov/id/...

🇬🇧 TNA - 영국 국립공문서관 (8건)
...
```

## 🔄 OpenClaw 자동화

OpenClaw에 설치하면 HEARTBEAT.md에 따라 자동 실행:
- **매일 08:00** - 일일 신규 자료 브리핑 (Telegram 전송)
- **매주 월요일 09:00** - 주간 종합 리포트
- **매월 1일 10:00** - 월간 분석 리포트

## 📝 기록관리교육센터 활용 시나리오

1. **교육 자료 수집**: 신규 발굴 자료를 교육 사례로 활용
2. **RG 모니터링**: 특정 Record Group의 비밀해제/디지털화 추적
3. **연구 지원**: 해외 소장 한국 관련 기록물 DB 구축
4. **MCP 서버 연동**: 기존 MCP 시스템과 통합 운용

---

*국가기록원 기록관리교육센터*
