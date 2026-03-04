# Global Archive Research Monitor - 설치 및 설정 가이드

## 1. 사전 요구사항

### 시스템 요구사항
- Python 3.9 이상
- pip (Python 패키지 관리자)
- 인터넷 연결 (API 접근)
- OpenClaw (자동화 실행 시)

### OpenClaw 설치 (자동화 실행 시)
```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw/main/install.sh | bash

# Windows (WSL 필수)
wsl --install
# WSL 내에서:
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw/main/install.sh | bash
```

## 2. 프로젝트 설치

### 2-1. 파일 배치
```bash
# OpenClaw 스킬 디렉토리에 복사
cp -r archive-skill/ ~/clawd/skills/archive-research/

# 또는 독립 실행 시 원하는 위치에 복사
cp -r archive-skill/ ~/archive-research/
```

### 2-2. 의존성 설치
```bash
cd ~/clawd/skills/archive-research/
pip install -r requirements.txt
```

### 2-3. 환경변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (실제 API 키 입력)
nano .env
```

## 3. API 키 발급

### NARA API 키 (필수)
1. Catalog_API@nara.gov 로 이메일 발송
2. 소속기관, 사용 목적 명시
3. 보통 1-2 영업일 내 발급
4. 월 10,000건 무료 (추가 요청 가능)

### DPLA API 키 (선택)
1. https://pro.dp.la/developers/policies#get-a-key 접속
2. 이메일 주소로 신청
3. 즉시 또는 당일 발급
4. 무료

### Europeana API 키 (선택)
1. https://pro.europeana.eu/pages/get-api 접속
2. 계정 생성 후 API 키 발급
3. 즉시 발급
4. 무료

### 키 불필요 아카이브
- TNA Discovery API: 인증 없이 사용 가능
- NAA RecordSearch: 웹 스크래핑 (키 불필요)
- JACAR: 웹 스크래핑 (키 불필요)

## 4. 설정 커스터마이즈

### config/settings.json 주요 설정

```json
{
  "general": {
    "default_days_back": 30,      // 기본 검색 기간
    "max_results_per_archive": 50, // 아카이브당 최대 결과
    "request_delay_seconds": 1     // 요청 간 대기시간
  }
}
```

### 검색 키워드 추가/수정

각 아카이브의 "keywords" 배열에 원하는 키워드를 추가:

```json
"nara": {
  "keywords": [
    "Korea",
    "Korean War",
    "YOUR_NEW_KEYWORD"
  ]
}
```

### 특정 아카이브 비활성화

```json
"europeana": {
  "enabled": false
}
```

## 5. 실행 방법

### 수동 실행
```bash
cd ~/clawd/skills/archive-research/

# 전체 6개 아카이브 검색
python3 scripts/main_search.py --all --days 30

# NARA + TNA만 검색
python3 scripts/main_search.py --archive nara tna --days 30

# NARA 특정 Record Group (국무부 RG 59)
python3 scripts/main_search.py --archive nara --rg 59 --days 60

# TNA 특정 시리즈 (FO 371 외무부)
python3 scripts/main_search.py --archive tna --series "FO 371"

# 키워드 추가하여 검색
python3 scripts/main_search.py --all --keyword "comfort women" --days 90

# JSON 결과도 함께 저장
python3 scripts/main_search.py --all --days 30 --json

# 화면 출력 없이 파일만 저장
python3 scripts/main_search.py --all --days 30 --quiet
```

### OpenClaw 자동 실행

HEARTBEAT.md에 정의된 스케줄에 따라 자동 실행:
- 매일 오전 8시: 일일 브리핑
- 매주 월요일 오전 9시: 주간 종합
- 매월 1일 오전 10시: 월간 분석

### 결과 확인

결과 파일은 `output/` 디렉토리에 저장됩니다:
- `archive_briefing_YYYYMMDD_HHMM.md` - 마크다운 보고서
- `archive_data_YYYYMMDD_HHMM.json` - JSON 원시 데이터

## 6. 프로젝트 구조

```
archive-research/
├── SKILL.md              # OpenClaw 스킬 정의
├── SOUL.md               # 에이전트 페르소나
├── HEARTBEAT.md          # 자동 실행 스케줄
├── .env.example          # 환경변수 템플릿
├── .env                  # 실제 API 키 (git 제외)
├── requirements.txt      # Python 의존성
├── config/
│   └── settings.json     # 검색 설정 (키워드, RG, 시리즈)
├── scripts/
│   ├── archive_base.py   # 기본 클래스 (ArchiveRecord, ArchiveSearcher)
│   ├── nara_search.py    # NARA Catalog API v2
│   ├── tna_search.py     # TNA Discovery API
│   ├── naa_search.py     # NAA RecordSearch (스크래핑)
│   ├── jacar_search.py   # JACAR (스크래핑)
│   ├── dpla_search.py    # DPLA API v2
│   ├── europeana_search.py # Europeana REST API
│   ├── report_generator.py # 한국어 보고서 생성
│   └── main_search.py    # 통합 오케스트레이터
├── docs/
│   └── SETUP.md          # 이 파일
├── templates/            # 보고서 템플릿 (확장용)
└── output/               # 검색 결과 저장
```

## 7. 각 아카이브 모듈 상세

### NARA (nara_search.py)
- API: REST API v2 (JSON)
- 인증: x-api-key 헤더
- 주요 RG: 59(국무부), 84(해외공관), 338(극동군), 332(미군정)
- 필터: Record Group, 날짜, 디지털화 여부

### TNA (tna_search.py)
- API: Discovery API (JSON)
- 인증: 불필요
- 주요 시리즈: FO 371, FO 660, WO 308, CAB 128
- 필터: 시리즈, 날짜순 정렬, 디지털화 필터

### NAA (naa_search.py)
- 방식: RecordSearch 웹 스크래핑
- 인증: 불필요
- 주요 시리즈: A1838(외교), B883(군인기록)
- 의존성: beautifulsoup4

### JACAR (jacar_search.py)
- 방식: 웹 스크래핑
- 인증: 불필요
- 컬렉션: A(국립공문서관), B(외무성), C(방위성)
- 키워드: 일본어(한자) 사용

### DPLA (dpla_search.py)
- API: REST API v2 (JSON)
- 인증: api_key 파라미터
- 다양한 미국 기관 소장 한국 자료 통합 검색

### Europeana (europeana_search.py)
- API: REST API (JSON)
- 인증: wskey 파라미터
- 유럽 전역 문화유산 기관 한국 관련 자료

## 8. 확장 방법

### 새 아카이브 추가

1. `scripts/` 에 새 검색 모듈 생성 (ArchiveSearcher 상속)
2. `config/settings.json` 에 설정 추가
3. `scripts/main_search.py`의 SEARCHER_CLASSES에 등록

```python
# 예시: 캐나다 LAC 추가
from lac_search import LACSearcher
CLS['lac'] = LACSearcher
```

### 알림 채널 추가

`report_generator.py`에 Slack, 이메일 등 전송 기능 추가 가능

## 9. 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| NARA 결과 없음 | API 키 미설정 | .env에 NARA_API_KEY 설정 |
| NAA/JACAR 오류 | bs4 미설치 | pip install beautifulsoup4 |
| 429 오류 | 요청 과다 | request_delay_seconds 증가 |
| 빈 결과 | 키워드 불일치 | settings.json 키워드 조정 |

## 10. 라이선스 및 주의사항

- 각 아카이브의 이용 약관을 준수하세요
- 스크래핑 대상(NAA, JACAR)은 과도한 요청을 자제하세요
- API 할당량을 모니터링하세요 (특히 NARA 월 10,000건)
- 수집된 자료의 저작권은 원 소장기관에 있습니다
