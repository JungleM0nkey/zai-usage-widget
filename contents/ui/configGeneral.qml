/*
    SPDX-License-Identifier: GPL-3.0-or-later
*/

import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.SimpleKCM {
    id: configPage

    property int cfg_refreshInterval
    property bool cfg_showIcon
    property double cfg_backgroundOpacity

    Kirigami.FormLayout {
        RowLayout {
            Kirigami.FormData.label: i18n("Refresh interval:")

            QQC2.SpinBox {
                id: refreshSpinBox
                from: 1
                to: 999
                stepSize: 1
                value: cfg_refreshInterval

                onValueChanged: {
                    cfg_refreshInterval = value
                }
            }

            QQC2.Label {
                text: i18n("minutes")
            }
        }

        QQC2.Label {
            visible: cfg_refreshInterval < 2
            text: "⚠ " + i18n("Values under 2 min hit the API very frequently")
            color: Kirigami.Theme.negativeTextColor
            font.italic: true
            Layout.fillWidth: true
        }

        Kirigami.Separator {
            Kirigami.FormData.isSection: true
            Kirigami.FormData.label: i18n("Panel display")
        }

        QQC2.CheckBox {
            Kirigami.FormData.label: i18n("Icon:")
            text: i18n("Show Z.ai icon")
            checked: cfg_showIcon
            onCheckedChanged: cfg_showIcon = checked
        }

        RowLayout {
            Kirigami.FormData.label: i18n("Background opacity (desktop):")

            QQC2.Slider {
                id: opacitySlider
                from: 0.0
                to: 1.0
                stepSize: 0.05
                value: cfg_backgroundOpacity
                Layout.preferredWidth: Kirigami.Units.gridUnit * 10

                onMoved: {
                    cfg_backgroundOpacity = value
                }
            }

            QQC2.Label {
                text: Math.round(opacitySlider.value * 100) + "%"
                Layout.preferredWidth: Kirigami.Units.gridUnit * 2
            }
        }
    }
}
