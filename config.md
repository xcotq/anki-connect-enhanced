# AnkiConnect Local configuration

Restart Anki after changing these values.

- `apiKey`: Optional API key. When set, include the same value in the top-level `key` property of every API request.
- `apiPollInterval`: Server polling interval in milliseconds.
- `webBacklog`: Maximum number of pending socket connections.
- `webBindAddress`: Address on which the HTTP API listens. Keep `127.0.0.1` unless remote access is required.
- `webBindPort`: HTTP API port.
- `webCorsOriginList`: Browser origins allowed to make cross-origin API requests. Add only origins you trust. Use `"*"` only if unrestricted browser access is intentional.
