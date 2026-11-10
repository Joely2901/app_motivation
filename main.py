# -*- coding: utf-8 -*-
"""Motivation Quotidienne - application Android (Kivy)."""
import datetime
import json
import os
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from quotes import QUOTES

BG = (0.07, 0.09, 0.15, 1)
CARD = (0.12, 0.15, 0.24, 1)
ACCENT = (0.98, 0.76, 0.22, 1)
TEXT = (0.95, 0.96, 0.98, 1)
MUTED = (0.62, 0.67, 0.78, 1)


class FlatButton(Button):
    def __init__(self, bg=CARD, fg=TEXT, **kwargs):
        super().__init__(background_normal="", background_down="",
                         background_color=(0, 0, 0, 0), color=fg, **kwargs)
        self._bg = bg
        with self.canvas.before:
            self._c = Color(*bg)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self._upd, size=self._upd, state=self._state)

    def _upd(self, *_):
        self._r.pos, self._r.size = self.pos, self.size

    def _state(self, *_):
        c = self._bg
        self._c.rgba = (c[0] * 0.8, c[1] * 0.8, c[2] * 0.8, 1) if self.state == "down" else c


class MotivationApp(App):
    title = "Motivation Quotidienne"

    def build(self):
        Window.clearcolor = BG
        self.index = self._daily_index()
        self.favorites = self._load_favorites()
        self.show_favs = False

        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(14))

        self.header = Label(text="Citation du jour", font_size=sp(20), bold=True,
                            color=ACCENT, size_hint_y=None, height=dp(44))
        root.add_widget(self.header)

        self.card = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        with self.card.canvas.before:
            Color(*CARD)
            self._card_rect = RoundedRectangle(pos=self.card.pos, size=self.card.size,
                                               radius=[dp(22)])
        self.card.bind(pos=self._card_upd, size=self._card_upd)

        self.quote_label = Label(font_size=sp(22), color=TEXT, halign="center",
                                 valign="middle")
        self.quote_label.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        self.author_label = Label(font_size=sp(16), italic=True, color=MUTED,
                                  size_hint_y=None, height=dp(34))
        self.card.add_widget(self.quote_label)
        self.card.add_widget(self.author_label)
        root.add_widget(self.card)

        row1 = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(12))
        self.btn_new = FlatButton(text="Nouvelle citation", bg=ACCENT, fg=(0.1, 0.1, 0.1, 1),
                                  bold=True, font_size=sp(17))
        self.btn_new.bind(on_release=lambda *_: self.next_quote())
        self.btn_fav = FlatButton(text="Ajouter aux favoris", font_size=sp(15))
        self.btn_fav.bind(on_release=lambda *_: self.toggle_favorite())
        row1.add_widget(self.btn_new)
        row1.add_widget(self.btn_fav)
        root.add_widget(row1)

        row2 = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(12))
        self.btn_today = FlatButton(text="Citation du jour", font_size=sp(15))
        self.btn_today.bind(on_release=lambda *_: self.go_today())
        self.btn_list = FlatButton(text="Mes favoris (0)", font_size=sp(15))
        self.btn_list.bind(on_release=lambda *_: self.toggle_favs_view())
        row2.add_widget(self.btn_today)
        row2.add_widget(self.btn_list)
        root.add_widget(row2)

        self.refresh()
        return root

    # ---------- logique ----------
    def _card_upd(self, *_):
        self._card_rect.pos, self._card_rect.size = self.card.pos, self.card.size

    @staticmethod
    def _daily_index():
        today = datetime.date.today()
        return (today.toordinal()) % len(QUOTES)

    def _fav_path(self):
        return os.path.join(self.user_data_dir, "favorites.json")

    def _load_favorites(self):
        try:
            with open(self._fav_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
            return [i for i in data if isinstance(i, int) and 0 <= i < len(QUOTES)]
        except Exception:
            return []

    def _save_favorites(self):
        try:
            with open(self._fav_path(), "w", encoding="utf-8") as f:
                json.dump(self.favorites, f)
        except Exception:
            pass

    def _pool(self):
        return self.favorites if (self.show_favs and self.favorites) else None

    def next_quote(self):
        pool = self._pool()
        if pool:
            candidates = [i for i in pool if i != self.index] or pool
        else:
            candidates = [i for i in range(len(QUOTES)) if i != self.index]
        self.index = random.choice(candidates)
        self.header.text = "Mes favoris" if pool else "Une pensée pour toi"
        self.refresh()

    def go_today(self):
        self.show_favs = False
        self.index = self._daily_index()
        self.header.text = "Citation du jour"
        self.refresh()

    def toggle_favorite(self):
        if self.index in self.favorites:
            self.favorites.remove(self.index)
        else:
            self.favorites.append(self.index)
        self._save_favorites()
        self.refresh()

    def toggle_favs_view(self):
        if not self.favorites:
            self.header.text = "Aucun favori pour l'instant"
            return
        self.show_favs = not self.show_favs
        if self.show_favs:
            self.index = random.choice(self.favorites)
            self.header.text = "Mes favoris"
        else:
            self.header.text = "Une pensée pour toi"
        self.refresh()

    def refresh(self):
        text, author = QUOTES[self.index]
        self.quote_label.text = "« %s »" % text
        self.author_label.text = "— %s" % author
        self.btn_fav.text = ("Retirer des favoris" if self.index in self.favorites
                             else "Ajouter aux favoris")
        self.btn_list.text = ("Tout afficher" if self.show_favs
                              else "Mes favoris (%d)" % len(self.favorites))


if __name__ == "__main__":
    MotivationApp().run()
