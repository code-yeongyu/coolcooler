# EBS Lecture auto-listener

개인적인 호기심으로 제작하였으나 사용을 권장하지는 않습니다.
javscript 소스를 사용해 완강처리를 시켜버리는것이 아닌, 크롬을 백그라운드로 돌려 강의를 듣는것과 100% 똑같이 처리하는 방법입니다.

## 준비물
본 프로젝트는 selenium과 파이썬을 사용합니다.  
프로젝트를 다운로드 받은 뒤, <https://chromedriver.chromium.org/downloads> 에서 현재 사용중인 크롬과 같은 버전의 드라이버를 다운받아주세요. 이 방법으로 크롬드라이버를 설치 해주세요.

<https://chromedriver.chromium.org/downloads> 에서 다운로드 받은 파일의 압축을 해제하고, "chromedriver.exe" 혹은 "chromedriver" 라는 이름으로 된 파일을 lecture.py가 위치한곳과 같은 경로에 넣어주세요.

파이썬은 검색을 통해 설치해주시면 좋겠습니다.
파이썬을 설치 한 이후,
```bash
pip install -r requirements.txt
```
를 통해 selenium 모듈을 설치해주세요.

## 설정
lecture_list.txt에 수강처리하고싶은 강의를 넣어주세요.  
본 프로젝트는 자동으로 강의 동영상을 순차적으로 재생시키는 원리를 갖고있습니다.  
따라서, lecture_list.txt에 들어가는 링크는 동영상이 포함된 강의의 링크여야합니다.  
이후 settings.json 파일을 열어 관련 내용을 수정해주세요.  
settings.json에서 어떤 내용을 수정해야 할지는 해당 파일에 이미 설명되어있습니다.

## 사용
본 파이썬 파일을 실행해주시면 됩니다. *nix 게열의 운영체제에서는:
```bash
python3 lecture.py
```
NT 계열의 운영체제에서는:
```powershell
python lecture.py
```

## 주의
소스가 궁금하다거나, 어떻게 작동한다거나 하는 호기심을 제외하고는, 본 코드를 사용하지 않는것을 매우 강력하게 권장합니다.  
이 코드를 사용함으로써 생길 수 있는 모든 문제는 사용자의 책임입니다.