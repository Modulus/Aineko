from rx import Observable, Observer


class ArticlesObserver(Observer):

    def on_next(self, articles):
        print("Received {0}".format(articles))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))

