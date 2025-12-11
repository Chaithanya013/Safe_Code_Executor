# Safe Code Executor

A learning project where users submit code via an API, and it is executed safely inside Docker containers.

- Supports **Python** (main requirement) and **Node.js (JavaScript)** as a bonus.
- Uses Docker to isolate execution and enforce:
  - CPU time limit (via timeout)
  - Memory limit
  - No network access
  - Read-only root filesystem
- Includes a **VS Code–style web UI** and detailed documentation.

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Features](#2-features)
- [3. Project Structure](#3-project-structure)
- [4. Prerequisites](#4-prerequisites)
- [5. Setup & Installation](#5-setup--installation)
  - [5.1. Clone the project](#51-clone-the-project)
  - [5.2. Create and activate virtual environment](#52-create-and-activate-virtual-environment)
  - [5.3. Install dependencies](#53-install-dependencies)
  - [5.4. Pull Docker images](#54-pull-docker-images)
- [6. Running the Project](#6-running-the-project)
  - [6.1. Terminal 1: Run the Flask server](#61-terminal-1-run-the-flask-server)
  - [6.2. Terminal 2: Run tests and send API requests](#62-terminal-2-run-tests-and-send-api-requests)
- [7. API Usage (Python & Node.js)](#7-api-usage-python--nodejs)
  - [7.1. Basic Python example](#71-basic-python-example)
  - [7.2. Basic Node.js example (bonus)](#72-basic-nodejs-example-bonus)
  - [7.3. Error and validation examples](#73-error-and-validation-examples)
- [8. Web UI](#8-web-ui)
- [9. Security Features](#9-security-features)
  - [9.1. Timeout](#91-timeout)
  - [9.2. Memory Limits](#92-memory-limits)
  - [9.3. Network Blocking](#93-network-blocking)
  - [9.4. Read-only Filesystem](#94-read-only-filesystem)
  - [9.5. Code Length Limit](#95-code-length-limit)
- [10. Docker Security Experiments](#10-docker-security-experiments)
- [11. Full Test Command Suite](#11-full-test-command-suite)
- [12. Internal Design](#12-internal-design)
- [13. Extending the Project](#13-extending-the-project)
- [14. Troubleshooting & Common Issues](#14-troubleshooting--common-issues)
- [15. Git & Deliverables Checklist](#15-git--deliverables-checklist)
- [16. What I Learned](#16-what-i-learned)
- [17. Future Work & Conclusion](#17-future-work--conclusion)
- [18. Author Details](#18-author-details)

---

## 1. Overview

This project is a **Safe Code Executor**:

- Users send code to an API.
- The server runs that code inside a **sandboxed Docker container**.
- The server returns either the **output** or a **clear error**.
- You learn:
  - How to connect Flask + Docker.
  - How to enforce time, memory, network, and filesystem limits.
  - How to build a tiny but useful web UI.

---

## 2. Features

- **API**: `POST /run` to execute code.
- **Languages**:
  - `python` via `python:3.11-slim`
  - `node` (Node.js / JavaScript) via `node:20-slim` (bonus)
- **Docker Sandbox**:
  - `--memory=128m` → memory limit
  - `--network none` → no network access
  - `--read-only` → read-only root filesystem
  - `--rm` → container automatically removed
- **Timeout**:
  - Requests are killed after **10 seconds** with a clear error message.
- **Input Validation**:
  - Maximum code length: **5000 characters**.
- **Web UI**:
  - VS Code–style UI with editor, run button, clear button, and terminal output.
- **Documentation & Tests**:
  - Detailed README
  - Test script: `run_tests.sh`

---

## 3. Project Structure

```text
Safe_Code_Executor/
├── app.py                 # Flask app (API + UI route + Docker integration)
├── requirements.txt       # Python dependencies (Flask)
├── templates/
│   └── index.html         # Web UI (VS Code-style)
├── run_tests.sh           # Convenience script for running tests
├── README.md              # Documentation
└── .gitignore             # Ignore venv, __pycache__, etc.
```

# 4. Prerequisites

To run and test the **Safe Code Executor** project successfully, ensure your system meets the following requirements.

---

## 4.1. Software Requirements

These tools must be installed on your machine:

### Python 3.8 or higher

Check your version:

```
python3 --version
```

### Virtual Environment Support (Debian/Ubuntu/WSL)

If `python3 -m venv` gives an error, install:

```
sudo apt update
sudo apt install python3-venv -y
```

### Docker (with WSL integration if on Windows)

Verify Docker is installed and accessible:

```
docker --version
```

### Optional: jq (for pretty JSON output)

Recommended for nicer outputs when testing APIs:

```
sudo apt install jq -y
```

---

## 4.2. System Requirements

### Operating System Compatibility

This project works on:

* Windows (with **Docker Desktop** + **WSL2**)
* Ubuntu/Linux
* macOS (Docker Desktop recommended)

### Internet Connection (first time only)

Required only to pull Docker images:

```
docker pull python:3.11-slim
docker pull node:20-slim
```

After pulling once, local execution does not need internet.

---

## 4.3. Recommended Setup

Best experience comes from using **two terminals**:

### Terminal 1 → Run Flask server

Used to host API and monitor logs.

### Terminal 2 → Run tests and send API requests

Used to execute curl commands and test security rules.

---

## 4.4. Optional Tools for Development

### VS Code or PyCharm

Useful for editing Flask code.

### Git

If you're managing the project in a repository:

```
git --version
```

### Browser (Chrome/Firefox)

Required to use the web UI located at:

```
http://localhost:5000/
```

---

This completes all prerequisites needed before installing and running the project.


# 5. Setup & Installation

This section explains exactly how to set up the **Safe Code Executor** project on your machine. It includes installation steps, environment configuration, Docker setup, and screenshot placeholders (formatted for GitHub). All instructions are written so even a beginner can follow without errors.

---

# 5.1. Clone the Project

### Command:

```
git clone <your-repo-url> Safe_Code_Executor
cd Safe_Code_Executor
```

### Explanation:

* `git clone` downloads the repository.
* `cd Safe_Code_Executor` moves into the project directory where all code lives.

---

# 5.2. Create and Activate Virtual Environment

### Command (Linux/macOS/WSL):

```
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell):

```
python -m venv venv
venv\Scripts\Activate.ps1
```

### Explanation:

* `python3 -m venv` creates an independent Python environment.
* `source venv/bin/activate` activates it so dependencies install locally.


![Activate Virtual Environment](https://raw.githubusercontent.com/Chaithanya013/Safe_Code_Executor/f9ee7a76fea9c12d3203b44f3e82f031452ed30a/screenshots/Activate%20Virtual%20Environment.png)



---

# 5.3. Install Dependencies

### Command:

```
pip install -r requirements.txt
```

### Explanation:

* Installs Flask and any required packages inside the virtual environment.


---

# 5.4. Pull Docker Images

### Command:

```
docker pull python:3.11-slim
```

(Optional, for Node.js bonus support)

```
docker pull node:20-slim
```

### Explanation:

* Downloads the Python and Node.js Docker images locally.
* Ensures the first execution is instant, without pulling during runtime.


---

# 5.5. Verify Docker Installation

### Command:

```
docker --version
```

### Explanation:

* Confirms Docker is installed and available inside your terminal.

---

# 5.6. (WSL USERS) Enable Docker Integration

### Requirements:

* Docker Desktop (Windows)
* WSL2 installed
* Integration turned ON for your Ubuntu distro

### Steps:

1. Open Docker Desktop → *Settings*
2. Go to **Resources → WSL Integration**
3. Enable *Ubuntu* or your distribution

---

# 5.7. Start the Flask Server (Terminal 1)

### Command:

```
source venv/bin/activate
python3 app.py
```

### Explanation:

* Starts the Flask development server.
* Keeps running while you execute tests from another terminal.
* Runs at: `http://127.0.0.1:5000/`

![Flask Server Running](https://github.com/Chaithanya013/Safe_Code_Executor/blob/9c3a5e0b0c1a2eadf6babed3b3e23f47d88c3811/screenshots/Flask%20Server%20Running.png)


---

# 5.8. Open a Second Terminal for Testing (Terminal 2)

### Command:

```
cd Safe_Code_Executor
source venv/bin/activate
```

### Explanation:

* You now have two terminals:

  * **Terminal 1** → Running Flask server
  * **Terminal 2** → Sending requests & running tests
* This setup is required for observing live logs in Terminal 1.



![Two Terminal Setup](https://github.com/Chaithanya013/Safe_Code_Executor/blob/1c1ab1c8b205f5f7f2f3702b86849d30dd880f9c/screenshots/Two%20Terminal%20Setup1.png)


---

# 5.9. Access the Web UI

### Open in browser:

```
http://localhost:5000/
```

### Explanation:

* Loads the VSCode-style web UI.
* You can type code, run it, clear editor, and view terminal output.

![Web UI Homepage](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/web%20ui%20homepage.png)


---

# 6. Running the Project

This section explains how to correctly run the Safe Code Executor using the recommended **two-terminal setup**. This is required for testing, debugging, and verifying Docker sandbox behaviors in real-time.

Each subsection includes:

* Commands
* Explanations
* Screenshot placeholders (GitHub-friendly)

---

# 6.1. Terminal 1 — Run the Flask Server

Terminal 1 will run the Flask server continuously. Keep it open at all times.

### **Command:**

```
cd Safe_Code_Executor
source venv/bin/activate
python3 app.py
```

### **Explanation:**

* `source venv/bin/activate` → activates your virtual environment.
* `python3 app.py` → starts the Flask server at:

  * **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**
* This terminal displays:

  * API logs
  * Runtime errors
  * Request activity
* You **do not type curl commands here**.

### **Expected Output:**

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

![Flask Running](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Flask%20Running.png)


---

# 6.2. Why Two Terminals?

Using two terminals is **essential**:

| Terminal       | Purpose                                                |
| -------------- | ------------------------------------------------------ |
| **Terminal 1** | Run Flask server, watch logs in real time              |
| **Terminal 2** | Run tests (curl commands), trigger security conditions |

This separation mirrors real-world backend testing workflows.


---

# 6.3. Terminal 2 — Send Requests, Run Tests

Open a **new terminal**, not the one running Flask.

### **Command:**

```
cd Safe_Code_Executor
source venv/bin/activate
```

### **Explanation:**

* You activate the environment again (each terminal needs activation).
* From this terminal you will run:

  * API test commands
  * Security verification commands
  * The `run_tests.sh` script


---

# 6.4. Run Example Test Command (Verify Server is Working)

In **Terminal 2**, run:

### Command:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello from Terminal 2\")"}'
```

### Expected Output:

```json
{"output":"Hello from Terminal 2"}
```

### Explanation:

* Confirms Flask API is reachable.
* Confirms Docker executed your Python code.
* Confirms JSON response formatting.


---

# 6.5. Run the Full Test Suite

You can test everything (timeouts, memory limits, network blocking, errors) using:

### Command:

```
chmod +x run_tests.sh
./run_tests.sh
```

### Explanation:

* `chmod +x` makes the script executable.
* `./run_tests.sh` runs all API tests sequentially.
* Terminal 1 will show logs for each request.

---

# 6.6. Open the Browser UI

While the server is running (Terminal 1), open:

```
http://localhost:5000/
```

### Explanation:

* Loads the file **templates/index.html**.
* You can:

  * Type Python code
  * Run code via API
  * See terminal-style output
  * Hit Clear Editor or Clear Terminal buttons

![UI Running](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/UI%20Run%20Code%20Example.png)


---

# 6.7. Confirm UI Interacts with API

In the UI editor, type:

```python
print("Hello from Web UI")
```

Then click **Run Code**.

### Expected Output:

```
Hello from Web UI
```

### Explanation:

* Confirms the frontend → backend → Docker pipeline works.


![UI Output Example](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/UI%20Run%20Code%20Example.png)


---

# 6.8. Stop the Server

Press **CTRL + C** in **Terminal 1** to stop Flask.

### Explanation:

* Safe shutdown of the development server.
* Docker containers automatically clean up because of `--rm`.

---

# 7. API Usage (Python & Node.js)

This section explains how to interact with the `/run` API endpoint to execute **Python** and **Node.js (JavaScript)** code safely inside Docker containers.

It includes:

* Basic examples
* Language selection
* Validation behavior
* Error responses
* Screenshot placeholders


---

# 7.1. API Endpoint Summary

### **Endpoint:**

```
POST /run
```

### **Headers:**

```
Content-Type: application/json
```

### **Basic Request Body:**

```json
{
  "code": "print(2 + 2)"
}
```

### **Optional Parameter — Language:**

```json
{
  "language": "python",   // or "node"
  "code": "console.log(10)"
}
```

### **Explanation:**

* If `language` is omitted → defaults to **Python**.
* The `code` field must be **non-empty** and **<= 5000 characters**.
* Returns JSON with either `output` or `error`.

---

# 7.2. Basic Python Example

### **Command:**

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"print(\"Hello from Python\")"}'
```

### **Expected Output:**

```json
{"output": "Hello from Python"}
```

### **Explanation:**

* This sends Python code to the API.
* Docker uses the `python:3.11-slim` image.
* Output is captured from stdout and returned as JSON.

![Python API Example](https://github.com/Chaithanya013/Safe_Code_Executor/blob/88bc1b4d4d70e0ac01367f14c07969b45add3ccb/screenshots/python%20test%20(bonus).png))


---

# 7.3. Basic Node.js Example (Bonus Feature)

### **Command:**

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"language":"node","code":"console.log(\"Hello from Node.js\")"}'
```

### **Expected Output:**

```json
{"output": "Execution Timed out After 10 seconds"}
```

### **Explanation:**

* This uses the **Node.js sandbox** running inside `node:20-slim`.
* Executes JavaScript safely inside Docker.
* Same timeout, memory limit, and network restrictions apply.

![Node API Example](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/nodejs%20(bonus).png)


---

# 7.4. Multi-Line Python Code Example

### **Command:**

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "for i in range(5):\n    print(i)"}'
```

### **Expected Output:**

```json
{"output":"0\n1\n2\n3\n4"}
```

### **Explanation:**

* Multi-line code must use `\n` inside JSON.
* The output preserves line breaks.


![Multi-line Python Output](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Multi-line%20Python%20Output.png)


---

# 7.5. Error Example — Invalid Code

### **Command:**

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "print(x)"}'
```

### **Expected Output:**

```json
{
  "error": "Code execution failed.",
  "details": "NameError: name 'x' is not defined"
}
```

### **Explanation:**

* Errors from Python or Node.js are captured and returned in `details`.
* The API does **not crash** even for invalid user code.


![API Error Example](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/API%20Error%20Example.png)


---

# 7.6. Error Example — Code Too Long (> 5000 chars)

### **Command:**

```
body=$(python3 - <<'PY'
import json
print(json.dumps({"code": "print('a'*6000)"}))
PY
)

curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d "$body"
```

### **Expected Output:**

```json
{"error": "Code too long. Maximum allowed length is 5000 characters."}
```

### **Explanation:**

* This prevents memory abuse and oversized payloads.
* The check happens **before** Docker is called.

![Code Too Long Error](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Code%20Too%20Long%20Error.png)


---

# 7.7. Error Example — Infinite Loop (Timeout)

### **Command:**

```
time curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "while True:\n    pass"}'
```

### **Expected Output:**

```json
{"error": "Execution timed out after 10 seconds"}
```

### **Explanation:**

* The API enforces a **10-second timeout**.
* The Docker container is safely terminated.


![Timeout Error](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Timeout%20Error1.png)

---

# 7.8. Error Example — Network Blocked

### **Command:**

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "import urllib.request\nurllib.request.urlopen(\"http://example.com\")"}'
```

### **Expected Output:**

```json
{
  "error": "Code execution failed.",
  "details": "...Temporary failure in name resolution..."
}
```

### **Explanation:**

* Docker runs with `--network none`.
* All network access is blocked.


![Network Block Error](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Network%20Block%20Error.png)


---

# 8. Web UI (VS Code–Style Interface)

The Safe Code Executor includes a built‑in **web interface** designed to look and feel like a lightweight version of **Visual Studio Code**. This UI allows you to type, run, and clear code easily without needing to use cURL commands.

---

![Web UI Overview](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Web%20UI%20Overview.png)


*This screenshot should show the entire UI: sidebar, editor, run button, terminal output.*

---

# 8.1. Accessing the Web UI

Once the Flask server is running in **Terminal 1**, open your browser and visit:

```
http://localhost:5000/
```

### Explanation:

* Flask renders the page from `templates/index.html`.
* The page provides a comfortable coding environment.
* No additional setup is required.

---

# 8.2. UI Layout

The UI contains four major components:

### ** 1. Sidebar**

A slim vertical bar similar to VS Code’s side navigation.

### ** 2. Code Editor **

* Monospace font
* Line numbers
* Syntax-friendly styling
* Large editable area


### ** 3. Buttons Panel **

* **Run Code** → sends the code to `/run`
* **Clear Editor** → clears code input
* **Clear Terminal** → clears previous output

### ** 4. Terminal‑Style Output Panel **

* Black background
* Green/white text for output
* Red text for errors

---

# 8.3. Running Code from the UI

### Steps:

1. Type your Python or Node.js code into the editor.
2. Click **Run Code**, or press:

   * **Ctrl + Enter** (Windows/Linux)
   * **Cmd + Enter** (macOS)
3. Output appears instantly in the terminal panel.

### Example:

Inside the editor, type:

```python
print("Hello from Web UI")
```

Click **Run Code**.

### Expected Output:

```
Hello from Web UI
```

![UI Run Code Example](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/UI%20Run%20Code%20Example.png)


---

# 8.4. Error Output in the UI

The UI displays errors clearly in the terminal panel.

### Example Error Code:

```python
print(x)
```

### Expected UI Output:

```
Code execution failed.
NameError: name 'x' is not defined
```

### Explanation:

* Frontend shows error in red text.
* Backend returns structured JSON.

---

# 8.5. Clearing Editor & Terminal

### Buttons:

* **Clear Editor** → removes all text from the code editor.
* **Clear Terminal** → resets output panel.

### When to Use:

* Testing multiple code snippets.
* Separating outputs for cleaner debugging.

---

# 8.6. How the UI Communicates With the API

The UI sends a POST request:

```
POST /run
Content-Type: application/json
```

With payload:

```json
{
  "language": "python",
  "code": "print('Hello')"
}
```

### Explanation:

* JavaScript inside `index.html` captures the editor content.
* Sends it via `fetch()` to the Flask backend.
* Backend runs code inside Docker and returns JSON.
* UI parses JSON and shows output.


---

# 8.7. Using Node.js From the UI 

Choose Node.js by adding:

```json
{
  "language": "node"
}
```

### Example:

```javascript
console.log("Running JavaScript from the UI!")
```

### Expected Output:

```
Running JavaScript from the UI!
```

---

# 8.8. UI Limitations (By Design)

* No file-saving or multi‑tab support (simple prototype UI).
* Errors are shown plainly; no syntax highlighting.
* Code is not executed in real time—only on button press.
* Large outputs may scroll; terminal auto-scroll enabled.

### Future Enhancements:

* Replace textarea with **Monaco Editor** (actual VS Code engine).
* Add themes, layout resizing, and code history panel.

---

# 9. Security Features

The Safe Code Executor is designed to safely run untrusted code using Docker-based sandboxing. This section explains every security mechanism implemented in the project, how it works, how to test it, and includes screenshot placeholders for GitHub documentation.

Each security layer protects against common attacks such as infinite loops, memory abuse, network access, filesystem modification, and oversized input payloads.

---

# 9.1. Execution Timeout (Prevents Infinite Loops)

The backend uses:

```python
subprocess.run(..., timeout=10)
```

This ensures any code running longer than **10 seconds** is automatically terminated.

### Protection Against:

* `while True:` infinite loops
* Very slow programs
* Long-running computations

### Test (Terminal 2):

```
time curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "while True:\n    pass"}'
```

### Expected Output:

```json
{"error": "Execution timed out after 10 seconds"}
```

### Explanation:

* Backend kills the process after 10 seconds.
* Docker container is also terminated safely.


![Timeout Protection](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Timeout%20Protection.png)

---

# 9.2. Memory Limit (Prevents Memory Attacks)

Docker container is run with:

```bash
--memory=128m
```

This restricts program memory usage to **128 MB**.

### Protection Against:

* Large object allocation attacks (e.g. `"a" * 1_000_000_000`)
* Memory overflow
* System crashes due to excessive RAM usage

### Test (Terminal 2):

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "x = \"a\" * 1000000000\nprint(len(x))"}'
```

### Expected Output:

```json
{"error": "Code execution failed.", "details": ""}
```

![Memory Limit Protection](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Memory%20Limit%20Protection.png)

---

# 9.3. Network Blocking (No External Requests)

Docker is run with:

```bash
--network none
```

This disables internet access from inside the container.

### Protection Against:

* Data exfiltration attempts
* HTTP/DNS attacks
* Malware downloading
* Remote command & control traffic

### Test:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "import urllib.request\nurllib.request.urlopen(\"http://example.com\")"}'
```

### Expected Output:

```json
{
  "error": "Code execution failed.",
  "details": "...Temporary failure in name resolution..."
}
```

![Network Block Protection](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Network%20Block%20Error.png)


---

# 9.4. Read-Only Filesystem (Prevents Writes)

Docker container uses:

```bash
--read-only
```

This makes the entire root filesystem unmodifiable.

### Protection Against:

* Writing malicious files
* Dropping payloads
* Modifying system configs
* Persistent attacks

### Special Note:

We mount the temporary script directory with:

```
-v <temp_path>:/app
```

so that the script file itself can be executed.

### Test (Write Attempt):

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "with open(\"/tmp/hack.txt\",\"w\") as f:\n f.write(\"Hacked!\")"}'
```

### Expected Output:

```json
{
  "error": "Code execution failed.",
  "details": "OSError: [Errno 30] Read-only file system: '/tmp/hack.txt'"
}
```

![Read Only Filesystem Protection](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Write%20Tmp%20After%20Readonly.png)

---

# 9.5. Code Length Limit (Prevents Massive Payloads)

Backend checks length before executing code:

```python
if len(code) > 5000:
    return jsonify({"error": "Code too long. Maximum allowed length is 5000 characters."}), 400
```

### Protection Against:

* Excessively large submissions
* Payload-based denial-of-service attacks
* Code editors freezing from huge input

### Test:

```
b=$(python3 - <<'PY'
import json; print(json.dumps({"code": "print('a'*6000)"}))
PY
)

curl -s -X POST http://localhost:5000/run -H "Content-Type: application/json" -d "$b"
```

### Expected Output:

```json
{"error": "Code too long. Maximum allowed length is 5000 characters."}
```


![Code Length Limit](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Code%20Too%20Long%20Error.png)

---

# 9.6. Container Auto-Removal (Prevents Resource Waste)

Docker flag:

```bash
--rm
```

Ensures used containers are automatically deleted after execution.

### Benefits:

* No orphan containers
* No manual cleanup required
* Sandboxes do not accumulate over time


---

# 9.7. Language Isolation (Python & Node.js)

Each language runs in its own container:

* Python → `python:3.11-slim`
* Node.js → `node:20-slim`

### Protection Against:

* Cross-language conflicts
* Mixed dependencies
* Script execution pollution

---

# 9.8. No Access to Host Machine

Because code runs **inside Docker**, it cannot:

* Access your host filesystem
* Modify local files
* Escape to host OS (without kernel vulnerability)

### Example Test:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "with open(\"/etc/passwd\") as f:\n print(f.read())"}'
```

### Explanation:

* The file displayed is **container's /etc/passwd**, not the host's.
* Isolation confirmed.

![Host Isolation](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Reading%20etc-passwd.png)


---

# 10. Docker Security Experiments

This section demonstrates important security experiments that help you understand what Docker **can** and **cannot** protect your system from. These experiments were part of the assignment and serve as hands-on learning to evaluate container isolation.

Each test shows:

* What happens
* Why it happens
* What it means for security
* Screenshot placeholders for documentation

---

# 10.1. Experiment 1 — Reading `/etc/passwd`

### Test Command (Terminal 2):

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code": "with open(\"/etc/passwd\") as f:\n print(f.read())"}'
```

### Expected Behavior:

* It **successfully reads** `/etc/passwd`.
* But the file is **from the Docker container**, not the host machine.

### Explanation:

* Docker containers contain their own minimal filesystem.
* `/etc/passwd` inside the container lists container users, not system users.
* This confirms **filesystem isolation** works correctly.



![Experiment Reading etc-passwd](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Reading%20etc-passwd.png)


---

# 10.2. Experiment 2 — Writing to `/tmp` (Before Read-Only Mode)

### Test Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code": "with open(\"/tmp/test.txt\", \"w\") as f:\n f.write(\"hacked!\")\nprint(open(\"/tmp/test.txt\").read())"}'
```

### Expected Behavior:

* This **works successfully**, printing:

  ```
  hacked!
  ```
* Because by default Docker allows the container to write inside its own filesystem.

### Explanation:

* Containers have a writable layer unless explicitly made read-only.
* This is safe for the host machine, because the write happens **inside the container**, not on your system.


![Experiment Write Tmp Before Readonly](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Write%20Tmp%20Before%20Readonly.png)


---

# 10.3. Experiment 3 — Writing to `/tmp` After Enabling Read-Only Filesystem

When using this Docker flag:

```
--read-only
```

Docker prevents all write attempts to the filesystem **except** mounted volumes.

### Test Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code": "with open(\"/tmp/test.txt\", \"w\") as f:\n f.write(\"blocked!\")"}'
```

### Expected Behavior:

An error such as:

```json
{
 "error": "Code execution failed.",
 "details": "OSError: [Errno 30] Read-only file system: '/tmp/test.txt'"
}
```

### Explanation:

* The root filesystem is read-only.
* Attempting to write anywhere (other than mounted volumes) fails.
* Demonstrates stronger filesystem isolation.


![Experiment Write Tmp After Readonly](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Write%20Tmp%20After%20Readonly.png)


---

# 10.4. Experiment 4 — Attempting Network Access

Since containers run with:

```
--network none
```

nobody inside the container can use the internet.

### Test Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code": "import urllib.request\nurllib.request.urlopen(\"http://example.com\")"}'
```

### Expected Behavior:

An error similar to:

```
Temporary failure in name resolution
```

### Explanation:

* No DNS resolution.
* No internet.
* Prevents malicious code from contacting external servers.

### Screenshot Placeholder:

```markdown
![Experiment Network Block](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Network%20Block%20Error.png)
```

---

# 10.5. Experiment 5 — Attempting to Escape the Container

### Test Idea:

Try Python code that attempts to traverse directories:

```
import os
print(os.listdir("/"))
```

### Expected Behavior:

* Only **container-level directories** are shown.
* No access to host filesystem.

### Example Output:

```
['bin', 'usr', 'lib', 'etc', 'app', ...]
```

### Explanation:

* Docker isolates the process in its own filesystem and process namespace.
* Direct escape is not possible without a Docker or kernel vulnerability.


---

# 10.6.Experiment 6 — Running a Malicious Fork Bomb (Simulated)

 **IMPORTANT:** You MUST NOT execute a real fork bomb.

Example malicious code (DO NOT RUN):

```
:(){ :|:& };:
```

### Expected Result in Sandbox:

* Docker would reject it because:

  * Shell is not available
  * Process limits + timeout kill runaway programs

### Explanation:

* The sandbox protects host OS from harmful shell-level operations.
* Containers run isolated processes with strict resource limits.


---

# 10.7. Summary of Findings

| Experiment                       | Result               | Meaning                            |
| -------------------------------- | -------------------- | ---------------------------------- |
| Read `/etc/passwd`               | Shows container file | Container filesystem is isolated   |
| Write to `/tmp` before read-only | Works                | Containers are writable by default |
| Write after read-only            | Fails                | Write protection enabled           |
| Network access                   | Fails                | Outbound connections blocked       |
| Directory traversal              | Limited to container | Strong filesystem isolation        |
| Shell attacks                    | Ineffective          | No shell + resource limits         |

---

# 10.8. What These Experiments Teach Us

### Docker **does** provide:

* Filesystem isolation
* Network isolation
* Process isolation
* Resource (CPU/memory) control
* Read-only root filesystem support

### Docker **does NOT** provide full security:

* Root inside the container can still be dangerous
* Vulnerable Docker daemon → host compromise
* Misconfigured mounts → host exposure
* Kernel vulnerabilities → possible escape

### Therefore:

Docker is a **great sandbox for learning and basic protection**, but **not enough for production-grade secure code execution** without additional layers like:

* Seccomp
* AppArmor
* User namespaces
* Non-root execution
* Firejail / gVisor / Kata Containers

---

# 11. Full Test Suite

This section includes **all test commands** required to verify correct functionality, security, and stability of the Safe Code Executor. These tests should be run from **Terminal 2**, while **Terminal 1** is running the Flask server.

Every test has:

* The command
* What it checks
* Expected behavior
* Screenshot placeholders for documentation

---

## Screenshot Placeholder (Test Suite Overview)

---

# 11.1. Test 1 — Simple Python Print

### Command:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"print(\"Hello\")"}'
```

### Verifies:

* API is running
* Docker container launches
* Output is returned correctly

### Expected Output:

```json
{"output":"Hello"}
```

![Test 1 Output](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Test%201%20Output.png)


---

# 11.2. Test 2 — Multi-Line Python Code

### Command:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"x = 5 + 3\nprint(x)"}'
```

### Verifies:

* Multi-line handling works
* Whitespace and indentation preserved

### Expected Output:

```json
{"output":"8"}
```

![Test 2 Output](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Test%202%20Output.png)


---

# 11.3. Test 3 — For Loop Output

### Command:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"for i in range(5):\n print(i)"}'
```

### Verifies:

* Iterative output works
* Newlines preserved

### Expected Output:

```json
{"output":"0\n1\n2\n3\n4"}
```

![For Loop Output](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/For%20Loop%20Output.png)


---

# 11.4. Test 4 — Read `/etc/passwd`

### Command:

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"with open(\"/etc/passwd\") as f:\n print(f.read())"}'
```

### Verifies:

* Container filesystem isolation
* Host filesystem NOT exposed

### Expected Behavior:

* You see *container's* `/etc/passwd`, not the host's.

![Read etc Passwd](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Reading%20etc-passwd.png)

---

# 11.5. Test 5 — Write Before Read-Only Mode

> Only works if you temporarily remove `--read-only` from Docker flags.

### Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code":"with open(\"/tmp/test.txt\",\"w\") as f:\n f.write(\"hacked!\")\nprint(open(\"/tmp/test.txt\").read())"}'
```

### Verifies:

* Containers normally allow writing inside their own FS

### Expected Output:

```
hacked!
```

![Write Before Readonly](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Write%20Tmp%20Before%20Readonly.png)

---

# 11.6. Test 6 — Write After Read-Only Mode

Requires `--read-only` in Docker command.

### Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code":"with open(\"/tmp/hack.txt\",\"w\") as f:\n f.write(\"blocked!\")"}'
```

### Verifies:

* Read-only filesystem protection

### Expected Output:

```json
{
  "error": "Code execution failed.",
  "details": "OSError: [Errno 30] Read-only file system: '/tmp/hack.txt'"
}
```

![Write After Readonly](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Experiment%20Write%20Tmp%20After%20Readonly.png)

---

# 11.7. Test 7 — Infinite Loop Timeout

### Command:

```
time curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code":"while True:\n pass"}'
```

### Verifies:

* Timeout is correctly enforced (10s)
* Container killed safely

### Expected Output:

```json
{"error":"Execution timed out after 10 seconds"}
```

![Timeout Test](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Timeout%20Error1.png)


---

# 11.8. Test 8 — Memory Bomb

### Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code":"x = \"a\" * 1000000000\nprint(len(x))"}'
```

### Verifies:

* `--memory=128m` limit works
* Docker terminates memory-heavy processes

### Expected Behavior:

* Failure (details may be empty):

```json
{"error": "Code execution failed.", "details": ""}
```

![Memory Test](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Memory%20Limit%20Protection.png)

---

# 11.9. Test 9 — Network Block

### Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code":"import urllib.request\nurllib.request.urlopen(\"http://example.com\")"}'
```

### Verifies:

* `--network none` works
* Internet is disabled

### Expected Output:

Error with DNS failure:

```
Temporary failure in name resolution
```

---

# 11.10. Test 10 — Code Too Long (> 5000 chars)

### Command:

```
b=$(python3 - <<'PY'
import json; print(json.dumps({"code": "print('a'*6000)"}))
PY
)

curl -s -X POST http://localhost:5000/run -H "Content-Type: application/json" -d "$b"
```

### Verifies:

* Input size restriction works
* Oversized payload is rejected early

### Expected Output:

```json
{"error":"Code too long. Maximum allowed length is 5000 characters."}
```

![Code Length Test](https://github.com/Chaithanya013/Safe_Code_Executor/blob/882e774a37663232e0cf87694c8c0e1619b11c88/screenshots/Code%20Too%20Long%20Error.png)


---

# 11.11. Test 11 — Basic Node.js Execution (Bonus)

### Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"language":"node","code":"console.log(100+200)"}'
```

### Verifies:

* Node.js execution works
* Node container responds correctly

### Expected Output:

```json
{"output":"300"}
```

---

# 11.12. Test 12 — Complex Mixed Output

### Command:

```
curl -s -X POST http://localhost:5000/run \
 -H "Content-Type: application/json" \
 -d '{"code":"for i in range(3):\n print(\"Value:\", i)"}'
```

### Expected Output:

```
Value: 0
Value: 1
Value: 2
```
---

# 12. Internal Design

This section explains the **architecture**, **design decisions**, and **internal workflow** of the Safe Code Executor system. It describes how Python/Node.js code is processed, validated, executed inside Docker, and how output/error responses are generated.

---

# 12.1. High-Level Overview

The system consists of three major components:

### 1. Frontend Web UI (index.html)

* VS Code–style editor interface
* Sends code to `/run` endpoint using `fetch()`
* Displays output and errors in terminal panel

### 2. Flask Backend (app.py)

* Validates input
* Chooses Docker image (Python or Node.js)
* Creates temporary script file
* Runs Docker container with strict security flags
* Captures stdout/stderr
* Returns JSON response

### 3. Docker Sandbox

* Executes untrusted user code safely
* Provides filesystem, memory, CPU, and network isolation


---

# 12.2. Backend Request Flow 

This is the exact lifecycle of every request:

## Step 1 — User submits code

Either through API or Web UI.

Example payload:

```json
{
  "language": "python",
  "code": "print(10 + 20)"
}
```

## Step 2 — Input validation

The backend checks:

* Code exists
* Code length ≤ 5000
* Language is supported
* Dangerous payload sizes are blocked early

## Step 3 — Temporary script creation

Backend writes the code into a temp directory:

```
/tmp/sc-exec-xyz123/script.py
/tmp/sc-exec-xyz123/script.js
```

This directory is mounted into the Docker container.

## Step 4 — Docker command assembly

Depending on language:

```bash
python: python3 script.py
node:   node script.js
```

Flags are added:

* `--rm` → auto-remove container
* `--network none` → block internet
* `--read-only` → block writes
* `--memory=128m` → RAM limit
* `--pids-limit=64` → prevent fork bombs

## Step 5 — Execute Docker container

```
subprocess.run([...], timeout=10)
```

## Step 6 — Capture output and errors

* `stdout` → success output
* `stderr` → Python/Node error details
* `timeout` → forced termination

## Step 7 — JSON response returned to UI or client

Example:

```json
{
  "output": "30"
}
```

Or error:

```json
{
 "error": "Execution timed out after 10 seconds"
}
```

---

# 12.3. Docker Sandbox Architecture

Inside the container:

* Only essential tools exist (minimal base image)
* No internet
* Filesystem is read-only
* Code executes as non-root user (optional enhancement)
* Only mounted `/app` directory is writable (script file)

### Container Structure Example:

```
/app/script.py
/bin
/usr
/lib
/etc/passwd
```
---

# 12.4. Security Flags Breakdown

| Flag                | Purpose                     |
| ------------------- | --------------------------- |
| `--rm`              | Auto-clean containers       |
| `--memory=128m`     | Prevent memory exhaustion   |
| `--network none`    | Block internet access       |
| `--read-only`       | Prevent filesystem writes   |
| `-v host_path:/app` | Only mount script directory |
| `--pids-limit=64`   | Prevent fork bombs          |


---

# 12.5. Error Handling Design

Different errors are handled differently:

### 1. Timeout Errors

```
"Execution timed out after 10 seconds"
```

### 2. Python/Node Runtime Errors

Captured in stderr:

```
NameError: x is not defined
```

### 3. Docker Failure Errors

Example:

```
Cannot connect to Docker daemon
```

### 4. Input Validation Errors

```
"Code too long. Maximum allowed length is 5000 characters."
```
---

# 12.6. Language Support Design (Python + Node.js)

The backend selects the correct runtime image based on:

```python
if language == "node":
    image = "node:20-slim"
else:
    image = "python:3.11-slim"
```

This modular design allows adding new languages easily:

* Ruby
* Go
* Java
* PHP

By adding a simple mapping table.


---

# 12.7. Why Docker Instead of Local Execution?

### Advantages:

* Full filesystem isolation
* Memory limits
* Network blocking
* Process restriction
* Prevents host compromise
* Reproducible environments

### Local execution would be dangerous:

* Code could delete files
* Steal data
* Install malware

Docker provides a safe execution sandbox.

---

# 12.8. Internal Folder Naming Strategy

Temp folders are created using:

```
tempfile.mkdtemp(prefix="sc-exec-")
```

This prevents collisions and limits attacker knowledge of paths.

Example folder:

```
/tmp/sc-exec-x29dh83a/
```

### Why this matters:

* Attackers cannot guess filenames
* Reduces race condition attacks
* Ensures secure cleanup

---

# 12.9. Cleanup Strategy

After each run:

* Docker container is auto-removed (`--rm`)
* Temporary folder is deleted using `shutil.rmtree`

This ensures:

* No leftover code
* No disk clutter
* Perfect cleanup after every execution

---

# 13. Extending the Project

This section explains how to expand the Safe Code Executor with new languages, UI improvements, and advanced sandboxing features. These extensions demonstrate forward-thinking design and show how the system can evolve beyond the basic assignment requirements.

Each subsection includes:

* What the extension is
* Why it’s useful
* How to implement it
* Screenshot placeholders

---

# 13.1. Adding More Programming Languages

The system currently supports:

* Python (default)
* Node.js (bonus feature)

Adding new languages only requires:

1. A new Docker image
2. A command mapping
3. Language validation

---

### Example: Add Ruby Support

#### Step 1 — Pull the Docker image:

```
docker pull ruby:3.2-slim
```

#### Step 2 — Extend language mapping in `app.py`:

```python
LANGUAGE_CONFIG = {
    "python": {
        "image": "python:3.11-slim",
        "run_cmd": "python3"
    },
    "node": {
        "image": "node:20-slim",
        "run_cmd": "node"
    },
    "ruby": {
        "image": "ruby:3.2-slim",
        "run_cmd": "ruby"
    }
}
```

#### Step 3 — Send Ruby code from UI or cURL:

```json
{
  "language": "ruby",
  "code": "puts 5 + 5"
}
```
---

# 13.2. Upgrading the Web UI with the Monaco Editor

The current UI uses a basic `<textarea>`.
A major enhancement is replacing it with **Monaco Editor**, the same editor engine used inside VS Code.

### Benefits:

* Syntax highlighting
* Autocomplete suggestions
* Multiple themes
* Line gutter and minimap
* Better user experience

### Basic Integration Outline:

In `index.html`, include Monaco via CDN:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/loader.min.js"></script>
```

Then initialize the editor inside the layout:

```javascript
require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.getElementById("editor"), {
        value: "print('Hello')",
        language: "python",
        theme: "vs-dark",
        automaticLayout: true
    });
});
```

---

# 13.3. Adding Execution History

You can store the last N executions and display them in a sidebar.

### Why this is useful:

* Helps students review previous outputs
* Makes debugging easier
* Enables learning through iteration

### Simple Backend Addition:

```python
history.append({
    "timestamp": time.time(),
    "code": code,
    "output": output_or_error
})
```

---

# 13.4. Running Code in a Non-Root User Inside Docker

Currently containers may run as root (default Docker behavior).
For stronger isolation:

### Add this to Docker command:

```bash
--user nobody
```

### Benefits:

* Reduces damage if sandbox escapes
* Follows security best practices

### Potential Issues:

* Some languages may require write access to cache folders
* Can be fixed by mounting a writable folder

---

# 13.5. Add CPU Usage Limits

To prevent busy loops from consuming 100% CPU.

### Extend Docker flags:

```bash
--cpus="0.5"
```

This restricts the container to half a CPU.


---

# 13.6. Add Log Storage and Admin Dashboard

A future enhancement for instructors or administrators.

### Features:

* Store error logs
* View resource usage by each execution
* Add analytics dashboard (Flask + Chart.js)

---

# 13.7. Container Pooling (Advanced Optimization)

Starting a new Docker container for every request is slow.

### Possible enhancement:

* Maintain a pool of pre-warmed containers
* Communicate via sockets or APIs

### Challenges:

* Ensuring security between re-used containers
* Resetting state between executions

---

# 13.8. Adding Support for File Inputs & Multiple Files

Future versions could allow users to upload small files used by their code.

### Safe way to do this:

* Store files in a temp directory
* Mount directory read-only into container
* Provide file paths to user code

---

# 13.9. Adding Docker Alternatives (Isolation Layers)

For stronger sandboxing, consider:

* **gVisor** (Google's userspace kernel)
* **Kata Containers** (lightweight virtual machines)
* **Firejail** (namespace sandbox)
* **Sysbox** (enhanced containers)

### Why:

* Protects even if Docker daemon is compromised
* Adds kernel-level isolation

---

# 14. Troubleshooting Guide

This section helps you diagnose and fix common issues encountered while setting up, running, or extending the Safe Code Executor project. Each issue includes symptoms, causes, and step-by-step fixes. Screenshot placeholders are included for GitHub documentation.

---

# 14.1. Problem: `python3 -m venv` Fails (ensurepip missing)

### Symptom:

```
The virtual environment was not created successfully because ensurepip is not available...
```

### Cause:

Your system is missing the `python3-venv` package.

### Fix:

```
sudo apt update
sudo apt install python3-venv -y
```

---

# 14.2. Problem: Docker command fails with “Permission denied”

### Symptom:

```
Got permission denied while trying to connect to Docker daemon
```

### Cause:

Your user is not in the Docker group.

### Fix (Linux/WSL):

```
sudo usermod -aG docker $USER
newgrp docker
```

### Fix (Windows):

* Make sure **Docker Desktop** is running.
* Ensure WSL integration is enabled.

---

# 14.3. Problem: Flask server doesn’t restart after code changes

### Cause:

Debug mode is disabled.

### Fix:

Add:

```python
app.run(debug=True)
```

### Or set environment variable:

```
export FLASK_ENV=development
```

---

# 14.4. Problem: Output shows nothing (empty output)

### Possible Causes:

* Code prints nothing
* stderr contained error but UI didn't format it
* Docker terminated container due to memory or timeout

### Fix:

* Check Terminal 1 (server logs)
* Add debug prints to `app.py`
* Ensure UI terminal panel scrolls properly

---

# 14.5. Problem: Infinite loop does NOT timeout

### Cause:

`timeout=10` missing in `subprocess.run`.

### Fix:

Ensure:

```python
result = subprocess.run(cmd, ..., timeout=10, ...)
```

---

# 14.6. Problem: Memory bomb doesn’t fail as expected

### Possible Causes:

* Missing Docker flag:

```bash
--memory=128m
```

* Code did not allocate enough memory

---

# 14.7. Problem: Network calls succeed (they shouldn't)

### Cause:

`--network none` missing.

### Fix:

Verify Docker command contains:

```bash
--network none
```

---

# 14.8. Problem: File writes still work after enabling `--read-only`

### Possible Causes:

* The write target is inside the mounted folder `/app`
* You forgot to include:

```bash
--read-only
```

### Fix:

1. Ensure `--read-only` exists.
2. Ensure no writable mounts except the script directory.


---

# 14.9. Problem: Node.js execution returns “command not found”

### Cause:

Node.js Docker image was not pulled.

### Fix:

```
docker pull node:20-slim
```

---

# 14.10. Problem: UI Buttons Not Working

### Causes:

* JavaScript not loaded
* Wrong element IDs
* Browser caching old version of `index.html`

### Fix:

Try:

* Hard refresh UI: **Ctrl + Shift + R**
* Open browser console (F12) for errors
* Ensure correct IDs:

```html
<button id="run-btn">Run Code</button>
```

---

# 14.11. Problem: Two terminals become out of sync

### Cause:

One terminal has deactivated venv or wrong directory.

### Fix:

In both terminals:

```
cd Safe_Code_Executor
source venv/bin/activate
```

---

# 14.12. Problem: Flask server crashes while executing Docker

### Possible Causes:

* Docker Desktop not running
* Corrupted Docker installation
* Incorrect Docker flags

### Fix:

* Restart Docker Desktop
* Run:

```
docker ps
```

* Verify Docker command in `app.py`

---


# 15. Git Deliverables

This section lists all the files, commits, branches, and Git hygiene practices required for submitting the Safe Code Executor project. It ensures your repository is clean, professional, and easy for reviewers to explore.


---

# 15.1. Required Files in the Repository

Your final GitHub repo **must include** the following files:

```
Safe_Code_Executor/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── run_tests.sh
├── .gitignore
└── docs/
    └── screenshots/ (optional but recommended)
```

### Description of key files:

* **app.py** → Flask API + Docker execution logic
* **README.md** → Full project documentation
* **index.html** → VS Code–style UI
* **run_tests.sh** → Automated test suite script
* **requirements.txt** → Python dependencies
* **.gitignore** → Ignore venv, logs, caches, etc.

---

# 15.2. Recommended `.gitignore`

Your `.gitignore` should include:

```
venv/
__pycache__/
*.pyc
*.log
.DS_Store
tmp/
docs/screenshots/*.png
```

### Explanation:

* Prevents accidental commits of virtual environments
* Keeps repo clean and lightweight

---

# 15.3. Commit Naming Standards

Use **clean, descriptive commit messages** such as:

```
feat: add Docker sandbox execution for Python
feat(ui): implement VS Code-style web UI
fix: enforce 10 second timeout and handle errors
docs: add sections 1–10 to README
refactor: clean up subprocess command builder
```

### Avoid messages like:

```
update code
final commit
asdfgqwe
```

---

# 15.4. Branch Recommendations

Although optional for small projects, recommended branching strategy:

```
main         → production-ready code
feature/ui   → web interface changes
feature/node → node.js execution support
feature/docs → README and documentation
```

### Benefits:

* Cleaner pull requests
* Easy rollback
* Organized development


---

# 15.5. Ready-to-Commit Patch

Below is an example patch (diff) for final submission:

```diff
+ - feat: finalize Safe Code Executor project
+ - Added Flask backend with Docker sandbox
+ - Implemented Python & Node.js support
+ - Added VS Code-style UI
+ - Added security features: timeout, memory limit, no network, read-only FS
+ - Wrote README with 17 sections
+ - Added troubleshooting and extension sections
```

---

# 15.6. Tagging Your Final Release

Create a Git tag for your final version:

```
git tag -a v1.0 -m "Safe Code Executor - Final Submission"
git push origin v1.0
```

### Why?

* Reviewers can easily find the final version.
* GitHub shows a named release version.


---

# 15.7. Optional: Create a GitHub Release Page

For a polished project:

1. Go to **GitHub → Releases → New Release**
2. Choose tag: `v1.0`
3. Title: *Safe Code Executor — Final Release*
4. Attach screenshots (optional)
5. Publish release

---


# 16. What I Learned

This final section reflects on the knowledge and skills gained throughout the Safe Code Executor project. It demonstrates understanding of security concepts, Docker isolation, backend design, and full-stack integration. This reflection is an important part of the assignment and shows the depth of learning.

Each subsection includes a clear explanation, real examples from the project, and connections to industry best practices.

---

# 16.1. Running Untrusted Code Safely Is Hard

Before the project, running user-submitted code sounded simple:

```python
eval(user_code)
```

But this is extremely dangerous.

### Key Learning:

To safely execute untrusted code, you need:

* Process isolation
* Filesystem isolation
* Network restrictions
* Memory limits
* Timeouts
* Sandboxing environments (Docker)

This project taught me that **security is not a feature — it is a system.**

---

# 16.2. Docker Is a Powerful Security Boundary

I learned how Docker isolates code from the host system:

* Independent filesystem (`/etc/passwd` inside container is different)
* No access to host OS
* Can disable network completely
* Can restrict memory usage
* Can enforce CPU limits

### Example:

Running this code inside Docker:

```python
with open('/etc/passwd') as f:
    print(f.read())
```

**does not expose the host system**, only the container’s internal files.

This taught me how containers provide a safe execution environment.

---

# 16.3. Timeouts and Memory Limits Matter

Without a timeout, a simple infinite loop would freeze the system:

```python
while True:
    pass
```

Without a memory limit, even one line of code could crash the server:

```python
x = "a" * 1_000_000_000
```

### Learning:

Sandboxing untrusted code requires **strict control of resources**.
Docker makes this easy using:

* `--memory=128m`
* `--pids-limit=64`
* Python’s `timeout` parameter

---

# 16.4. Network Access Must Be Blocked

Allowing user code to access the internet is a massive security risk.
I learned this by testing:

```python
urllib.request.urlopen("http://example.com")
```

The Docker flag:

```
--network none
```

blocked all requests.

### Learning:

This prevents:

* Data exfiltration
* Attacks to external servers
* Malware downloads

Network isolation is essential in any code execution service.

---

# 16.5. Read-Only Filesystems Enhance Safety

I learned that even inside Docker, users can still write files unless:

```
--read-only
```

enforces a read-only root filesystem.

### Why this matters:

* Prevent attackers from modifying container internals
* Prevent malicious persistence
* Prevent dropping scripts or payloads

---

# 16.6. Building a Full Stack System Is Rewarding

This project helped me integrate:

* HTML/CSS/JavaScript frontend
* Flask backend logic
* Docker sandbox execution
* Error handling and validation

The VS Code–style UI taught me:

* DOM manipulation
* Fetch API
* Terminal-style output rendering
* UX considerations for developer tools

---

# 16.7. Documentation Is Just as Important as Code

I learned how to write:

* Clear, structured README files
* Troubleshooting guides
* Architecture documentation
* API usage examples
* Security explanations

Good documentation makes the project easy to understand for anyone who opens the repository.

---

# 16.8. How to Think Like an Attacker

Security requires anticipating malicious behavior:

* What if someone tries an infinite loop?
* What if someone tries to fill up memory?
* What if someone tries to access the network?
* What if someone writes files?
* What if someone tries to escape the container?

This project trained me to think adversarially, which is a key skill in cybersecurity.

---

# 16.9. Clean Git Practices Matter

Keeping a clean history taught me how to:

* Write meaningful commit messages
* Organize code logically
* Maintain a clear project structure
* Use tags for final releases

This is invaluable for teamwork and professional development.

---

# 16.10. Confidence in Deploying Secure Code Execution Systems

By the end of this project, I now understand how online coding platforms like:

* LeetCode
* HackerRank
* Replit
* CodeRunner

build their secure sandboxes.

I now have the foundational knowledge to:

* Build safer execution environments
* Use Docker security features correctly
* Protect servers from untrusted code
* Debug containerized systems

---

# 17. Future Work & Conclusion

This final section highlights potential future enhancements and provides a strong concluding summary for the Safe Code Executor project. It demonstrates understanding of the system's limitations, opportunities for growth, and key takeaways. This section adds a polished, professional finish to the full documentation.

---

# 17.1. Future Improvements

Even though the Safe Code Executor is already functional and secure for academic use, there are many ways to evolve it into a production-grade sandbox. Below are enhancements worth exploring.

---

## 17.1.1. Add Support for More Languages

Languages that could be added:

* Java (OpenJDK)
* Go
* Rust
* C/C++ (with gcc/clang)
* PHP
* Bash shell (with strict sandboxing)

### Benefit:

Expands the executor into a full polyglot coding platform.

---

## 17.1.2. Replace Textarea with Monaco Editor (Real VS Code Engine)

This would provide:

* Syntax highlighting
* Language intelligence
* Auto-indentation
* Themes (Dark/Light)
* Minimap + line gutter

This upgrade would make the UI feel like an actual IDE.

---

## 17.1.3. Persistent User Sessions

Allow users to:

* Save previous code snippets
* Load history across sessions
* Store settings such as theme or language preference

This would require:

* A lightweight backend database (SQLite/PostgreSQL)
* User authentication (optional)

---

## 17.1.4. Execution Metrics Dashboard

Track:

* Runtime duration
* Memory usage
* CPU usage
* Frequency of errors

This is useful for educators and system administrators.

---

## 17.1.5. Stronger Security Layers

For production deployments, add:

### AppArmor Profiles

### Seccomp Filters

### User Namespaces

### gVisor or Kata Containers

These drastically reduce the damage possible from container escapes.

---

## 17.1.6. Container Pooling (Performance Optimization)

Instead of launching a new container per request:

* Maintain a pool of warm containers
* Use them for faster execution

### Challenge:

Ensuring containers have **no leftover state** between executions.

---

## 17.1.7. WebSocket-Based Live Output

Currently, output is returned only at the end of execution.

A real-time terminal can be implemented using:

* WebSockets
* Streaming stdout from Docker

This would allow live logs, similar to Replit or Google Colab.

---

## 17.1.8. Code File Support

Allow users to upload:

* Input files
* Test case files
* Dependencies (for Node/Python with limitations)

### Security Consideration:

Files must be:

* Scanned
* Stored in isolated temp directories
* Mounted read-only

---

# 17.2. Limitations of the Current System

Although secure for educational purposes, the current sandbox has limits:

###  Relies on Docker daemon security

###  No protection against kernel vulnerabilities

###  No networking inside container — not suitable for network-based exercises

###  No persistent storage

###  Limited language support

###  No concurrent sessions handling

Recognizing these limitations is essential for future development.

---

# 17.3. Final Conclusion

The Safe Code Executor project provided practical experience in:

* Backend API development
* Running untrusted code securely
* Docker containerization and isolation
* Building a developer-friendly UI
* Implementing resource limits and timeouts
* Designing a secure software system end-to-end
* Writing extensive documentation

###  Core Achievements:

* Successfully built a working Python & Node.js sandbox
* Ensured safety via Docker isolation
* Added UI similar to a lightweight online IDE
* Implemented detailed logging, validation, and error handling
* Produced professional documentation spanning all features

###  Overall Learning Impact:

This project builds foundational skills needed to:

* Develop code execution services
* Work on cloud-based IDEs
* Build secure backend systems
* Understand container security principles
* Think like a security engineer

The system is not only functional, but also a strong demonstration of modern engineering practices including documentation, testing, UI/UX, and platform security.

---

# 18. Author Details

- **Name:** V. Siva Chaithanya
- **Project:** Safe Code Executor (Secure Python + Node.js Sandbox)
- **GitHub:** https://github.com/Chaithanya013
- **Docker Hub:** https://hub.docker.com/u/chaithanya013
- **Email:** *chaithanyav.0203@gmail.com*



