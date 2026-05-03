# run.py
# Alternative entry point — use this instead of "python app.py"
# Useful for setting environment variables cleanly before starting.

import os
from app import app

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)   # ensure data/ folder exists
    
    print("=" * 45)
    print("  ⚡ LifeAssist AI — Starting Server")
    print("=" * 45)
    print("  URL : http://127.0.0.1:5000")
    print("  Mode: Development")
    print("  Press CTRL+C to stop")
    print("=" * 45)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )