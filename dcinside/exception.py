class DeletedPostException(Exception):
    def __init__(self, message="This post is already removed."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ServerException(Exception):
    def __init__(self, message="Failed to crawl due to server side error, Try it later."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class StaleElementException(Exception):
    def __str__(self):
        return "Stale element reference encountered during crawling."
