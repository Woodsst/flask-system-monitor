#!/bin/sh
python3 /flask_system_monitor/server/server.py&
cd /flask_system_monitor/tests
pytest -v
