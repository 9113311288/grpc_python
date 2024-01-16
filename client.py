import grpc
import Filetransfer_pb2
import Filetransfer_pb2_grpc

def send_data(stub, file_path):
    CHUNK_SIZE = 1024 * 1024

    # Open the file and send chunks as a stream
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b''):
            request = Filetransfer_pb2.DataRequest(data=chunk)
            try:
                response = stub.ProcessData(iter([request]))
                print(response.message)  # Print server response
            except grpc.RpcError as e:
                print(f"Error sending data: {e}")
                break

def run_client():
    # Specify the correct server IP address and port
    server_address = '127.0.0.1:50051'  # Replace with the server's IP and port
    channel = grpc.insecure_channel(server_address)
    stub = Filetransfer_pb2_grpc.FileTransferStub(channel)

    # Replace 'path_to_your_file' with the path to your file
    file_path = "C:\\Users\\Akshay\\Downloads\\sample.mp4"
    send_data(stub, file_path)

if __name__ == '__main__':
    run_client()
