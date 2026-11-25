# Aura Soulflame

[English](../README.md) · **한국어** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

짙은 자주색 배경, 분홍색 선택 강조, 민트색 불꽃을 담은 데스크톱 테마예요. KDE 효과와 Kitty 색상표를 골라 쓰고, 가지고 있는 배경화면·커서·코덱스 펫도 가져올 수 있어요.

![로그인 후 중앙 민트색 불꽃과 주변의 작은 불꽃이 차례로 켜지는 Plasma 스플래시](media/splash.gif)

**시작 화면**(`plasma-splash`)은 로그인 후 Plasma가 시작될 때 재생돼요. [정지 화면으로 보기](splash.png)

## 구성별로 무엇이 달라지나요?

### KDE Plasma 6

| 색 구성 | 야간 잠금화면 |
| --- | --- |
| <img src="media/colors.png" width="380" alt="자주색 바탕과 분홍색 선택 강조가 보이는 Plasma 색 구성 설정"> | <img src="media/night.png" width="380" alt="자주색 그라데이션 오른쪽에 민트색 불꽃이 있는 야간 잠금화면"> |
| `plasma-colors`는 창, 글자, 포커스, 선택 영역의 색을 바꿔요. 시스템 설정의 **색 구성**에서 **Aura Soulflame (Portable)**을 고르세요. | `plasma-lock`은 불꽃이 떠 있는 잠금화면 배경을 추가해요. **화면 잠금 → 모양 → 배경화면 유형**에서 **Aura Soulflame Night**를 고르세요. |

| 떠오르는 불티 | 패널 위젯 |
| --- | --- |
| <img src="media/drift.gif" width="380" alt="어두운 배경 양쪽에서 민트색과 주황색 불티가 천천히 위로 떠오르는 모습"> | <img src="media/panel.gif" width="258" alt="클릭하면 밝아지는 민트색 불꽃 패널 위젯"> |
| `plasma-drift`는 그라데이션이나 내가 고른 이미지 위에 불티를 띄워요. 바탕화면이나 잠금화면 배경 설정에서 **Aura Soulflame Drift**를 고르세요. 설정에서 애니메이션을 끌 수 있어요. | `plasma-panel`은 패널이나 바탕화면에 작은 불꽃을 올려요. **편집 모드 → 위젯 추가**에서 **Aura Soulflame Panel**을 고르고, 불꽃을 클릭하면 밝아져요. |

시작 화면은 시스템 설정의 **시작 화면**에서 **Aura Soulflame Splash**를 선택하면 돼요.

### Kitty 터미널

![자주색 배경, 민트색 커서, 분홍색 강조와 ANSI 16색을 보여 주는 Kitty 터미널](media/kitty.png)

`kitty`에는 배경·글자·커서·선택 영역·탭·ANSI 색이 들어 있어요. `kitty --config <aura-soulflame.conf 경로>`로 별도 창에서 먼저 볼 수 있어요. 계속 쓰려면 `kitty.conf`에서 기존 색상 프리셋 아래에 `include aura-soulflame.conf`를 추가하세요. Kitty가 다른 설정 폴더를 쓰면 설치할 때 `KITTY_CONFIG_DIRECTORY`를 그 폴더로 지정하세요.

### 가지고 있는 파일 쓰기

| 구성 | 준비할 파일 | 적용 위치 |
| --- | --- | --- |
| `cursor` | `index.theme`와 `cursors/`가 있는 Xcursor 테마 폴더 | Linux 데스크톱이나 컴포지터의 커서 설정 |
| `wallpapers` | PNG, JPEG, WebP 배경화면 | 운영체제의 배경화면 선택기 |
| `codex-pet` | `pet.json`과 여기에 지정된 스프라이트 시트 | Codex 펫 선택기. 호환 터미널에서는 `/pets`를 열고 `pet.json`의 ID로 검색해요. |
| Plasma 초상화 | 구성에서 쓰는 포즈별 투명 PNG | 시작 화면, 야간 배경, 패널에서 기본 불꽃 대신 사용 |

[에셋 폴더 형식](assets.md)에서 파일 이름과 `--assets` 사용 예시를 볼 수 있어요. 다른 터미널이나 데스크톱에 색을 옮길 때는 [공통 팔레트](../resources/palette.json)의 역할별 색과 ANSI 16색을 해당 앱의 테마 설정에 매핑하면 돼요.

## 설치하고 적용하기

**Python 3.9 이상**으로 저장소 루트에서 실행하세요. 아래 Kitty 예시는 Linux와 macOS에서 사용할 수 있어요. KDE 구성은 Linux의 Plasma 6이 필요하고, Windows에서 배경화면이나 펫을 가져올 때는 `py -3 aura.py`를 사용하세요.

```sh
python3 aura.py list
python3 aura.py plan --modules kitty
python3 aura.py install --modules kitty
python3 aura.py status --modules kitty
```

Linux에서 KDE 색과 시작 화면을 함께 쓰려면 같은 명령에서 `--modules plasma-colors plasma-splash`를 지정하세요. `plan`에서 파일이 들어갈 경로를 확인하고, 설치 뒤 위 표에 나온 앱이나 데스크톱 설정에서 활성화하세요.

되돌리려면 이전 테마를 선택하거나 Kitty의 `include` 줄을 제거한 뒤, 설치한 모듈에 대해 `python3 aura.py uninstall --modules kitty`를 실행하세요. 설치 후 편집한 파일은 `modified`로 표시되고 그대로 남아요.

## AI에 적용을 맡기기

> `AGENTS.md`를 읽고 내 운영체제, 데스크톱, 대상 앱을 확인해 줘. 내가 고른 Aura Soulflame 구성의 설치 미리보기를 보여 주고, 기존 설정을 보존하면서 적용해 줘. 앱에서 적용 여부를 확인하고 되돌리는 방법도 알려 줘. 내 에셋 팩 경로는 `<경로>`야.

[AI 적용 가이드](apply-with-ai.md) · [모듈 목록](../modules.json) · [출처와 크레딧](credits.md)

미리보기는 격리된 Linux 환경에서 KDE Plasma 6과 Kitty를 실행해 촬영했어요. 설치 도구는 `python3 -m unittest discover -s tests -v`로 점검할 수 있어요.
