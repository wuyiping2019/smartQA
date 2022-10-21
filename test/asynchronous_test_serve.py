#!/usr/bin/env python3

import asyncio
import time
import urllib.parse
from datetime import timedelta

from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

import tornado.httpclient
from tornado import gen, httpclient, queues

base_url = "http://www.tornadoweb.org/en/stable/"
concurrency = 10


async def get_links_from_url(url):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    response = await httpclient.AsyncHTTPClient().fetch(url)
    print("fetched %s" % url)

    html = response.body.decode(errors="ignore")
    return [urljoin(url, remove_fragment(new_url)) for new_url in get_links(html)]


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get("href")
            if href and tag == "a":
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


async def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched, dead = set(), set(), set()

    async def fetch_url(current_url):
        if current_url in fetching:
            return

        print("fetching %s" % current_url)
        fetching.add(current_url)
        urls = await get_links_from_url(current_url)
        fetched.add(current_url)

        for new_url in urls:
            # Only follow links beneath the base URL
            if new_url.startswith(base_url):
                await q.put(new_url)

    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await fetch_url(url)
            except Exception as e:
                print("Exception: %s %s" % (e, url))
                dead.add(url)
            finally:
                q.task_done()

    await q.put(base_url)

    # Start workers, then wait for the work queue to be empty.
    workers = gen.multi([worker() for _ in range(concurrency)])
    await q.join(timeout=timedelta(seconds=300))
    assert fetching == (fetched | dead)
    print("Done in %d seconds, fetched %s URLs." % (time.time() - start, len(fetched)))
    print("Unable to fetch %s URLS." % len(dead))

    # Signal all the workers to exit.
    for _ in range(concurrency):
        await q.put(None)
    await workers


@tornado.web.asynchronous
def done_m(self):
    client = tornado.httpclient.AsyncHTTPClient()

    input_data = {}
    input_data['query'] = '姚明的职业是什么'
    input_data['attribute'] = '职业'
    input_data['answer'] = '篮球运动员'

    data_send = urllib.parse.urlencode(input_data)

    url = 'http://10.2.13.150:8081/kg/sim'
    responses = client.fetch(url, method='POST', body=data_send, callback=self.test_resp)

def test_resp(self, resp):
    print('%s' % repr(resp.body))
    self.finish()


if __name__ == "__main__":
    # asyncio.run(main())

    done_m(self)

