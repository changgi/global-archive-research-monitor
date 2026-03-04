# 스케줄 설정

## 매일 오전 8시 - 아카이브 브리핑
```bash
python3 scripts/main_search.py --all --days 1
```

## 매주 월요일 오전 9시 - 주간 리포트
```bash
python3 scripts/main_search.py --all --days 7 --json
```

## 매월 1일 오전 10시 - 월간 분석
```bash
python3 scripts/main_search.py --all --days 30 --json
```
