#!/usr/bin/env python
from trial.server.main import run_server
from trial.model import initialize_db

if __name__ == "__main__" :
	initialize_db()
	run_server()
