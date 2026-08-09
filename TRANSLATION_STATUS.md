# eraNAS 한국어화 작업 현황

- 기준 원본: `mrpopsalot/pops-tw` `dev/omogatari-kai`
- 한국어 참고본: `TakenTextbung/eranaskr`
- 공통 경로 파일 수: 8238
- 최신 원본에만 있어 추가한 파일 수: 1
- 영어 화면 출력 후보 줄 수(자동 탐지, 오탐 포함): 652815
- 영어 화면 출력 후보가 있는 파일 수: 3012

## 병합 원칙

1. 공통 파일은 기존 한국어 번역을 우선 보존합니다.
2. 최신 원본에만 존재하는 파일은 원본에서 추가합니다.
3. 변수명, 함수명, 라벨, ERB 명령어 등 실행 식별자는 번역하지 않습니다.
4. `translation_remaining_sample.tsv`는 최대 5,000줄의 표본입니다.
5. `translation_remaining_by_file.tsv`는 영어 후보가 많은 파일 상위 1,000개입니다.
