#!/usr/bin/env python3

import http.server, pkgutil, socket

class Handler(http.server.BaseHTTPRequestHandler):
	ENCODING = 'UTF-8'
	CONTENT_TEMPLATE = pkgutil.get_data('demo_http_server', 'content_template.html').decode(ENCODING)

	def do_GET(self):
		if self.path == '/':
			a = dict(service=socket.getfqdn())
			a['server_ip'], a['server_port'] = self.connection.getsockname()
			a['server_name'] = socket.getfqdn(a['server_ip'])
			a['client_ip'], a['client_port'] = self.connection.getpeername()
			a['client_name'] = socket.getfqdn(a['client_ip'])
			content = self.CONTENT_TEMPLATE.format(**a)
			data = content.encode(self.ENCODING)
		else:
			try:
				data = pkgutil.get_data('demo_http_server', self.path)
			except:
				import logging, traceback
				logging.debug(traceback.format_exc())
				self.send_response(404)
				self.end_headers()
				return

		self.send_response(200)
		self.send_header("Content-length", str(len(data)))
		self.end_headers()
		self.wfile.write(data)

def serve(ports):
	import threading, logging
	server_threads = []
	for portdef in ports:
		ip, port = portdef.split() if ':' in portdef else ('', portdef)
		server = http.server.HTTPServer((ip, int(port)), Handler)
		thread = threading.Thread(target=server.serve_forever, name='serve-' + portdef)
		logging.info('starting HTTP server on ' + portdef)
		thread.start()
		server_threads.append(thread)
	return server_threads

#if __name__ == '__main__':
def main():
	import logging, argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('port', nargs='+', help='local TCP bindings of the form [ip:]port')
	args = parser.parse_args()
	serve(args.port)

	try:
		while True:
			time.sleep(10)
	except:
		logging.info('\nexiting')

