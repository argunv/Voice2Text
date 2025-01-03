#!/bin/bash

case "$1" in
  bot)
    python3 -m app.bot.bot
    ;;
  consumer)
    python3 -m app.consumer
    ;;
  migrate)
    python3 -m scripts.migrate
    ;;
  *)
    echo "Неизвестная команда. Используйте bot, consumer или migrate."
    exit 1
    ;;
esac
