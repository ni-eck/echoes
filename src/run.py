#!/usr/bin/env python3
"""Run the Echoes application programmatically."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "echoes.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )