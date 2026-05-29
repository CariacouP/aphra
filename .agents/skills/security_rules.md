## 2026-03-11 - Path Traversal in Data Manager
**Vulnerability:** Arbitrary file write/overwrite path traversal vulnerability in `src/data_manager.py` due to concatenating user inputs (`ticker`, `source`, `interval`) into `.parquet` file paths without sanitization.
**Learning:** File paths were naively constructed directly from arguments (e.g. `f"{ticker}_{source.lower()}_{interval}.parquet"`) assuming valid inputs, allowing inputs like `../secret` to write to unexpected directories outside of `data/`.
**Prevention:** Always validate and sanitize user-provided variables that form any part of a filesystem path. Use a strict allowlist or strong regex replacement (e.g., `re.sub(r'[^a-zA-Z0-9_\-]', '_', str(name))`) before interpolating them into a filepath.

## 2025-02-15 - [Security Headers]
**Vulnerability:** The application was missing defense-in-depth HTTP security headers (e.g. `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`), leaving it vulnerable to clickjacking and MIME sniffing.
**Learning:** Security headers are often overlooked in purely functional Flask applications if not explicitly enforced by a middleware or infrastructure layer, leaving the app reliant on framework-level template escaping, which is prone to human error.
**Prevention:** Incorporate a generic `@app.after_request` decorator to automatically inject `Content-Security-Policy`, `Strict-Transport-Security`, and `X-Frame-Options` on every response to ensure baseline protection regardless of the route's specific logic.

## 2026-03-15 - Unsafe Eval in Content Security Policy
**Vulnerability:** The Content-Security-Policy header in the web application previously allowed `'unsafe-eval'`.
**Learning:** Permitting `'unsafe-eval'` enables the execution of JavaScript via functions like `eval()` and `setTimeout('...', delay)`. This significantly increases the risk of Cross-Site Scripting (XSS) attacks by allowing an attacker to inject string-based code execution if any DOM-based injection vector exists, overriding the protection typically provided by a strict CSP.
**Prevention:** Always strive for a strict Content-Security-Policy by removing directives like `'unsafe-eval'` and `'unsafe-inline'` unless absolutely mandated by a necessary framework, and refactor code to avoid string-based script execution in favor of pre-compiled or structurally safe JavaScript handlers.
## 2026-03-16 - Prevent Backtest Traceback Leakage
**Vulnerability:** The backtester's exception block (`webapp/backend.py`) caught all exceptions and saved the raw `traceback.format_exc()` directly to the `index.json` under `error_traceback`. This field was then exposed un-sanitized via the web frontend's Error Modal (Information Disclosure via Stack Traces).
**Learning:** Exception handling paths that map internal error states to database/json objects that the frontend renders can implicitly expose sensitive internal logic/paths to the user.
**Prevention:** Catch exceptions gracefully, securely log the full traceback to server-side logging mechanisms (e.g. `logger.error`), and only store safe, generic error descriptions (e.g. "An internal error occurred") in client-facing models.
## 2026-03-13 - [Secure Session Cookies]
**Vulnerability:** The application was not explicitly enforcing secure session cookies (`SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`), leaving session identifiers potentially vulnerable to interception over unencrypted connections or cross-site scripting (XSS) attacks.
**Learning:** Default Flask configurations do not enforce secure cookie policies, which can lead to session hijacking if a vulnerability like XSS is discovered elsewhere in the application, or if the user is targeted over a non-HTTPS connection.
**Prevention:** Always explicitly configure `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, and `SESSION_COOKIE_SAMESITE='Lax'` (or 'Strict') upon application initialization to provide defense-in-depth against session theft.
## 2024-05-24 - Input Validation Missing for Engine Configuration
**Vulnerability:** Missing input validation in `/live/update_config` route (`webapp/app.py`), allowing arbitrary data (e.g., unintended or malicious values for `environment` and `interval`) to be written to `config.yaml`.
**Learning:** Config writes directly relied on request inputs without enforcing a valid schema or whitelist, which can lead to application logic bugs or potential configuration manipulation issues.
**Prevention:** Implement strict whitelists and bounds checking on any input data before it's saved to the server configuration.

## 2026-03-17 - Configuration Injection via Unvalidated Web Input
**Vulnerability:** Arbitrary configuration injection (and potentially YAML manipulation) in `webapp/app.py`'s `update_engine_config` due to directly writing user inputs (`environment` and `interval`) into the application's `config.yaml` file.
**Learning:** Web endpoints that persist user inputs directly into application configuration files (like YAML, JSON) without strict whitelisting are prime vectors for logic abuse and configuration injection.
**Prevention:** Strictly validate any user input destined for a configuration file against an explicit allowlist of safe, expected values before allowing the file write operation.

## 2026-03-22 - Prevent XSS via unsafe-eval
**Vulnerability:** The `Content-Security-Policy` header in `webapp/app.py` mistakenly allowed `'unsafe-eval'`, a directive that permits the execution of string-to-code APIs like `eval()`, `setTimeout(string)`, and `new Function()`.
**Learning:** Including `'unsafe-eval'` completely breaks the defense-in-depth provided by a strict CSP, allowing attackers who find a minor injection vector to easily escalate it into full Remote Code Execution within the user's browser context.
**Prevention:** Avoid using `'unsafe-eval'` in the CSP. Use safe, modern APIs instead of `eval()`.

## 2026-03-24 - Arbitrary File Read in Webapp Results Endpoint
**Vulnerability:** Arbitrary file read via Path Traversal in `webapp/app.py`'s `/results/<id>` and `/grid_results/<id>` endpoints. The application reads `entry["file"]` from `index.json` and blindly appends it to `BACKTESTS_DIR` before reading its contents. An attacker who controls the json (e.g. by exploiting another bug to inject `"file": "../config.yaml"`) can force the backend to read arbitrary system files.
**Learning:** Even internal configuration or index files should be treated as untrusted data sources if they can be influenced by users, especially when they dictate which files are read from the filesystem.
**Prevention:** Always restrict paths to a safe directory. Use `Path(entry["file"]).name` to guarantee the path only references the base filename within the expected directory, stripping out any `../` path traversal elements.

## 2026-03-31 - Missing Defense-in-Depth HTTP Headers
**Vulnerability:** The web application was missing defense-in-depth HTTP security headers for `Referrer-Policy` and `Permissions-Policy`.
**Learning:** While `Content-Security-Policy` and `X-Frame-Options` provide strong protections, modern web applications should also restrict the information leaked via referrers and explicitly disable sensitive browser APIs (like geolocation and camera) if they are unused, reducing the overall attack surface.
**Prevention:** Always implement a comprehensive set of security headers in web frameworks, including `Referrer-Policy: strict-origin-when-cross-origin` and `Permissions-Policy` with a restrictive policy (e.g. `geolocation=(), microphone=(), camera=()`).
## 2026-03-28 - Missing CSRF Protection
**Vulnerability:** The Flask application lacked protection against Cross-Site Request Forgery (CSRF). Any form submission (POST request) could be triggered by an attacker crafting a malicious webpage and enticing an authenticated user to visit it, performing actions (like stopping the live engine or running a backtest) in the context of the user's session without their knowledge.
**Learning:** Default Flask applications do not include CSRF protection automatically for forms without utilizing an extension like `Flask-WTF`. Simple POST endpoints without specific API authentication mechanisms are vulnerable if they rely solely on session cookies.
**Prevention:** Always implement a synchronizer token pattern by storing a cryptographically secure random token in the user's session (`session['_csrf_token']`) and requiring the same token to be submitted as a hidden field (`<input type='hidden' name='csrf_token'>`) on every state-changing HTTP request (e.g., POST). Validate this matching pair in a global `@app.before_request` hook.

## 2026-04-27 - [Missing Security Headers Enhancement]
**Vulnerability:** The web application lacked modern, defense-in-depth security headers, specifically `Referrer-Policy`, `Permissions-Policy`, and strict directives (`object-src 'none'`, `base-uri 'none'`) in its `Content-Security-Policy`. This omission could allow cross-site leakage of sensitive URLs and the unauthorized use of browser features if an exploit payload successfully executes.
**Learning:** Security headers are not "set and forget". Even if basic headers (X-Frame-Options, X-Content-Type-Options) are present, modern browser security mechanisms like Permissions-Policy and Referrer-Policy must be explicitly configured to restrict unauthorized feature access and prevent referer leakage, forming an essential layer of the defense-in-depth posture.
**Prevention:** Always define a comprehensive suite of security headers when setting up a web application, routinely review them against modern best practices, and restrict CSP directives (such as `object-src` and `base-uri`) to `none` unless strictly required.

## 2026-05-10 - Hardcoded Fallback Secret Key
**Vulnerability:** The Flask application used a random hex string as a fallback for the `SECRET_KEY` if the environment variable was not set (`os.environ.get('SECRET_KEY', secrets.token_hex(32))`).
**Learning:** Using a random fallback for the secret key causes session invalidation on every server restart and is insecure in multi-worker environments (e.g., Gunicorn), as each worker would generate a different key, leading to inconsistent session decryption.
**Prevention:** Explicitly require a stable, securely-generated `SECRET_KEY` from the environment in production contexts. Raise a `RuntimeError` during application startup if it's missing, and only allow a stable development fallback when explicitly in debug mode.
## 2026-05-09 - CSRF Token Timing Attack
**Vulnerability:** The CSRF token validation in `webapp/app.py` used standard string equality (`==` or `!=`) to compare the user-provided token with the expected token.
**Learning:** Standard string equality operators fail fast, taking less time to evaluate when the strings mismatch early on. This can be exploited in a timing attack, where an attacker measures the time it takes the server to respond to determine the correctness of a token character by character.
**Prevention:** Always use a constant-time comparison function, such as `secrets.compare_digest()`, when comparing cryptographic tokens, passwords, or secrets (e.g., CSRF tokens) to prevent timing side-channel attacks.
## 2026-06-25 - [CSP] Removed unsafe-inline and refactored inline scripts
**Vulnerability:** The Flask application's Content Security Policy (CSP) used the `'unsafe-inline'` directive in `default-src`, and multiple inline scripts (e.g., `<script>` tags without nonces) and inline event handlers (e.g., `onclick`, `onsubmit`) were present in the templates. This setup significantly weakened XSS protection.
**Learning:** `unsafe-inline` was likely allowed to easily support inline Bootstrap scripts and quick event bindings like `onclick="addDate()"`. However, it leaves the application vulnerable to Cross-Site Scripting (XSS) attacks by allowing an attacker to execute arbitrary inline scripts if they can inject them into the DOM.
**Prevention:** Always refactor inline event handlers (like `onclick` or `onsubmit`) to use `addEventListener` inside nonced script blocks or external JS files. When building a CSP, avoid `'unsafe-inline'` and enforce a secure nonce or hash-based policy for all script execution.
