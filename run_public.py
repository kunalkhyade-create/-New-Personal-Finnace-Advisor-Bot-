"""
run_public.py — Launch the Personal Finance Advisor Bot with a public Ngrok tunnel.

Usage:
    python run_public.py

Replace the TOKEN value below with your own Ngrok authtoken from https://dashboard.ngrok.com
"""

import threading
from pyngrok import ngrok, conf
from app import app

# -----------------------------------------------------------------------
# REPLACE WITH YOUR NGROK AUTHTOKEN
# -----------------------------------------------------------------------
TOKEN = "YOUR_NGROK_AUTHTOKEN_HERE"
# -----------------------------------------------------------------------


def start_flask():
    """Run Flask in a background thread (debug=False to avoid reloader issues)."""
    app.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False)


if __name__ == "__main__":
    # Configure Ngrok authtoken
    conf.get_default().auth_token = TOKEN

    # Open the public tunnel
    tunnel = ngrok.connect(5000, "http")
    public_url = tunnel.public_url

    print("\n" + "=" * 60)
    print("  YOUR PUBLIC WEBSITE URL IS LIVE!")
    print("  URL: {}".format(public_url))
    print("=" * 60)
    print("  Share this URL with anyone to access your Finance Bot.")
    print("  Press Ctrl+C to stop.\n")

    # Start Flask in a daemon thread so Ctrl+C stops everything cleanly
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    try:
        flask_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down tunnel...")
        ngrok.disconnect(public_url)
        ngrok.kill()
