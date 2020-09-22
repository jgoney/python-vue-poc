import os
import math
import time

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
    g,
    render_template,
    send_from_directory,
)

import settings


templates = os.path.abspath("dist")
print(templates)
app = Flask(__name__, template_folder=templates, static_url_path=templates)
app.config.from_object(settings)


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "{:.5f}s".format(time.time() - g.request_start_time)


@app.after_request
def after_request(resp):
    if resp.is_json:
        j = resp.get_json()
        j["responseTime"] = g.request_time()
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
        # return value as string, since JavaScript can mangle these values as numbers
        return jsonify(
            {
                "value": str(fn),
                "processingTime": "{:.5f}s".format(processing_end - processing_start),
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
            "calculated Ackermann function for m={}, n={} in {:.5f}s".format(
                m,
                n,
                processing_end - processing_start,
            )
        )

        # return value as string, since JavaScript can mangle these values as numbers
        return jsonify(
            {
                "value": str(ack),
                "processingTime": "{:.5f}s".format(processing_end - processing_start),
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

    # return value as string, since JavaScript can mangle these values as numbers
    return jsonify(
        {
            "value": str(f),
            "processingTime": "{:.5f}s".format(processing_end - processing_start),
        }
    )


# Serve index.html template and static files
# You MUST run `npm run build` first to ensure that the dist/
# directory exists.
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/<path:path>", methods=["GET"])
def send_favicons(path):
    return send_from_directory(app.static_url_path, path)


@app.route("/js/<path:path>", methods=["GET"])
def send_js(path):
    js_path = os.path.join(app.static_url_path, "js")
    return send_from_directory(js_path, path)


@app.route("/css/<path:path>", methods=["GET"])
def send_css(path):
    css_path = os.path.join(app.static_url_path, "css")
    return send_from_directory(css_path, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.PORT)
