import QtQuick

AuraScene {
    property int stage: 0
    awake: stage >= 2
    litFlames: Math.min(3, Math.max(0, stage))
}
