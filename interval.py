import concurrent.futures
import time
import rx
from rx.core.blockingobservable import BlockingObservable

nums = [1,2,3,4,5,6,7,8,9,10]

def f(x):
    return x * x
def sleep(t):
    time.sleep(t)
    return t


def output(result):
    print('%d seconds' % result)

# def main():

    # with concurrent.futures.ProcessPoolExecutor(2) as executor:
    #     rx.Observable.interval(200)\
    #         .flat_map(lambda s: executor.submit(sleep, s))\
    #         .subscribe(output)


if __name__ == '__main__':
    from rx import Observable

    #
    # source = BlockingObservable.interval(1000).controlled()
    # source.take_while(lambda it: it > 0).subscribe(
    #     on_next=lambda x: print("on_next %s" % x),
    #     on_error=lambda e: print("on_error %s" % e)
    # )

    # with concurrent.futures.ProcessPoolExecutor(2) as executor:
    #     rx.Observable.interval(200) \
    #         .subscribe(lambda s: executor.submit(print, s))

    #rx.Observable.interval(20).to_blocking().last(lambda x : print(x))#
    rx.Observable.take_last_with_time(200).to_blocking().for_each(lambda x : print(x))
    #rx.Observable.interval(500).to_blocking().subscribe(on_next=lambda i: print("PROCESS 2: {1}".format(i)),
     #                                                   on_error=lambda e: print(e), on_completed=lambda: print("PROCESS done!"))

   # input("jadda")
    #while True:
     #   time.sleep(1000)