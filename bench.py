import os, time, httplib2, urllib3, threading, Queue

urls = [
    'http://code.google.com/apis/apps/',
    'http://code.google.com/apis/base/',
    'http://code.google.com/apis/blogger/',
    'http://code.google.com/apis/calendar/',
    'http://code.google.com/apis/codesearch/',
    'http://code.google.com/apis/contact/',
    'http://code.google.com/apis/books/',
    'http://code.google.com/apis/documents/',
    'http://code.google.com/apis/finance/',
    'http://code.google.com/apis/health/',
    'http://code.google.com/apis/notebook/',
    'http://code.google.com/apis/picasaweb/',
    'http://code.google.com/apis/spreadsheets/',
    'http://code.google.com/apis/webmastertools/',
    'http://code.google.com/apis/youtube/',
]

def bench_simple_sequential(name, callback):
    begin = time.time()

    for url in urls:
        callback(url)

    end = time.time()

    print "%-8s took %0.3f seconds" % (name, (end - begin))

def bench_urllib3_with_threads():
    begin = time.time()

    pool = urllib3.connection_from_url(urls[0], maxsize=4)

    urls_queue = Queue.Queue()
    for url in urls:
        urls_queue.put(url)

    def download():
        while True:
            try:
                url = urls_queue.get_nowait()
            except Queue.Empty:
                return
            pool.get_url(url)
            urls_queue.task_done()

    for i in range(4):
        threading.Thread(target=download).start()

    urls_queue.join()

    end = time.time()

    print "took %0.3f seconds" % (end - begin)

if __name__ == '__main__':
    os.system("rm -rf cache-tmp")

    pool = urllib3.connection_from_url(urls[0])
    http = httplib2.Http('httplib2-cache.tmp')

    print "simple sequential download, first run:"
    print
    bench_simple_sequential('urllib3', pool.get_url)
    bench_simple_sequential('httplib2', http.request)

    print
    print "simple sequential download, second run:"
    print
    bench_simple_sequential('urllib3', pool.get_url)
    bench_simple_sequential('httplib2', http.request)

    print
    print "now, urllib3 with 4 threads and 4 connections:"
    print
    bench_urllib3_with_threads()

    os.system("rm -rf httplib2-cache.tmp")
