import io
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>684</width>
    <height>507</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>380</x>
      <y>120</y>
      <width>47</width>
      <height>13</height>
     </rect>
    </property>
    <property name="text">
     <string>Текст 2</string>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="text1">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>140</y>
      <width>291</width>
      <height>321</height>
     </rect>
    </property>
   </widget>
   <widget class="QDoubleSpinBox" name="alert_value">
    <property name="geometry">
     <rect>
      <x>160</x>
      <y>80</y>
      <width>311</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
   <widget class="QPlainTextEdit" name="text2">
    <property name="geometry">
     <rect>
      <x>380</x>
      <y>140</y>
      <width>291</width>
      <height>321</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>80</y>
      <width>131</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Порог срабатывания (%)</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>120</y>
      <width>47</width>
      <height>13</height>
     </rect>
    </property>
    <property name="text">
     <string>Текст 1</string>
    </property>
   </widget>
   <widget class="QPushButton" name="checkBtn">
    <property name="geometry">
     <rect>
      <x>300</x>
      <y>430</y>
      <width>81</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Сравнить</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>684</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class AntiPlagiarism(QMainWindow):
    def __init__(self):
        """ЗАГРУЗКА НЕОБХОДИМЫХ КОМПОНЕНТОВ ДЛЯ ИНТЕРФЕЙСА"""
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.statusbar = self.statusBar()
        self.checkBtn.clicked.connect(self.plagiat)

    def plagiat(self):
        text_one = set(self.text1.toPlainText().split('\n'))  # Разбираем первый текст на предложения
        text_two = set(self.text2.toPlainText().split('\n'))  # Анологично со вторым текстом
        tot = list(text_two | text_one)  # Объединяем множества text_one и text_two
        temp = list((text_one - text_two) | (text_two - text_one))  # Получаем уникальные предложения

        """Отношение количества уникальных строк, встречающихся в обоих текстах, к общему количеству уникальных строк"""
        plag_level = round((1 - len(temp) / len(tot)) * 100, 2)

        threshold = self.alert_value.value()  # Получаем заданный порог срабатывания

        if threshold <= plag_level:  # Если схожесть текстов больше или равна порогу срабатывания
            self.statusbar.showMessage(f'Тексты похожи на'
                                       f' {"{:.2f}".format(round(plag_level, 2))}%, плагиат')
        else:  # Если схожесть текстов меньше порога срабатывания
            self.statusbar.showMessage(f'Тексты похожи на'
                                       f' {"{:.2f}".format(round(plag_level, 2))}%, не плагиат')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AntiPlagiarism()
    ex.show()
    sys.exit(app.exec_())
