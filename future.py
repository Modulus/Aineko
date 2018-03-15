import concurrent.futures
import time
import rx

nums = [1,2,3,4,5,6,7,8,9,10]

def f(x):
    return x * x
def sleep(t):
    time.sleep(t)
    return t


def output(result):
    print('%d seconds' % result)

def main():
    # Make sure the map and function are working
    print([val for val in map(f, nums)])

    # Test to make sure concurrent map is working
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print([val for val in executor.map(f, nums)])

    seconds = [5,1,2,4,3]
    # print(x[::11000])
    # print(data)
    # print(multiprocessing.cpu_count())
    # articles = article_reader.collect_articles_pool()

    # for article in articles:
    #     print(article)
    from rx.core import blockingobservable

    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        blockingobservable.BlockingObservable(rx.Observable.interval(1000)\
            .flat_map(lambda s: executor.submit(sleep, s))\
            .subscribe(output))


if __name__ == '__main__':
    main()
    input()