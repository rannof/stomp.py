import unittest

import stomp

from stomp.test.testutils import *

class TestRabbitMQSend(unittest.TestCase):

    def setUp(self):
        pass

    def testbasic(self):
        conn = stomp.Connection11(get_rabbitmq_host())
        listener = TestListener('123')
        conn.set_listener('', listener)
        conn.start()
        conn.connect(get_rabbitmq_user(), get_rabbitmq_password(), wait=True)
        conn.subscribe(destination='/queue/test', id=1, ack='auto')

        conn.send(body='this is a test', destination='/queue/test', receipt='123')

        listener.wait_on_receipt()
        conn.disconnect(receipt=None)

        self.assert_(listener.connections == 1, 'should have received 1 connection acknowledgement')
        self.assert_(listener.messages == 1, 'should have received 1 message')
        self.assert_(listener.errors == 0, 'should not have received any errors')


