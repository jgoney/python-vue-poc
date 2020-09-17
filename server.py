import math

from flask import Flask, jsonify, make_response, request

import settings


app = Flask(__name__)
app.config.from_object(settings)


@app.route("/api/factorial", methods=["GET"])
def get_factorial():

    n = request.args.get("n")
    try:
        n = int(n)
    except (TypeError, ValueError):
        return make_response(
            jsonify({"error": "bad request: query parameter n missing or invalid"}), 400
        )

    try:
        f = math.factorial(n)
    except ValueError:
        return make_response(
            jsonify({"error": "bad request: query parameter n cannot be negative"}), 400
        )

    return jsonify({"factorial": f})


@app.route("/api/fibonacci", methods=["GET"])
def get_fibonacci():

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

    if n == 0 or n == 1:
        return jsonify({"fibonacci": n})

    try:
        # Implementation of Binet's formula for finding the nth number in the Fibonacci sequence
        phi_pos = ((1 + 5 ** 0.5) / 2) ** n
        phi_neg = ((1 - 5 ** 0.5) / 2) ** n
        fib = (phi_pos - phi_neg) / (5 ** 0.5)
        fib = math.floor(fib)

        return jsonify({"fibonacci": fib})

    except OverflowError:
        return make_response(
            jsonify({"error": "bad request: n={} is too big".format(n)}), 400
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
