# tistory-indexer

![PyPI](https://img.shields.io/pypi/v/tistory-indexer)
![Python](https://img.shields.io/pypi/pyversions/tistory-indexer)

티스토리(Tistory) 블로그 글을 자동으로 Google Search Console (GSC)에 색인 요청하는 파이썬 라이브러리입니다.

> ✅ 블로그가 GSC에 등록되어 있어야 하며, OAuth 인증이 필요합니다.

---

## 🚀 주요 기능

- 티스토리 블로그에서 전체 글 자동 수집 (가장 최근 수정된 글부터 순서대로 처리)
- Google Indexing API를 통해 자동 색인 요청
- 이미 색인된 글은 건너뜀 (중복 방지)

---

## 📦 설치 방법

Python 3.11 이상에서 다음 명령어로 설치할 수 있습니다:

```bash
pip install tistory-indexer
```

---

## ⚙️ 사전 준비

1. Google Cloud Console에서 프로젝트 생성
2. Web Search Indexing API, Google Search Console API 활성화
3. OAuth 클라이언트 ID 생성 (애플리케이션 유형: 데스크톱 앱)
4. JSON 형식의 클라이언트 ID 파일 다운로드 (예: oauth_credentials.json)
5. OAuth 동의 화면 > 대상 > 테스트 사용자에서 자신의 이메일 주소를 추가

---

## 🧪 사용 방법

```python
from tistory_indexer import TistoryIndexer

indexer = TistoryIndexer(
    tistory_blog_url="https://your-blog.tistory.com",
    oauth_credentials_path="oauth_credentials.json"
)

indexer.run(pages=5)  # 가장 최근 수정된 글 중 최대 5개 색인 요청
```

---

## ⚙️ 옵션 설명

| **옵션**               | **설명**                            |
| ---------------------- | ----------------------------------- |
| tistory_blog_url       | 티스토리 블로그 주소                |
| oauth_credentials_path | OAuth 클라이언트 키(JSON) 파일 경로 |

---

📋 요구 사항

- Python 3.11 이상
- 설치 시 다음 의존성이 자동으로 포함됩니다:
  - google-auth
  - google-auth-oauthlib
  - requests
  - beautifulsoup4
  - lxml

---

📜 라이선스

MIT License © 2025 OuOHoon  
GitHub: [@ouohoon](https://github.com/ouohoon)

자세한 내용은 LICENSE 파일을 참고하세요.

---

☕ 후원하기

이 프로젝트가 도움이 되었다면 후원을 고려해주세요!

<a href="https://www.buymeacoffee.com/OuOHoon" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

---

🙋 자주 묻는 질문 (FAQ)

Q. OAuth 인증은 어떻게 하나요?

- 최초 실행 시 브라우저를 통해 Google 로그인 창이 나타납니다. 로그인 후 생성된 token.json 파일이 자동 저장되며, 이후에는 자동으로 인증됩니다.

Q. 색인 요청을 자주 보내도 되나요?

- Google Indexing API는 무료 사용자의 하루 요청 횟수에 제한(기본적으로 200개)이 있습니다. 무분별한 요청은 피해주세요.

Q. API로 색인 상태를 조회하면 "NEUTRAL"이 뜨는데, GSC에서는 "색인 등록됨"이라고 나와요. 왜 그런가요?

- Google Search Console API에서 반환하는 `verdict` 값은 실시간 검사 결과 또는 제한된 분석 기반으로 판단됩니다. 실제 색인 상태와 달리 "NEUTRAL"로 나올 수 있으며, 이는 색인이 안 됐다는 의미는 아닙니다.
- 색인 여부는 GSC 웹 UI의 색인 상태도 함께 참고하는 것이 좋습니다.

---

## ⚠️ 주의 및 면책 조항

이 도구는 Google Indexing API를 자동으로 사용하는 오픈소스 도구입니다.  
본 프로그램의 사용으로 인해 발생하는 색인 문제, API 사용 제한, 또는 기타 손해에 대해 작성자는 책임지지 않습니다.

사용자는 본 도구를 자신의 책임하에 사용해야 하며,  
예상치 못한 결과에 대해서는 어떠한 보장도 제공되지 않습니다.
