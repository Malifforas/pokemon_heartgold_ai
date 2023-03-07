import logging
import keyboard

def create_logger(log_file):
    logger = logging.getLogger('debug_logger')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = create_logger('debug.log')


def check_keypresses():
    while True:
        try:
            if keyboard.is_pressed('up'):
                logger.debug('AI pressed Up')
            elif keyboard.is_pressed('down'):
                logger.debug('AI pressed Down')
            elif keyboard.is_pressed('left'):
                logger.debug('AI pressed Left')
            elif keyboard.is_pressed('right'):
                logger.debug('AI pressed Right')
            elif keyboard.is_pressed('z'):
                logger.debug('AI pressed A')
            elif keyboard.is_pressed('x'):
                logger.debug('AI pressed B')
            elif keyboard.is_pressed('enter'):
                logger.debug('AI pressed Start')
            elif keyboard.is_pressed('backspace'):
                logger.debug('AI pressed Select')
        except:
            break
