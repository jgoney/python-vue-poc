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

    def common_json_response_time(self, url):
        """JSON responses should include response time field"""
        resp = self.app.get(url)
        self.assertTrue(resp.is_json)

        data = resp.get_json()

        self.assertIsNotNone(data["response_time"])


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

    # Common cases
    def test_response_time(self):
        """factorials: response_time is valid"""
        super().common_json_response_time("/api/factorial?n=5")

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

        result = 27269884455406270157991615313642198705000779992917725821180502894974726476373026809482509284562310031170172380127627214493597616743856443016039972205847405917634660750474914561879656763268658528092195715626073248224067794253809132219056382939163918400

        self.assertEqual(result, data["fibonacci"])

    # Common cases
    def test_response_time(self):
        """fibonacci: response_time is valid"""
        super().common_json_response_time("/api/fibonacci?n=5")

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
