import QtQuick
import QtQuick.Controls as Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.FormLayout {
    id: form
    property alias cfg_Image: imageUrl.text
    property alias cfg_Animate: animate.checked

    RowLayout {
        Kirigami.FormData.label: qsTr("Image")
        Controls.TextField {
            id: imageUrl
            Layout.fillWidth: true
            placeholderText: qsTr("Optional local image URL")
        }
        Controls.Button {
            text: qsTr("Browse…")
            onClicked: picker.open()
        }
    }

    Controls.CheckBox {
        id: animate
        text: qsTr("Animate drifting embers")
    }

    FileDialog {
        id: picker
        title: qsTr("Choose a wallpaper image")
        nameFilters: [qsTr("Images (*.png *.jpg *.jpeg *.webp)")]
        onAccepted: imageUrl.text = selectedFile.toString()
    }
}
