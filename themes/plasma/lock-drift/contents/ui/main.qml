pragma ComponentBehavior: Bound

import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasmoid

WallpaperItem {
    id: root

    property real elapsed: 0
    readonly property bool animate: root.visible && root.configuration["Animate"]
                                    && Kirigami.Units.longDuration > 1
    readonly property real densityScale: Math.max(0.7, Math.min(1.8, root.height / 1080))

    function variation(index, salt) {
        const value = Math.sin((index + 1) * 12.9898 + salt * 78.233) * 43758.5453;
        return value - Math.floor(value);
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0; color: "#38253E" }
            GradientStop { position: 0.63; color: "#2B2235" }
            GradientStop { position: 1; color: "#30304C" }
        }
    }

    Image {
        id: artwork
        anchors.fill: parent
        source: root.configuration["Image"] || ""
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
        smooth: true
    }

    Timer {
        id: frame
        property double lastTime: 0
        interval: 42
        repeat: true
        running: root.animate && (artwork.status === Image.Null || artwork.status === Image.Ready)
        onRunningChanged: lastTime = 0
        onTriggered: {
            const now = Date.now();
            if (lastTime > 0)
                root.elapsed += Math.min(0.15, Math.max(0, (now - lastTime) / 1000));
            lastTime = now;
        }
    }

    Repeater {
        model: frame.running ? 24 : 0

        delegate: Item {
            id: mote

            required property int index
            readonly property bool leftLane: index < 12
            readonly property bool far: index % 3 === 0
            readonly property bool ember: index % 7 === 0
            readonly property color tint: ember ? "#E7AA78" : "#A6F5E3"
            readonly property real lifetime: (far ? 36 : 23) + root.variation(index, 1) * 19
            readonly property real offset: root.variation(index, 2)
            readonly property real phase: (root.elapsed / lifetime + offset) % 1
            readonly property real lane: (leftLane ? 0.035 : 0.705) + root.variation(index, 3) * 0.26
            readonly property real sway: Math.sin(root.elapsed * 0.49 + offset * 20) * 0.012
            readonly property real drift: (phase - 0.5) * (far ? 0.022 : 0.045)
            readonly property real fade: Math.min(1, phase * 7, (1 - phase) * 7)
            readonly property real shimmer: 0.79 + 0.21 * Math.sin(root.elapsed * 0.9 + offset * 15)

            width: ((far ? 1.5 : 2.7) + root.variation(index, 4) * 2.8) * root.densityScale
            height: width
            x: root.width * (lane + sway + drift) - width / 2
            y: root.height * (1.04 - phase * 1.1) - height / 2
            opacity: fade * shimmer * (far ? 0.46 : 0.78)

            Rectangle {
                anchors.centerIn: parent
                width: mote.width * 3.2
                height: width
                radius: width / 2
                color: mote.tint
                opacity: 0.12
            }

            Rectangle {
                anchors.fill: parent
                radius: width / 2
                color: mote.tint
            }
        }
    }
}
