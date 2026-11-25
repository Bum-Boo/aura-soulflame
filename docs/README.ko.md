# Aura Soulflame

자주색 배경과 핑크 포커스, 민트 불꽃을 KDE와 Kitty에 적용하는 테마예요. 필요한 구성만 골라 설치하고, 가지고 있는 커서·배경화면·코덱스 펫도 같은 방식으로 가져올 수 있어요.

```sh
python3 aura.py list
python3 aura.py plan --modules kitty
python3 aura.py install --modules kitty
```

Plasma에서는 시스템 설정에서 **Aura Soulflame (Portable)** 색 구성을 선택하세요. Kitty에서는 배포된 색상 파일을 `kitty.conf`에 `include aura-soulflame.conf`로 연결하면 돼요. 스플래시·잠금화면·패널 위젯은 [구성별 설치와 적용 위치](../README.md#install-a-component)에서 볼 수 있어요.

AI에 맡기려면 이렇게 요청해 보세요.

> 이 저장소의 `AGENTS.md`를 읽고 내 OS, 데스크톱, 터미널을 확인해 줘. 내가 고른 Aura Soulflame 구성만 설치 전 미리보기로 보여 주고, 기존 설정을 보존하면서 적용해 줘. 실제 적용 여부와 되돌리는 방법도 알려 줘.

본인 이미지나 기존 커서·펫을 쓰려면 [로컬 에셋 폴더 형식](assets.md)을 따라 `--assets`를 넘기세요. 다른 터미널이나 데스크톱은 [공통 팔레트](../resources/palette.json)의 색을 해당 앱의 테마 파일로 옮길 수 있어요. [AI 적용 가이드](apply-with-ai.md)
