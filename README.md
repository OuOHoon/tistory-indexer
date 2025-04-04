# tistory-indexer

티스토리(Tistory) 블로그 글을 자동으로 Google Search Console (GSC)에 색인 요청하는 파이썬 라이브러리입니다.


> ✅ 블로그가 GSC에 등록되어 있어야 하며, 서비스 계정이 소유자로 추가되어야 합니다.

---

## 🚀 주요 기능

- 티스토리 블로그에서 전체 글 자동 수집 (가장 최근 글부터 순서대로 처리)
- Google Indexing API를 통해 자동 색인 요청
- 이미 색인된 글은 건너뜀 (중복 방지)
- 크론(cron) 또는 GitHub Actions로 자동 실행 가능

---

## 📦 설치 방법

```bash
pip install tistory-indexer
```

---

## ⚙️ 사전 준비

1.	Google Cloud Console에서 프로젝트 생성
2.	Web Search Indexing API, Google Search Console API 활성화
3.	서비스 계정 생성 및 JSON 키 다운로드 (예: gsc-key.json)
4.	해당 서비스 계정 이메일을 GSC 소유자 권한으로 추가

---

## 🧪 사용 방법
```python
from tistory_indexer import TistoryIndexer

indexer = TistoryIndexer(
    tistory_blog_url="https://your-blog.tistory.com",
    credentials_path="gsc-key.json"
)

indexer.run()  # 전체 글 수집 후 색인 요청
```

---

## ⚙️ 옵션 설명

|**옵션**|**설명**|
|:---|:---|
|tistory_blog_url|티스토리 블로그 주소|
|credentials_path|서비스 계정 키(JSON) 경로|

---

## 🔄 자동 실행 예시
🖥 로컬에서 크론(cron) 설정
```cron
0 0 * * * /usr/bin/python3 /path/to/run_indexer.py
```
☁️ GitHub Actions 예시
```yaml
on:
  schedule:
    - cron: '0 0 * * *'

jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install tistory-indexer
      - run: python run_indexer.py
```

---

📋 요구 사항
-	Python 3.8 이상
-	google-auth, requests, beautifulsoup4
→ 설치 시 자동으로 포함됨

---

📜 라이선스

MIT License © 2025 OuOHoon

자세한 내용은 LICENSE 파일을 참고하세요.

---

☕ 후원하기

이 프로젝트가 도움이 되었다면 후원을 고려해주세요!

<a href="https://www.buymeacoffee.com/OuOHoon" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

---

🙋 자주 묻는 질문 (FAQ)

Q. 색인 요청을 자주 보내도 되나요?
-	Google Indexing API는 무료 사용자의 하루 요청 횟수에 제한(기본적으로 200개)이 있습니다. 무분별한 요청은 피해주세요.

Q. 서비스 계정을 Search Console에 어떻게 추가하나요?
-	GSC에서 사이트를 클릭 → 설정 → 사용자 및 권한 → 서비스 계정 이메일 추가 + 소유자 권한 부여
