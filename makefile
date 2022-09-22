demo-server.pyz: demo-server/*
	python3 -m zipapp demo-server --python "/usr/bin/env python3" --output $@ --main demo_http_server:main --compress
