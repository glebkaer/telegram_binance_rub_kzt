#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from telegrambot import TelegramBot

if __name__ == '__main__':
    TelegramBot(os.getenv('BotToken'))
