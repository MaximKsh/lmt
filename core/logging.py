class LmtLogger:
    def trace(self, text):
        raise NotImplementedError()

    def warn(self, text):
        raise NotImplementedError()

    def err(self, text):
        raise NotImplementedError()


class WarnConsoleLogger(LmtLogger):

    def trace(self, text):
        pass

    def warn(self, text):
        print(text)

    def err(self, text):
        print(text)


class TraceConsoleLogger(LmtLogger):

    def trace(self, text):
        print(text)

    def warn(self, text):
        print(text)

    def err(self, text):
        print(text)


def get_suitable_logger(config):
    return TraceConsoleLogger() if config.verbose else WarnConsoleLogger()
