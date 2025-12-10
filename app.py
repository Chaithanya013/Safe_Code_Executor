from flask import Flask, request, jsonify, render_template
import subprocess
import tempfile
from pathlib import Path
import time
import sys

app = Flask(__name__)

# Configuration
DEBUG = False
MAX_CODE_LENGTH = 5000
EXECUTION_TIMEOUT = 10  # seconds

# Language configuration
LANGUAGE_CONFIG = {
    "python": {
        "image": "python:3.11-slim",
        "filename": "script.py",
        "cmd": ["python", "script.py"],
    },
    "node": {
        "image": "node:20-slim",
        "filename": "script.js",
        "cmd": ["node", "script.js"],
    },
}

# In-memory history of recent executions
HISTORY = []
MAX_HISTORY = 20
NEXT_HISTORY_ID = 1


def add_history_entry(language, code, output, error, duration):
    """Store a history entry (newest later, we'll reverse for display)."""
    global NEXT_HISTORY_ID
    entry = {
        "id": NEXT_HISTORY_ID,
        "timestamp": time.time(),
        "language": language,
        "code": code,
        "output": output,
        "error": error,
        "duration": duration,
    }
    HISTORY.append(entry)
    NEXT_HISTORY_ID += 1

    # Keep only the last MAX_HISTORY entries
    if len(HISTORY) > MAX_HISTORY:
        HISTORY.pop(0)


@app.route("/")
def home():
    """Serve the main UI page."""
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_code():
    """
    Receive JSON { "code": "<code>", "language": "python" | "node" }
    Run it inside a Docker container and return output or error.
    """
    start_time = time.time()

    # Parse JSON
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON body."}), 400

    # Get language and code
    language = str(data.get("language", "python")).lower()
    code = data.get("code", "")

    # Validate language
    if language not in LANGUAGE_CONFIG:
        return jsonify({
            "error": f"Unsupported language '{language}'. Supported: {', '.join(LANGUAGE_CONFIG.keys())}."
        }), 400

    # Simple debug log
    if DEBUG:
        print(f"DEBUG: language={language}, code_len={len(code)}", file=sys.stderr)

    # Validate code
    if not isinstance(code, str) or code.strip() == "":
        return jsonify({"error": "Field 'code' must be a non-empty string."}), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify({
            "error": f"Code too long. Maximum allowed length is {MAX_CODE_LENGTH} characters."
        }), 400

    # Language config
    lang_cfg = LANGUAGE_CONFIG[language]
    image = lang_cfg["image"]
    filename = lang_cfg["filename"]
    run_cmd = lang_cfg["cmd"]

    # Prepare temp directory and script file
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            script_path = tmp_path / filename
            script_path.write_text(code, encoding="utf-8")

            # Build Docker command
            docker_cmd = [
                "docker", "run", "--rm",
                "--memory=128m",
                "--network", "none",
                "--read-only",
                "-v", f"{tmp_path}:/app",
                "-w", "/app",
                image,
            ] + run_cmd

            if DEBUG:
                print("DEBUG: docker_cmd =", docker_cmd, file=sys.stderr)

            try:
                result = subprocess.run(
                    docker_cmd,
                    capture_output=True,
                    text=True,
                    timeout=EXECUTION_TIMEOUT,
                )
            except subprocess.TimeoutExpired:
                duration = time.time() - start_time
                # Record history as timeout error
                add_history_entry(
                    language=language,
                    code=code,
                    output="",
                    error=f"Execution timed out after {EXECUTION_TIMEOUT} seconds",
                    duration=duration,
                )
                return jsonify({
                    "error": f"Execution timed out after {EXECUTION_TIMEOUT} seconds"
                }), 408
            except FileNotFoundError:
                return jsonify({
                    "error": "Docker is not installed or not in PATH."
                }), 500
            except Exception as e:
                return jsonify({
                    "error": "Internal server error while running Docker.",
                    "details": str(e),
                }), 500

            stdout = (result.stdout or "").rstrip("\n")
            stderr = (result.stderr or "").strip()
            duration = time.time() - start_time

            if DEBUG:
                print("DEBUG: returncode =", result.returncode, file=sys.stderr)
                if stderr:
                    print("DEBUG: stderr =", stderr, file=sys.stderr)

            # On error (non-zero exit code)
            if result.returncode != 0:
                add_history_entry(
                    language=language,
                    code=code,
                    output="",
                    error=stderr or "Code execution failed.",
                    duration=duration,
                )
                return jsonify({
                    "error": "Code execution failed.",
                    "details": stderr,
                }), 400

            # Success
            add_history_entry(
                language=language,
                code=code,
                output=stdout,
                error="",
                duration=duration,
            )
            return jsonify({"output": stdout}), 200

    except Exception as outer_exc:
        if DEBUG:
            print("DEBUG: unexpected exception in run_code:", outer_exc, file=sys.stderr)
        return jsonify({
            "error": "Internal server error.",
            "details": str(outer_exc)
        }), 500


@app.route("/history", methods=["GET"])
def get_history():
    """
    Return recent history entries (newest first).
    """
    # return reversed list so newest is first
    items = list(reversed(HISTORY))
    return jsonify({"history": items}), 200


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """
    Clear all history entries.
    """
    HISTORY.clear()
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Run dev server
    app.run(debug=True, host="127.0.0.1", port=5000)
