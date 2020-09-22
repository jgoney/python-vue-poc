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

        self.assertIsNotNone(data["responseTime"])


class ServerFibonacciTestCase(ServerBaseTestCase):
    def test_basic_series(self):
        """fibonacci: first 20 in series """
        series = [
            "0",
            "1",
            "1",
            "2",
            "3",
            "5",
            "8",
            "13",
            "21",
            "34",
            "55",
            "89",
            "144",
            "233",
            "377",
            "610",
            "987",
            "1597",
            "2584",
            "4181",
        ]

        for i in range(len(series)):
            with self.subTest(i=i):
                resp = self.app.get("/api/fibonacci?n={}".format(i))
                self.assertEqual(resp.status_code, 200)

                data = resp.get_json()

                self.assertEqual(series[i], data["value"])

    def test_processing_time(self):
        """fibonacci: processingTime is present on successful requests"""
        resp = self.app.get("/api/fibonacci?n={}".format(5))
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()

        self.assertIsNotNone(data["processingTime"])

    def test_very_large(self):
        """fibonacci: very large numbers"""
        resp = self.app.get("/api/fibonacci?n={}".format(1200))
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()

        result = "27269884455406270157991615313642198705000779992917725821180502894974726476373026809482509284562310031170172380127627214493597616743856443016039972205847405917634660750474914561879656763268658528092195715626073248224067794253809132219056382939163918400"

        self.assertEqual(result, data["value"])

    # Common cases
    def test_response_time(self):
        """fibonacci: responseTime is valid"""
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


class ServerAckermannTestCase(ServerBaseTestCase):
    def test_basic_series(self):
        """Ackermann function: values through A(3,4) """
        series = [
            ["1", "2", "3", "4", "5"],
            ["2", "3", "4", "5", "6"],
            ["3", "5", "7", "9", "11"],
            ["5", "13", "29", "61", "125"],
        ]

        i = 0
        for m in range(4):
            for n in range(5):
                i += 1
                with self.subTest(i=i):
                    resp = self.app.get("/api/ackermann?m={}&n={}".format(m, n))
                    self.assertEqual(resp.status_code, 200)
                    data = resp.get_json()
                    self.assertEqual(series[m][n], data["value"])

    def test_processing_time(self):
        """Ackermann function: processingTime is present on successful requests"""
        resp = self.app.get("/api/ackermann?m={}&n={}".format(1, 1))
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()

        self.assertIsNotNone(data["processingTime"])

    # Common cases
    def test_response_time(self):
        """Ackermann function: responseTime is valid"""
        super().common_json_response_time("/api/ackermann?m=0&n=0")

    # error cases
    def test_negative(self):
        """Ackermann function should not support negatives"""
        cases = [
            (-1, 0),  # m is negative
            (0, -1),  # n is negative
            (-1, -1),  # both are negative
        ]
        i = 0
        for case in cases:
            i += 1
            with self.subTest(i=i):
                resp = self.app.get("/api/ackermann?m={0}&n={1}".format(*case))
                self.assertEqual(resp.status_code, 400)

                data = resp.get_json()

                self.assertEqual(
                    "bad request: neither query parameter m nor n can be negative",
                    data["error"],
                )

    def test_missing(self):
        """Ackermann function needs valid m and n parameters"""
        resp = self.app.get("/api/ackermann")
        self.assertEqual(resp.status_code, 400)

        data = resp.get_json()

        self.assertEqual(
            "bad request: query parameter m and/or n missing or invalid", data["error"]
        )

    def test_overflow(self):
        """Ackermann function will stack overflow where m >= 5"""

        # N.B: this depends on how the interpreter's recursion stack is set
        # to ensure a reliable test, we'll set m to some absurdly high value, but it
        # will overflow much sooner than that
        resp = self.app.get("/api/ackermann?m=100&n=0")
        self.assertEqual(resp.status_code, 400)

        data = resp.get_json()

        self.assertEqual(
            "bad request: maximum recursion depth exceeded calculating Ackermann function where m=100 and n=0",
            data["error"],
        )


class ServerFactorialTestCase(ServerBaseTestCase):
    def test_basic_series(self):
        """factorials: first 10 in series """
        series = ["1", "1", "2", "6", "24", "120", "720", "5040", "40320", "362880"]

        for i in range(len(series)):
            with self.subTest(i=i):
                resp = self.app.get("/api/factorial?n={}".format(i))
                self.assertEqual(resp.status_code, 200)

                data = resp.get_json()

                self.assertEqual(series[i], data["value"])

    def test_processing_time(self):
        """factorials: processingTime is present on successful requests"""
        resp = self.app.get("/api/factorial?n={}".format(5))
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()

        self.assertIsNotNone(data["processingTime"])

    # Common cases
    def test_response_time(self):
        """factorials: responseTime is valid"""
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


if __name__ == "__main__":
    unittest.main()
