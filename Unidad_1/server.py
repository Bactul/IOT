from http.server import BaseHTTPRequestHandler, HTTPServer
import json

contador = 0

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, content_type="text/plain"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        self._set_response()
        respuesta = "El valor es: " + str(contador)
        self.wfile.write(respuesta.encode())

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        body_json = json.loads(post_data.decode())

        global contador

        if "action" in body_json and "quantity" in body_json:
            action = body_json["action"]
            quantity = int(body_json["quantity"])

            if action == 'asc':
                contador += quantity
            elif action == 'desc':
                contador -= quantity

            # Respond to the client
            response_data = json.dumps({"message": "Received POST data", "data": body_json, "status": "OK"})
            self._set_response("application/json")
            self.wfile.write(response_data.encode())
        else:
            response_data = json.dumps({"message": "Invalid POST data format", "status": "Error"})
            self._set_response("application/json")
            self.wfile.write(response_data.encode())

def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=7800):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
