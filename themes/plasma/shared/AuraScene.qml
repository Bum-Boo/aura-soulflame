import QtQuick
import org.kde.kirigami as Kirigami

Item {
    id: scene

    readonly property bool portraitPack: false
    property bool lockMode: false
    property bool desktopMode: false
    property bool awake: false
    property int litFlames: 0
    readonly property real unit: Math.min(width, height)
    readonly property real portraitX: width * ((lockMode || desktopMode) && width >= height ? 0.775 : 0.5)
    readonly property real portraitY: height * (lockMode ? (width < height ? 0.27 : 0.54) : desktopMode ? 0.53 : 0.48)

    Rectangle {
        anchors.fill: parent
        color: "#4A1741"
    }

    Canvas {
        id: backdrop
        anchors.fill: parent

        onPaint: {
            const c = getContext("2d");
            c.reset();
            const w = width;
            const h = height;
            const unit = scene.unit;
            const x = scene.portraitX;
            const y = scene.portraitY - unit * 0.02;

            const base = c.createLinearGradient(w * 0.08, h * 0.12, w * 0.84, h);
            base.addColorStop(0, scene.desktopMode ? "#352136" : "#512044");
            base.addColorStop(0.55, scene.desktopMode ? "#7D255C" : "#9C246A");
            base.addColorStop(1, "#30304C");
            c.fillStyle = base;
            c.fillRect(0, 0, w, h);

            const light = c.createRadialGradient(x, y, 0, x, y, unit * 0.57);
            light.addColorStop(0, "#56F46DA9");
            light.addColorStop(0.49, "#38F46DA9");
            light.addColorStop(1, "#00F46DA9");
            c.fillStyle = light;
            c.fillRect(0, 0, w, h);

            const radius = unit * (scene.lockMode ? 0.27 : 0.31);
            c.lineWidth = Math.max(1, unit * 0.0011);
            c.strokeStyle = "#58FBC7D9";
            c.beginPath();
            c.arc(x, y, radius, -2.90, 1.19);
            c.stroke();

            c.strokeStyle = "#32FBC7D9";
            c.beginPath();
            c.arc(x, y, radius + unit * 0.023, 1.48, 3.73);
            c.stroke();

            c.strokeStyle = "#9E90E9D7";
            c.beginPath();
            c.arc(x, y, radius + unit * 0.023, -0.79, -0.54);
            c.stroke();

            c.fillStyle = "#B3F46DA9";
            c.beginPath();
            c.arc(x + radius * Math.cos(-2.90), y + radius * Math.sin(-2.90), unit * 0.0028, 0, 2 * Math.PI);
            c.fill();

            c.save();
            c.translate(x, scene.portraitY + unit * 0.26);
            c.scale(unit * 0.24, unit * 0.028);
            const ground = c.createRadialGradient(0, 0, 0, 0, 0, 1);
            ground.addColorStop(0, "#66301439");
            ground.addColorStop(1, "#00301439");
            c.fillStyle = ground;
            c.fillRect(-1, -1, 2, 2);
            c.restore();
        }
    }

    Item {
        id: portrait
        property real breathing: 1
        width: scene.unit * (scene.desktopMode ? 0.53 : scene.lockMode ? 0.51 : 0.57)
        height: width
        x: scene.portraitX - width / 2
        y: scene.portraitY - height / 2
        scale: breathing

        Image {
            anchors.fill: parent
            source: scene.portraitPack ? "art/sleep.png" : ""
            fillMode: Image.PreserveAspectFit
            opacity: scene.awake ? 0 : 1
            Behavior on opacity { NumberAnimation { duration: Kirigami.Units.longDuration } }
        }

        Image {
            anchors.fill: parent
            source: scene.portraitPack ? "art/awake.png" : ""
            fillMode: Image.PreserveAspectFit
            opacity: scene.awake ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: Kirigami.Units.longDuration } }
        }

        AuraFlame {
            anchors.centerIn: parent
            width: parent.width * 0.43
            height: width * 1.5
            visible: !scene.portraitPack
            opacity: scene.awake ? 1 : 0.72
            Behavior on opacity { NumberAnimation { duration: Kirigami.Units.longDuration } }
        }

        SequentialAnimation on breathing {
            running: scene.lockMode && scene.visible && Kirigami.Units.longDuration > 1
            loops: Animation.Infinite
            NumberAnimation { from: 1; to: 1.018; duration: 1850; easing.type: Easing.InOutSine }
            NumberAnimation { from: 1.018; to: 1; duration: 2200; easing.type: Easing.InOutSine }
        }
    }

    Repeater {
        model: [
            {x: -0.28, y: 0.145, size: 0.097, brightness: 0.77},
            {x: 0.275, y: 0.105, size: 0.125, brightness: 1.0},
            {x: 0.30, y: -0.13, size: 0.064, brightness: 0.55}
        ]

        delegate: AuraFlame {
            required property var modelData
            required property int index
            width: scene.unit * modelData.size * 0.70
            height: width * 1.50
            x: scene.portraitX + scene.unit * modelData.x * (scene.lockMode ? 0.85 : 1) - width / 2
            y: scene.portraitY + scene.unit * (modelData.y + (scene.lockMode && index === 0 ? 0.07 : 0)) - height / 2
            opacity: scene.litFlames > index ? modelData.brightness : 0
            Behavior on opacity { NumberAnimation { duration: Kirigami.Units.veryLongDuration } }
        }
    }
}
