class Logger():
    def __init__(self,logger):
        self.logger = logger
    
    def log(self,msg):
        self.logger.info(msg)

    def error(self,msg):
        self.logger.error(msg)
