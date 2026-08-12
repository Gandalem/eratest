# korean-next 마이그레이션 원칙

`korean-next`는 `main@418eec9`에서 분기한 최신 한국어판 계보이다. 기존
`korean` 및 PR #1은 병합 대상이 아니라 번역 문장 참고 원본으로 사용한다.

## 브랜치 역할

- `main`: 최신 게임 코드와 번역 도구·스캐너를 관리한다.
- `korean`: 기존 한글판과 64차까지의 번역 자산을 보존한다.
- `codex/korean-pass-65`: PR #1의 65차 번역과 부팅 오류 수정 자산을 보존한다.
- `korean-next`: `main`의 코드 골격 위에 검증된 표시 문자열만 이식한다.

## 금지 사항

- unrelated histories 병합
- legacy 번역 커밋의 강제 cherry-pick
- legacy ERB 파일 전체 복사 또는 덮어쓰기
- `main`에서 삭제된 파일 복원
- 함수명, 변수명, 레이블, 조건식, 계산식, 내부 키 번역

## 이식 순서

1. `.github/scripts/korean_string_migration.py analyze`로 후보를 분류한다.
2. `automatic` 중 20~50개 파일만 한 배치로 선택한다.
3. 동일 함수와 동일 문맥의 표시 문자열만 이식한다.
4. `verify`로 `origin/main` 대비 실행 코드 골격 불변을 확인한다.
5. 번역 스캐너와 Emuera 부팅 검사를 통과시킨다.
6. 통과한 배치만 `korean-next`에 커밋한다.

## PR #1 최초 분석

상세 보고서는 `.github/migration/pr1-65-analysis/`에 있다.

| 분류 | 파일 수 |
|---|---:|
| 자동 이식 가능 | 101 |
| 부분 이식 가능 | 333 |
| 구조 변경 | 190 |
| main에서 삭제됨 | 1 |
| 코드 전용/이미 반영 | 7 |

이 수치는 실제 문자열 이식 전 분석 결과이며, 자동 분류도 배치 검증을 통과해야
최종 반영한다.
