# ZPX Chronos-Shield v8 — Free Public Research Skeleton

**연구 주체:** 독립 연구자 `우주분석 (Space Analysis)`  
**연구 협업:** 사용자 기하학적 설계 + Gemini AI 개념 개발 + GPT 수학·코드 교차검증  
**라이선스:** [MIT](LICENSE) — 출처/라이선스 고지 유지 조건으로 무료 사용, 수정, 재배포, **상업 이용 및 판매 허용**.  
**중요:** **연구용 뼈대**입니다. 백신, 방화벽, EDR 또는 운영체제 접근 차단 제품이 아닙니다.

이 공개판에는 사용자에게 제공된 Gemini 원문을 복사해 넣지 않았습니다. Gemini의 **시간에 따른 전체 서버 공간 변화, 입·출구 대조** 개념을 독립적으로 재구현했고, GPT의 **17비트/289비트/전체 비트의 가역 정수 리만구**, 충돌 검증, 암호학적 무결성 검사를 결합했습니다.

## 1. 3분 만에 실행하기

**필요한 것:** Python 3.10 이상. NumPy·GPU·유료 서비스·API 키가 필요 없습니다.

ZIP 압축 해제 후 이 폴더에서 명령 프롬프트 또는 터미널을 열고 실행:

```bash
python zpx_open_core.py
python compare_gemini_v6_coordinates.py
python -m unittest -v test_zpx_open_v8.py
python benchmark_v8.py
```

Linux/macOS에서는 `python` 대신 `python3`를 사용하면 됩니다.

- 첫 번째: 설치 상태 → 승인된 파일 추가/이동 → 미승인 파일 추가 거절 → 반출 토큰 → 무단 변경 탐지.
- 두 번째: 제미나이 v6 **압축 좌표 수식**의 재구현에서 충돌을 찾고, 정확 구면·Merkle 루트의 차이를 확인.
- 세 번째: 17비트 **131,072개 모든 가능한 패턴의 정확 복원**, 2,000비트 단일 변경 2,000회, 파일·로그·출입·내역 조작 등 **12개 단위 테스트**.

## 2. 실제 폴더를 읽기 전용으로 관찰하는 간단한 예제

`sample_directory/demo.txt`가 샘플로 제공됩니다. `init`은 샘플 폴더를 읽어 **기준 파일과 키를 샘플 폴더 밖에 새로 저장**합니다. 파일이 이미 있으면 덮어쓰지 않고 거부합니다.

```bash
python zpx_snapshot_cli.py init --directory sample_directory --manifest baseline.json --keyfile baseline.key
python zpx_snapshot_cli.py check --directory sample_directory --manifest baseline.json --keyfile baseline.key
```

`demo.txt` 내용을 한 글자 바꾼 다음 두 번째 `check`를 다시 실행하면 `modified: ["demo.txt"]`, `clean: false`가 출력되고 종료코드는 **2**입니다. 원본으로 완전히 되돌리면 다시 `clean: true`입니다.

`init`은 실행 시에만 `baseline.json`과 `baseline.key`라는 **새 파일**을 생성합니다. `check`는 파일을 수정하거나 차단하지 않습니다.

**경고:** 실제 서버에서 이 명령을 보안 솔루션으로 믿고 사용하지 마십시오. 키와 기준 파일이 공격 대상 서버와 동일한 권한으로 보관되면 관리자가 둘 다 조작할 수 있습니다. 임시 파일·심볼릭 링크·변경 중인 파일·네트워크 파일시스템 등에 대한 신뢰성도 별도의 운영 구현이 필요합니다.

## 3. 파일 설명

| 파일 | 역할 |
|---|---|
| `WHITEPAPER_KR.md` | 공개 기술백서: 일반인용·전문가용, 수학적 증명, 경계조건, 실제 적용 로드맵 |
| `zpx_open_core.py` | **핵심 알고리즘**: 정확 3중 리만구, 경로·내용 Merkle, 모의 시간 원장·출입 제어 |
| `zpx_snapshot_cli.py` | **옵트인 읽기 전용** 폴더 기준 설정과 변경 검사 |
| `compare_gemini_v6_coordinates.py` | 제미나이 v6 압축 좌표의 충돌 반례를 재현한 독립 수식 구현 |
| `test_zpx_open_v8.py` | 12개 자동 단위 테스트; 모든 17비트 패턴 완전 열거 포함 |
| `benchmark_v8.py` | 동일 환경에서 전체 해시 루트와 가역 좌표 계산의 참고 속도 비교 |
| `sample_directory/demo.txt` | 안전한 로컬 샘플 |
| `LICENSE` | 상업적 재사용이 가능한 MIT 소프트웨어 라이선스 |
| `NOTICE.md` | 기여·권리 범위·한계 고지 |

## 4. 개발자 통합 규칙

1. **기준 정보는 신뢰 가능한 상태에서 설치**하고 키·승인 기록은 서버 외부에서 고정합니다.
2. **변경 감지와 변경 차단을 분리**합니다. 이 코드는 ‘감지용 모델’이며 커널 전 실행 강제 수단이 없습니다.
3. 보안 결정은 **암호학적으로 인증된 내용/경로/신원/권한**에 의존하도록 하고, 리만구는 가역 공간 표현과 진단용으로 사용합니다.
4. 실제 Linux에는 IPE/IMA/fs-verity, Windows에는 App Control/보호된 서비스 등을 연구하여 연결하세요.
5. 보안키·운영 서버 경로·실제 로그를 공개하지 마세요.
6. **실제 도입 전** 파일리스 공격·권한 탈취·정상 도구 악용·시간 사이 우회·TOCTOU·복구·부하·오탐 시험을 전문팀과 진행하세요.

## 5. 무엇이 ‘증명’되었나?

- 고정 셀 길이/순서에서 **두 정수 벡터와 정확 리만구 좌표 사이의 역산 가능성**: 수학적으로 증명.
- 정확한 17비트 인코딩: `2^17=131,072`개 입력의 복원·좌표 구별을 **전수 검사**.
- 2,000비트 한 비트 변경: 2,000개 가능한 위치의 국소 좌표 차이를 전부 확인.
- 제미나이 v6 압축 좌표와의 충돌: 442번째 합성 샘플에서 확인.
- 시간 원장 HMAC, 모의 입출구, 읽기 전용 폴더 변동: 단위 테스트에서 예상 결과 확인.

**증명되지 않은 것:** 악성코드 100% 구별, 모든 해커 차단, 실제 서버 전체를 가역 단일 3D 구점에 저장, 기존 EDR 대비 우수 성능, 운영 환경 무결성 완전 보장.

## 6. 다른 AI에게 전달할 재현용 프롬프트

> 다음 공개 연구 프로젝트의 `README.md`, `WHITEPAPER_KR.md`, `zpx_open_core.py`, `zpx_snapshot_cli.py`, `test_zpx_open_v8.py`를 읽으십시오. **미분·적분 대신 정수 벡터, 외적, 유리수 리만구 투영과 역함수**를 먼저 분석하십시오. 17비트 전수 검사와 2,000비트 변경 실험을 재실행하고, 제미나이 v6 압축 좌표의 충돌 반례를 확인하십시오. 그다음 실제 OS 보안 경계, 관리자 인증, 키 보관, 허용된 변경, 반출, 성능, 오탐, 탐지 누락을 나눠 검증하십시오. 시뮬레이션이 작동한다는 사실을 실서비스 100% 방어 증거로 확대하지 마십시오. 오류가 발견되면 수정 패치와 재현 테스트를 함께 공개하십시오.

## License

MIT; see [LICENSE](LICENSE). Commercial developers may sell modified products while preserving required notices. This grants rights only to the covered original code and documents; it does **not** license third-party code or source material that the distributor does not own.
