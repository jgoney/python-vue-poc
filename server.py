import math
import time

from flask import Flask, jsonify, make_response, request, g

import settings


app = Flask(__name__)
app.config.from_object(settings)


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "{:.5f}s".format(time.time() - g.request_start_time)


@app.after_request
def after_request(resp):
    if resp.is_json:
        j = resp.get_json()
        j["response_time"] = g.request_time()
        return make_response(jsonify(j), resp.status_code)

    return resp


@app.route("/api/fibonacci", methods=["GET"])
def get_fibonacci():
    """
    For a valid positive integer 'n', returns the nth value in the Fibonacci series
    """

    n = request.args.get("n")
    try:
        n = int(n)
    except (TypeError, ValueError):
        return make_response(
            jsonify({"error": "bad request: query parameter n missing or invalid"}), 400
        )

    if n < 0:
        return make_response(
            jsonify({"error": "bad request: query parameter n cannot be negative"}), 400
        )

    try:
        processing_start = time.time()

        # Iterative version
        fn_2 = 0
        fn_1 = 1

        if n == 0 or n == 1:
            fn = n
        else:
            for _ in range(1, n):
                fn = fn_2 + fn_1
                fn_2 = fn_1
                fn_1 = fn

        processing_end = time.time()

        app.logger.info(
            "calculated nth Fibonacci number for n={} in {:.5f}s".format(
                n,
                processing_end - processing_start,
            )
        )
        return jsonify(
            {
                "fibonacci": fn,
                "processing_time": "{:.5f}s".format(processing_end - processing_start),
            }
        )

    except OverflowError:
        return make_response(
            jsonify({"error": "bad request: n={} is too big".format(n)}), 400
        )


@app.route("/api/ackermann", methods=["GET"])
def get_ackermann():
    m = request.args.get("m")
    n = request.args.get("n")

    try:
        m = int(m)
        n = int(n)

        if m < 0 or n < 0:
            return make_response(
                jsonify(
                    {
                        "error": "bad request: neither query parameter m nor n can be negative"
                    }
                ),
                400,
            )

        def ackermann(m, n):
            if m == 0:
                return n + 1
            elif m > 0 and n == 0:
                return ackermann(m - 1, 1)
            else:
                return ackermann(m - 1, ackermann(m, n - 1))

        processing_start = time.time()
        ack = ackermann(m, n)
        processing_end = time.time()

        app.logger.info(
            "calculated ackermann function for m={}, n={} in {:.5f}s".format(
                m,
                n,
                processing_end - processing_start,
            )
        )

        return jsonify(
            {
                "ackermann": ack,
                "processing_time": "{:.5f}s".format(processing_end - processing_start),
            }
        )

    except (TypeError, ValueError):
        return make_response(
            jsonify(
                {"error": "bad request: query parameter m and/or n missing or invalid"}
            ),
            400,
        )

    except RecursionError:
        return make_response(
            jsonify(
                {
                    "error": "bad request: maximum recursion depth exceeded calculating Ackermann function where m={} and n={}".format(
                        m, n
                    )
                }
            ),
            400,
        )


@app.route("/api/factorial", methods=["GET"])
def get_factorial():
    """
    Returns a factorial for a valid positive integer 'n'
    Slows down significantly for cases where n > 1000000
    """

    n = request.args.get("n")
    try:
        n = int(n)
    except (TypeError, ValueError):
        return make_response(
            jsonify({"error": "bad request: query parameter n missing or invalid"}), 400
        )

    try:
        processing_start = time.time()
        f = math.factorial(n)
        processing_end = time.time()

    except ValueError:
        return make_response(
            jsonify({"error": "bad request: query parameter n cannot be negative"}), 400
        )

    app.logger.info(
        "calculated factorial for n={} in {:.5f}s".format(
            n,
            processing_end - processing_start,
        )
    )

    return jsonify(
        {
            "factorial": f,
            "processing_time": "{:.5f}s".format(processing_end - processing_start),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
