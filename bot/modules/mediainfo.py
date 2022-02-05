import subprocess
from bot import LOGGER, dispatcher
from telegram import ParseMode
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage


def mediainfo(update, context):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        return sendMessage('No command to execute was given.', context.bot, update)
    cmd = cmd[1]
    process = subprocess.run(cmd, capture_output=True, mediainfo=True)
    reply = ''
    stderr = process.stderr.decode('utf-8')
    stdout = process.stdout.decode('utf-8')
    if len(stdout) != 0:
        reply += f"*Stdout*\n<code>{stdout}</code>\n"
        LOGGER.info(f"Mediainfo - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n<code>{stderr}</code>\n"
        LOGGER.error(f"Mediainfo - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('@MirrorDrive #Mediainfo.txt', 'w') as file:
            file.write(reply)
        with open('@MirrorDrive #Mediainfo.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        sendMessage(reply, context.bot, update)
    else:
        sendMessage('No Reply', context.bot, update)


MEDIAINFO_HANDLER = CommandHandler(BotCommands.mediainfoCommand, mediainfo,
                                                  filters=CustomFilters.authorized_chat, run_async=True)
CustomFilters.authorized_user, run_async=True
dispatcher.add_handler(MEDIAINFO_HANDLER)





