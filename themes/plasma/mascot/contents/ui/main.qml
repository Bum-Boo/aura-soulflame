pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore

PlasmoidItem {
    id: mascot
    readonly property bool portraitPack: false

    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: fullRepresentation
    toolTipMainText: qsTr("Aura Soulflame")
    toolTipSubText: qsTr("Click to wake the flame")

    Timer { id: wake; interval: 1500 }

    fullRepresentation: Item {
        id: slot
        implicitWidth: 50
        implicitHeight: 40
        Layout.minimumWidth: 32
        Layout.preferredWidth: 50
        Layout.minimumHeight: 26
        Layout.preferredHeight: 40

        readonly property bool glanceLeft: hover.hovered && hover.point.position.x < width / 2
        readonly property string pose: wake.running ? "awake"
            : hover.hovered ? (glanceLeft ? "look-left" : "look-right") : "lean"

        HoverHandler { id: hover }
        TapHandler { onTapped: wake.restart() }

        Image {
            anchors.centerIn: parent
            width: Math.max(0, Math.min(slot.width - 6, slot.height + 6))
            height: width
            source: mascot.portraitPack ? Qt.resolvedUrl("art/" + slot.pose + ".png") : ""
            sourceSize.width: 128
            sourceSize.height: 132
            fillMode: Image.PreserveAspectFit
        }

        AuraFlame {
            visible: !mascot.portraitPack || wake.running
            width: Math.min(slot.width * 0.50, slot.height * 0.53)
            height: width * 1.5
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: mascot.portraitPack ? slot.width * 0.24 : 0
            opacity: wake.running || hover.hovered ? 1 : 0.66
            Behavior on opacity { NumberAnimation { duration: Kirigami.Units.longDuration } }
        }
    }
}
