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
    For a valid non-negative integer 'n', returns the nth value in the Fibonacci series
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
    """
    For a valid non-negative integers 'm' and 'n', returns the result of the Ackermann function.

    This implementation uses memoization and direct computation optimizations inspired by
    https://medium.com/@a3zakir/computing-ackermann-function-in-ruby-1ec6fad22b2e. Still, the heavily
    recursive nature of the Ackermann function means that it will overflow the stack with relatively
    small arguments. The default recursion limit can be tweaked via sys.setrecursionlimit(), but this
    should be tuned on a case-by-case basis, as setting it too big can cause segfaults.
    """
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

        # dictionary cache to allow for memoization of ackermann(m, n)
        # in a real app, this could be cached in memcached, Redis, or the database, for example
        cache = {}

        def ackermann(m, n):

            if m in cache and n in cache[m]:
                return cache[m][n]

            if m == 0:
                result = n + 1
            elif m == 1:
                result = n + 2
            elif m == 2:
                result = 2 * n + 3
            elif m == 3:
                result = 2 ** (n + 3) - 3
            elif n == 0:
                result = ackermann(m - 1, 1)
            else:
                result = ackermann(m - 1, ackermann(m, n - 1))

            if m not in cache:
                cache[m] = {}

            cache[m][n] = result

            return result

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
# You MUST run `npm run build` first to ensure that the dist/ directory exists.
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Routes for serving favicons and js/css files.
# In a production environment, these would be served by the reverse proxy
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
