from celery import Celery

#app = Celery('tasks', broker='redis://localhost:6379/0')



app = Celery('proj',
             broker='redis://localhost:6379/0')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()