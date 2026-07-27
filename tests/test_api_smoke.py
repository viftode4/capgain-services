import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from examples.api_smoke import check


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(204)
        self.send_header("content-type", "application/json")
        self.end_headers()

    def log_message(self, *_args):
        pass


class ApiSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_expected_status_passes(self):
        result = check(f"http://127.0.0.1:{self.server.server_port}", 204)
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], 204)
        self.assertEqual(result["content_type"], "application/json")

    def test_unexpected_status_fails(self):
        result = check(f"http://127.0.0.1:{self.server.server_port}", 200)
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], 204)


if __name__ == "__main__":
    unittest.main()

