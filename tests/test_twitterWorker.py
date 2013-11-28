from abstract import TestCaseDB
from smm.lib.datastream.plugins.twitterworker import TwitterWorker
from smm.models import RawStreamQueue, SocketSession
import time
import threading

class TestTwitterWorker(TestCaseDB):

    def test_worker(self):
        """
        test single twitter worker
        """
        s = SocketSession(ip='x')
        s.keywords = ['google','bieber']
        s.save()
        kill = threading.Event()

        w = TwitterWorker(kill)
        w.setDaemon(True)
        w.start()

        # sleep is needed in order to get at least couple of tweets
        time.sleep(1)
        kill.set()
        self.assertGreater(RawStreamQueue.objects.count(), 0)

    def tearDown(self):
        RawStreamQueue.drop_collection()
        SocketSession.drop_collection()