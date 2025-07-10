import logging

class Logger:
    _instance = None

    def __new__(cls, fileName="AIGuideEnv.log"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            aiGuideLogger = logging.getLogger(fileName)

            logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                                datefmt='%Y-%m-%d %H:%M:%S')

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))

            fileHandler = logging.FileHandler(mode='w', filename=fileName)
            fileHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
            fileHandler.setLevel(logging.INFO)

            aiGuideLogger.addHandler(console)
            aiGuideLogger.addHandler(fileHandler)

            cls._instance.logger = aiGuideLogger
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def debug(self, message):
        Logger._instance.logger.debug(message)

    def info(self, message):
        Logger._instance.logger.info(message)

    def warning(self, message):
        Logger._instance.logger.warning(message)

    def error(self, message):
        Logger._instance.logger.error(message)

    def critical(self, message):
        Logger._instance.logger.critical(message)

    def exception(self, message):
        Logger._instance.logger.exception(message)
