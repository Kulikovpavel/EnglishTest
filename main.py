# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import codecs
import wx
import sys

__author__ = 'Kulikov Pavel'


class Test(object):
    words_list_filename = 'words_list.txt'
    # modes = enumerate('rus', 'eng')

    def __init__(self):
        self.mode = 'eng'
        with codecs.open(Test.words_list_filename, 'r', 'utf-8') as words_file:
            data = words_file.read()
            lines = data.splitlines()
            self.words_list = [line.split('-') for line in lines if len(line.split('-')) == 2]  # take if there 2 words
        self.random = random.seed()
        self.update_index_set()

    def update_index_set(self):
        self.unused_words = set(range(len(self.words_list)))

    def set_mode(self, mode):  # 'rus' or 'eng'
        self.mode = mode

    def add_words_line(self, rus, eng):
        adding_line = [rus.lower(), eng.lower()]
        if adding_line not in self.words_list:
            self.words_list.append(adding_line)
        self.update_index_set()

    def delete_words_line(self, i):
        if 0 <= i < len(self.words_list):
            del self.words_list[i]
        self.update_index_set()

    def save_words_list(self):
        words_lines = [(line[0] + '-' + line[1]) + u'\n' for line in self.words_list]
        words_text = ''.join(words_lines)
        with codecs.open(Test.words_list_filename, 'w', 'utf-8') as words_file:
            words_file.write(words_text)

    def check_answer(self, index, answer):
        answer = answer.lower()
        if self.mode == 'rus':
            check_index = 0
        else:
            check_index = 1
        if self.words_list[index][check_index] == answer:
            return 1
        else:
            return 0

    def get_words_pair(self):
        """
        Random line from list of words
        :return: index, question word, answer word
        """
        i = random.sample(self.unused_words, 1)[0]
        self.unused_words.remove(i)
        if self.mode == 'rus':
            return i, self.words_list[i][1], self.words_list[i][0]
        else:
            return i, self.words_list[i][0], self.words_list[i][1]

    def starter_set(self):
        self.words_list = []
        self.add_words_line('погода', 'weather')
        self.add_words_line('День', 'day')
        self.add_words_line('идти', 'go')
        self.add_words_line('он', 'he')
        self.save_words_list()

    def file_starter_set(self):
        with codecs.open('rus_words.txt', 'r', 'utf-8') as rus:
            data_rus = rus.readlines()
        with codecs.open('eng_words.txt', 'r', 'utf-8') as eng:
            data_eng = eng.readlines()
        data_rus = [line.replace('\n', '').replace('\r','').lower() for line in data_rus]
        data_eng = [line.replace('\n', '').replace('\r','').lower() for line in data_eng]
        words_lines = zip(data_rus, data_eng)
        self.words_list = words_lines
        self.save_words_list()


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame, wxWidgets. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 500))
        font = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)


        panel = wx.Panel(self)
        panel.SetFont(font)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.rb1 = wx.RadioButton(panel, -1, 'Русский - > English', (10, 10), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(panel, -1, 'English -> Русский', (10, 30))
        start_btn = wx.Button(panel, label=u'Начать тест')
        start_btn.Bind(wx.EVT_BUTTON, self.OnStart)

        static_text = wx.StaticText(panel, label=u"Слово для проверки:", style=wx.ALIGN_CENTER)
        self.question = wx.StaticText(panel, size=(200, 30), label="", style=wx.ALIGN_CENTER)
        self.answer_helper = wx.StaticText(panel, size=(400, 30), label="", style=wx.ALIGN_CENTER)
        self.answer = wx.TextCtrl(panel, style=wx.PROCESS_ENTER, size=(200, 30))
        self.answer.Bind(wx.EVT_TEXT_ENTER, self.OnCheck)
        self.answer.Enable(False)

        self.check_btn = wx.Button(panel, label=u'Проверить', )
        self.check_btn.Bind(wx.EVT_BUTTON, self.OnCheck)
        self.check_btn.Enable(False)

        self.words_btn = wx.Button(panel, label='Список слов', )
        self.words_btn.Bind(wx.EVT_BUTTON, self.OpenWordsList)

        self.imagered = wx.Bitmap('red.png', wx.BITMAP_TYPE_ANY)
        self.imagegreen = wx.Bitmap('green.png', wx.BITMAP_TYPE_ANY)
        self.imageBitmap = wx.StaticBitmap(panel, wx.ID_ANY, self.imagegreen)

        vbox.Add(self.rb1, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.rb2, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(start_btn, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(static_text, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.question, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.answer, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.check_btn, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.words_btn, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.imageBitmap, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        vbox.Add(self.answer_helper, flag=wx.ALL | wx.ALIGN_CENTER, border=5)
        panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def OpenWordsList(self, e):
        words_list_frame = Words(None, u'Учим английские слова')
        words_list_frame.Show(True)

    def set_words_control(self):
        self.try_number = 0
        i, question, answer = test.get_words_pair()
        self.question.Label = question
        self.correct_answer = answer

    def OnStart(self, e):
        self.check_btn.Enable(True)
        self.answer.Enable(True)
        if self.rb1.GetValue():
            test.set_mode("eng")
        else:
            test.set_mode("rus")
        test.update_index_set()
        self.set_words_control()

    def OnCheck(self, e):
        answer = self.answer.GetValue()
        helper_text = "%s: %s" % (self.question.Label, self.correct_answer)
        # print answer, self.correct_answer
        if answer == self.correct_answer:
            # self.ShowMessage("")
            self.imageBitmap.SetBitmap(self.imagegreen)
        else:
            self.try_number += 1
            self.imageBitmap.SetBitmap(self.imagered)
            self.answer.SetValue("")
            if answer != "":
                helper_text = "Начало правильного ответа: %s" % self.correct_answer[:self.try_number]
            self.answer_helper.SetLabel(helper_text)
            return
        self.answer_helper.SetLabel(helper_text)
        self.answer.SetValue("")
        self.set_words_control()

    def ShowMessage(self, e):
        dial = wx.MessageDialog(None, 'Правильно', 'Info', wx.OK)
        dial.ShowModal()


class Words(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(380, 230))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)

        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Русский', width=140)
        self.list.InsertColumn(1, 'Английский', width=130)
        # self.list.InsertColumn(2, 'year', wx.LIST_FORMAT_RIGHT, 90)

        for i in test.words_list:
            index = self.list.InsertStringItem(sys.maxint, i[0])
            self.list.SetStringItem(index, 1, i[1])
            # self.list.SetStringItem(index, 2, i[2])
        hbox.Add(self.list, 1, wx.EXPAND)

        ID_NEW = 1
        ID_RENAME = 2
        ID_CLEAR = 3
        ID_DELETE = 4

        btnPanel = wx.Panel(panel, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        new = wx.Button(btnPanel, ID_NEW, 'Новый', size=(90, 30))
        # ren = wx.Button(btnPanel, ID_RENAME, 'Rename', size=(90, 30))
        dlt = wx.Button(btnPanel, ID_DELETE, 'Удалить', size=(90, 30))
        # clr = wx.Button(btnPanel, ID_CLEAR, 'Clear', size=(90, 30))

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=ID_RENAME)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
        # self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)

        vbox.Add((-1, 20))
        vbox.Add(new)
        # vbox.Add(ren, 0, wx.TOP, 5)
        vbox.Add(dlt, 0, wx.TOP, 5)
        # vbox.Add(clr, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)

        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.LEFT, 20)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

    def NewItem(self, event):
        text = wx.GetTextFromUser('Введите слово и перевод через дефис, "день-day"', 'Вставить пару')
        if text != '':
            words = text.split('-')
            index = self.list.InsertStringItem(sys.maxint, words[0])
            self.list.SetStringItem(index, 1, words[1])

    def OnRename(self, event):
        sel = self.listbox.GetSelection()
        text = self.listbox.GetString(sel)
        renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)
        if renamed != '':
            self.listbox.Delete(sel)
            self.listbox.Insert(renamed, sel)

    def OnDelete(self, event):
        sel = self.list.GetNextSelected(-1)
        if sel != -1:
            self.list.DeleteItem(sel)



if __name__ == "__main__":
    test = Test()
    # test.file_starter_set()
    # while len(test.unused_words) > 0:
    #     print test.get_words_pair()

    app = wx.App(redirect=True)
    frame = MyFrame(None, u'Учим английские слова')
    app.MainLoop()