class DeletedPostException(Exception):
    def __str__(self):
        return "This post is already removed."


class ServerException(Exception):
    def __str__(self):
        return "Failed to crawl due to server side error, Try it later."
