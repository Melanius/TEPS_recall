# TEPS Recall (TEPS Remember)

TEPS 시험 준비를 위한 올인원 암기 퀴즈 앱입니다. Streamlit을 사용하여 웹 및 모바일 환경에 최적화된 학습 경험을 제공합니다.

## 🚀 기능 (Features)

### 1. 📘 어휘 (Vocabulary)
- **4지선다 퀴즈**: 단어를 보고 올바른 뜻을 맞추는 모드.
- **자동 오답 생성**: 같은 파일 내의 다른 단어 뜻을 오답 보기로 사용하여 매번 새로운 느낌을 줍니다.

### 2. 📗 문법 (Grammar)
- **유형별 학습**: 현재 'To 부정사 vs 동명사(-ing)' 취급 동사 구분 연습이 포함되어 있습니다.
- **힌트 기능**: 헷갈릴 때 한글 뜻을 힌트로 볼 수 있습니다.

### 3. 🎧 청해 (Listening)
- **Flashcard Mode**: 문장을 보고 스스로 해석한 뒤 정답을 확인하는 방식.
- **Self-Check**: '알았음/몰랐음'을 직접 체크하여 아는 문장은 넘어가고 모르는 문장만 복습할 수 있습니다.

### 4. 📖 독해 (Reading)
- **독해 필수 어휘**: 독해 지문에 자주 나오는 고난도 어휘를 4지선다로 테스트합니다.

---

## 🛠 설치 및 실행 (Installation & Run)

### 1. 환경 설정
Python이 설치되어 있어야 합니다. 필요한 라이브러리를 설치하세요.
```bash
pip install -r requirements.txt
```

### 2. 앱 실행
```bash
python -m streamlit run src/app.py
```

## 📂 폴더 구조
- `src/`: 앱 소스 코드 (`app.py`, `quiz_manager.py` 등)
- `data/`: 퀴즈 데이터 (`csv` 파일만 추가하면 자동으로 문제 생성)
