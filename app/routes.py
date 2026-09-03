import asyncio

from flask import Blueprint, jsonify, request, current_app

from app.services import ask_ai


api = Blueprint("api", __name__)


@api.get("/health")
def health():
    """
    Health-check endpoint.
    """
    return jsonify({
        "status": "ok"
    })


@api.post("/ask")
async def ask():
    """
    Processes a single user input using Grok.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    user_input = data.get("userInput")

    if not isinstance(user_input, str) or not user_input.strip():
        return jsonify({
            "error": "userInput must be a non-empty string"
        }), 400

    try:
        response = await ask_ai(user_input.strip())

        return jsonify({
            "response": response
        }), 200

    except Exception:
        current_app.logger.exception("Error while processing /ask")

        return jsonify({
            "error": "Failed to process the request"
        }), 500


@api.post("/ask-batch")
async def ask_batch():
    """
    Processes multiple user inputs concurrently.

    The order of responses is preserved because asyncio.gather()
    returns results in the same order as the input coroutines.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    user_inputs = data.get("userInputs")

    if not isinstance(user_inputs, list) or not user_inputs:
        return jsonify({
            "error": "userInputs must be a non-empty list"
        }), 400

    if not all(
        isinstance(user_input, str) and user_input.strip()
        for user_input in user_inputs
    ):
        return jsonify({
            "error": "Every item in userInputs must be a non-empty string"
        }), 400

    try:
        responses = await asyncio.gather(
            *(ask_ai(user_input.strip()) for user_input in user_inputs)
        )

        return jsonify({
            "responses": responses
        }), 200

    except Exception:
        current_app.logger.exception("Error while processing /ask-batch")

        return jsonify({
            "error": "Failed to process batch requests"
        }), 500