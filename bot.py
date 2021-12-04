from datetime import timedelta
from parser import get_info_by_link, get_status_by_link

import telegram
from env import CHAT_ID, NAME_LINK, TOKEN, HOURS, STATUS_LINK, STATUS_COLUMN
from telegram.ext import Updater


def job(context: telegram.ext.CallbackContext) -> None:
    content = ""
    for name, link in NAME_LINK.items():
        try:
            info = get_info_by_link(link)
        except Exception:
            content += f"{name}: cannot fetch info"
            continue

        content += f"{name}: {info} \n"

    try:
        status = get_status_by_link(STATUS_LINK, STATUS_COLUMN)
        content += f"Status: {status}"
    except Exception:
        pass

    context.bot.send_message(chat_id=CHAT_ID, text=content)


def build_updater(token: str) -> Updater:
    updater = Updater(token, use_context=True)
    return updater


def configure_queue(updater: Updater) -> None:
    queue = updater.job_queue
    queue.run_repeating(job, interval=timedelta(hours=HOURS), first=10)


def run(updater: Updater) -> None:
    updater.start_polling()
    updater.idle()


def main() -> None:
    updater = build_updater(TOKEN)
    configure_queue(updater)
    run(updater)


if __name__ == "__main__":
    main()
