from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import os
import ssl
class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        print(f'Received POST request:\n{self.headers}\nContent: {post_data}')
        print(f'Received POST request.\nUseful Content: {post_data}')
        
        
        if not getattr(self, 'post_handled', False):  # Check if logic already executed
            #params = parse_qs(post_data)
            params = json.loads(post_data)
            
            print("btn1 pressed by **")
            print("start of params log")
            print(params)
            print("end of params log")

            if params.get('buttonId', '') == 'btn1':
                print("btn1 pressed by me")
                # Button 1 was pressed
                file_list = self.get_file_list()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file_list, 'utf-8'))
                # Set the flag to True to indicate that the logic has been executed
                self.post_handled = True
            elif params.get('buttonId', '') == 'btn2':
                # Button 2 was pressed
                print("btn2 pressed by me this time")
                folder_list = self.get_folder_list()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(folder_list, 'utf-8'))
                # Set the flag to True to indicate that the logic has been executed
                self.post_handled = True
            elif params.get('buttonId', '') == 'btn3':
                # Button 3 was pressed
                print("btn 3 was pressed")
                all_files_list = self.get_all_files_list()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(all_files_list, 'utf-8'))
                self.post_handled = True
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Invalid request')

    # def get_file_list(self):
    #     # Implement your logic to analyze files and return a formatted list
    #     # For simplicity, a placeholder list is used here
    #     file_list = ['file1.txt', 'file2.txt', 'file3.txt']
    #     return '<ul>' + ''.join([f'<li>{file}</li>' for file in file_list]) + '</ul>'

    def get_file_list(self, directory='.'):
        try:
            files = os.listdir(directory)
            file_list = [f for f in files if os.path.isfile(os.path.join(directory, f))]
            if file_list:
                return '<ul>' + ''.join([f'<li>{file}</li>' for file in file_list]) + '</ul>'
            else:
                return '<p>No files found</p>'
        except Exception as e:
            print(f"Error retrieving file list: {e}")
            return '<p>Error retrieving file list.</p>'


    # def get_folder_list(self):
    #     # Implement your logic to analyze folders and return a formatted list
    #     # For simplicity, a placeholder list is used here
    #     folder_list = ['folder1', 'folder2', 'folder3']
    #     return '<ul>' + ''.join([f'<li>{folder}</li>' for folder in folder_list]) + '</ul>'

    def get_folder_list(self, directory='.'):
        try:
            folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
            if folders:
                return '<ul>' + ''.join([f'<li>{folder}</li>' for folder in folders]) + '</ul>'
            else:
                return '<p>NO folders found</p>'
        except Exception as e:
            print(f"Error retrieving folder list: {e}")
            return '<p>Error retrieving folder list.</p>'
        
    def get_all_files_list(self):
        root_path = os.path.join(os.getenv('EXTERNAL_STORAGE'), '')
        return self.list_files_in_directory(root_path)

    def list_files_in_directory(self, directory):
        try:
            file_list = os.listdir(directory)
            formatted_list = '<ul>' + ''.join([f'<li>{item}</li>' for item in file_list]) + '</ul>'
            return formatted_list
        except Exception as e:
            print(f"Error listing files in {directory}: {e}")
            return 'Error listing files.'
        
    # def get_all_files_list(self):
    #     root_path = '/'  # You can change this to the desired root path
    #     all_files = []
    #     for root, dirs, files in os.walk(root_path):
    #         for file in files:
    #             all_files.append(os.path.join(root, file))
    #     return '<ul>' + ''.join([f'<li>{file}</li>' for file in all_files]) + '</ul>'
    
if __name__ == '__main__':
    server_address = ('0.0.0.0', 8000)
    # handler = MyRequestHandler
    # server = HTTPServer(server_address, handler)
    httpd = HTTPServer(server_address, MyRequestHandler)
     # Create an SSL context and load your certificate and private key
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='path/to/your/certificate.pem', keyfile='path/to/your/private_key.pem')

    # Wrap the HTTPServer with the SSL context
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print('Server started on https://localhost:8000')
    httpd.serve_forever()
    
