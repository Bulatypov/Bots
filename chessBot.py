import telebot
import chess
import chess.engine

# Создаем экземпляр бота и указываем токен вашего Telegram-бота
bot = telebot.TeleBot('5955590526:AAExfYT1z1BahaZ-827QMIrhDcRofXiXujw')

# Создаем экземпляр шахматного движка
engine = chess.engine.SimpleEngine.popen_uci("stockfish_15_linux_x64/stockfish_15_x64")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я шахматный бот. Чтобы начать игру, используйте команду /play.')

# Обработчик команды /play
@bot.message_handler(commands=['play'])
def play_message(message):
    global board
    board = chess.Board()
    bot.reply_to(message, 'Шахматная доска создана. Ваш ход!')

# Обработчик сообщений с ходом
@bot.message_handler(func=lambda message: True)
def handle_move(message):
    try:
        move = message.text
        board.push_san(move)  # Применяем ход к доске

        # Проверяем наличие матовой или патовой позиции
        if board.is_checkmate():
            bot.reply_to(message, 'Мат! Вы победили!')
            bot.send_message(message.chat.id, 'Чтобы начать новую игру, используйте команду /play.')
            return
        elif board.is_stalemate():
            bot.reply_to(message, 'Пат! Ничья!')
            bot.send_message(message.chat.id, 'Чтобы начать новую игру, используйте команду /play.')
            return

        # Делаем ход с помощью шахматного движка
        result = engine.play(board, chess.engine.Limit(time=2.0))
        board.push(result.move)

        # Отправляем ход шахматного движка
        bot.reply_to(message, str(result.move))

        # Проверяем наличие матовой или патовой позиции после хода шахматного движка
        if board.is_checkmate():
            bot.send_message(message.chat.id, 'Мат! Вы проиграли!')
            bot.send_message(message.chat.id, 'Чтобы начать новую игру, используйте команду /play.')
        elif board.is_stalemate():
            bot.send_message(message.chat.id, 'Пат! Ничья!')
            bot.send_message(message.chat.id, 'Чтобы начать новую игру, используйте команду /play.')

    except ValueError:
        bot.reply_to(message, 'Некорректный ход!')

# Запускаем бота
bot.polling()
