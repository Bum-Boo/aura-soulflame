// Aura · Scales of Obedience — SDDM 로그인 테마 (Qt6)
import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: 1920; height: 1080

    readonly property color cBg:    "#2b2235"
    readonly property color cPink:  "#f46da9"
    readonly property color cMint:  "#90e9d7"
    readonly property color cPale:  "#deffF2"
    readonly property color cMuted: "#c9b3d6"
    readonly property string symScales: ""
    readonly property string symSword:  ""
    readonly property string symHead:   ""
    property bool failed: false

    FontLoader { id: symFont; source: "AuraSymbols.otf" }
    function sym(c) { return "<span style=\"font-family:'" + symFont.name + "'\">" + c + "</span>" }

    // --- 배경 ---
    Image {
        anchors.fill: parent
        source: config.background
        fillMode: Image.PreserveAspectCrop
        smooth: true
        asynchronous: false
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0;  color: "#f01a1422" }
            GradientStop { position: 0.32; color: "#c02b2235" }
            GradientStop { position: 0.55; color: "#002b2235" }
        }
    }
    Rectangle {
        anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: parent.bottom
        height: parent.height * 0.25
        gradient: Gradient {
            GradientStop { position: 0; color: "#002b2235" }
            GradientStop { position: 1; color: "#a01a1422" }
        }
    }

    // --- 시계 ---
    Column {
        id: clock
        x: root.width * 0.07; y: root.height * 0.12
        spacing: 2
        Text {
            id: timeText
            color: root.cPale; font.family: "Noto Sans"; font.pixelSize: 96; font.weight: Font.Light
            text: Qt.formatTime(new Date(), "HH:mm")
        }
        Text {
            id: dateText
            color: root.cMuted; font.family: "Noto Sans"; font.pixelSize: 22
            text: Qt.formatDate(new Date(), "dddd, d MMMM yyyy")
        }
        Timer {
            interval: 1000; running: true; repeat: true
            onTriggered: {
                timeText.text = Qt.formatTime(new Date(), "HH:mm")
                dateText.text = Qt.formatDate(new Date(), "dddd, d MMMM yyyy")
            }
        }
    }

    // --- 로그인 폼 ---
    Column {
        id: form
        x: root.width * 0.07; y: root.height * 0.46
        width: 400
        spacing: 14

        Row {
            spacing: 12
            // 소울플레임: 로그인 실패 시 크게 타오름
            Image {
                id: flame
                width: 36; height: 51
                property int frame: 0
                source: "flame/flame-" + (frame < 10 ? "0" : "") + frame + ".png"
                fillMode: Image.PreserveAspectFit
                smooth: true
                anchors.bottom: parent.bottom
                scale: root.failed ? 1.6 : 1.0
                transformOrigin: Item.Bottom
                Behavior on scale { NumberAnimation { duration: 260; easing.type: Easing.OutBack } }
                Timer { interval: 50; running: true; repeat: true; onTriggered: flame.frame = (flame.frame + 1) % 36 }
            }
            Text {
                text: "Scales of Obedience"
                color: root.cMint; font.family: "Noto Serif"; font.pixelSize: 32
            }
        }
        Text {
            textFormat: Text.RichText
            text: root.failed ? root.sym(root.symSword) + "&nbsp;&nbsp;천칭이 기울었다. 다시 말해라." : "Kneel, and state your name."
            color: root.failed ? root.cPink : root.cMuted
            font.family: "Noto Sans"
            font.pixelSize: 15
        }

        Item { width: 1; height: 6 }

        component AuraField: TextField {
            width: form.width; height: 48
            leftPadding: 46
            color: root.cPale
            placeholderTextColor: "#8a7a99"
            font.family: "Noto Sans"; font.pixelSize: 17
            selectByMouse: true
            property string icon: ""
            background: Rectangle {
                color: "#d02b2235"; radius: 8
                border.width: parent.activeFocus ? 2 : 1
                border.color: parent.activeFocus ? root.cPink : "#609c246a"
                Text {
                    anchors.left: parent.left; anchors.leftMargin: 14
                    anchors.verticalCenter: parent.verticalCenter
                    text: parent.parent.icon
                    font.family: symFont.name; font.pixelSize: 20
                    color: parent.parent.activeFocus ? root.cMint : root.cMuted
                }
            }
        }

        AuraField {
            id: username
            icon: root.symHead
            placeholderText: "이름"
            text: userModel.lastUser
            KeyNavigation.tab: password
            Keys.onReturnPressed: password.forceActiveFocus()
            Keys.onEnterPressed: password.forceActiveFocus()
        }
        AuraField {
            id: password
            icon: root.symScales
            placeholderText: "비밀번호"
            echoMode: TextInput.Password
            passwordCharacter: "•"
            KeyNavigation.tab: session
            onTextChanged: if (text.length > 0) root.failed = false
            Keys.onReturnPressed: root.doLogin()
            Keys.onEnterPressed: root.doLogin()
        }

        Row {
            spacing: 10
            ComboBox {
                id: session
                width: form.width - loginBtn.width - 10; height: 40
                model: sessionModel
                textRole: "name"
                currentIndex: sessionModel.lastIndex
                font.family: "Noto Sans"; font.pixelSize: 14
                contentItem: Text {
                    leftPadding: 14
                    text: session.displayText
                    color: root.cMuted; font: session.font
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }
                background: Rectangle { color: "#a02b2235"; radius: 8; border.color: "#409c246a" }
                delegate: ItemDelegate {
                    width: session.width
                    contentItem: Text { text: model.name; color: root.cPale; font: session.font }
                    background: Rectangle { color: session.highlightedIndex === index ? "#9c246a" : "#2b2235" }
                }
            }
            Rectangle {
                id: loginBtn
                width: 96; height: 40; radius: 8
                color: loginMouse.containsMouse ? root.cPink : "#9c246a"
                Text {
                    anchors.centerIn: parent
                    textFormat: Text.RichText
                    text: "입장"
                    color: "white"; font.family: "Noto Sans"; font.pixelSize: 15; font.bold: true
                }
                MouseArea { id: loginMouse; anchors.fill: parent; hoverEnabled: true; onClicked: root.doLogin() }
            }
        }
    }

    // --- 전원 버튼 ---
    Row {
        anchors.right: parent.right; anchors.bottom: parent.bottom
        anchors.margins: 36
        spacing: 26
        Repeater {
            model: [
                { label: "절전",   act: "suspend",  ok: sddm.canSuspend },
                { label: "재시작", act: "reboot",   ok: sddm.canReboot },
                { label: "종료",   act: "poweroff", ok: sddm.canPowerOff }
            ]
            delegate: Text {
                visible: modelData.ok
                text: modelData.label
                color: pm.containsMouse ? root.cPink : root.cMuted
                font.family: "Noto Sans"; font.pixelSize: 16
                MouseArea {
                    id: pm; anchors.fill: parent; anchors.margins: -8; hoverEnabled: true
                    onClicked: {
                        if (modelData.act === "suspend") sddm.suspend()
                        else if (modelData.act === "reboot") sddm.reboot()
                        else sddm.powerOff()
                    }
                }
            }
        }
    }

    // 아래 왼쪽: 심볼 서명
    Text {
        anchors.left: parent.left; anchors.bottom: parent.bottom
        anchors.leftMargin: root.width * 0.07; anchors.bottomMargin: 36
        text: root.symScales + "   " + root.symSword + "   " + root.symHead
        color: "#809c246a"; font.family: symFont.name; font.pixelSize: 22
    }

    function doLogin() {
        sddm.login(username.text, password.text, session.currentIndex)
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.failed = true
            password.text = ""
            password.forceActiveFocus()
        }
        function onLoginSucceeded() { root.failed = false }
    }

    Component.onCompleted: {
        if (username.text.length > 0) password.forceActiveFocus()
        else username.forceActiveFocus()
    }
}
