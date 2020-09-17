import unittest

import server
import settings


class ServerBaseTestCase(unittest.TestCase):
    def setUp(self):
        """Setup test client for each test"""
        server.app.config.from_object(settings)
        server.app.config["TESTING"] = True
        self.app = server.app.test_client()

    def errs_negative(self, url):
        """fibonacci/factorial should not support negatives"""
        resp = self.app.get(url)
        self.assertEqual(resp.status_code, 400)

        data = resp.get_json()

        self.assertEqual(
            "bad request: query parameter n cannot be negative", data["error"]
        )

    def errs_missing_invalid(self, url):
        """fibonacci/factorial needs valid n parameter"""
        resp = self.app.get(url)
        self.assertEqual(resp.status_code, 400)

        data = resp.get_json()

        self.assertEqual(
            "bad request: query parameter n missing or invalid", data["error"]
        )


class ServerFactorialTestCase(ServerBaseTestCase):
    def test_basic_series(self):
        """factorials: first 10 in series """
        series = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

        for i in range(len(series)):
            with self.subTest(i=i):
                resp = self.app.get("/api/factorial?n={}".format(i))
                self.assertEqual(resp.status_code, 200)

                data = resp.get_json()

                self.assertEqual(series[i], data["factorial"])

    # Common error cases
    def test_invalid_n(self):
        """factorials: n is invalid"""
        super().errs_missing_invalid("/api/factorial?n=foobar")

    def test_missing_n(self):
        """factorials: n is missing"""
        super().errs_missing_invalid("/api/factorial")

    def test_negative(self):
        """factorials: negatives"""
        super().errs_negative("/api/factorial?n=-1")


class ServerFibonacciTestCase(ServerBaseTestCase):
    def test_basic_series(self):
        """fibonacci: first 20 in series """
        series = [
            0,
            1,
            1,
            2,
            3,
            5,
            8,
            13,
            21,
            34,
            55,
            89,
            144,
            233,
            377,
            610,
            987,
            1597,
            2584,
            4181,
        ]

        for i in range(len(series)):
            with self.subTest(i=i):
                resp = self.app.get("/api/fibonacci?n={}".format(i))
                self.assertEqual(resp.status_code, 200)

                data = resp.get_json()

                self.assertEqual(series[i], data["fibonacci"])

    def test_very_large(self):
        """fibonacci: very large numbers"""
        resp = self.app.get("/api/fibonacci?n={}".format(1200))
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()

        result = 27269884455407365847192026241192332547250796698164704715463580385597197075537548253492087865024098245321784944722311472705029391914337116136306691783618953277982977916818418369582710642008814191391090984759478348473276714347732043884108324642586886144
        self.assertEqual(result, data["fibonacci"])

    def test_too_large(self):
        """fibonacci: n too large"""
        resp = self.app.get("/api/fibonacci?n={}".format(1000000))
        self.assertEqual(resp.status_code, 400)

        data = resp.get_json()

        self.assertEqual("bad request: n=1000000 is too big", data["error"])

    # Common error cases
    def test_invalid_n(self):
        """fibonacci: n is invalid"""
        super().errs_missing_invalid("/api/fibonacci?n=foobar")

    def test_missing_n(self):
        """fibonacci: n is missing"""
        super().errs_missing_invalid("/api/fibonacci")

    def test_negative(self):
        """fibonacci: negatives"""
        super().errs_negative("/api/fibonacci?n=-1")


if __name__ == "__main__":
    unittest.main()
