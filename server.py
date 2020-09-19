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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
