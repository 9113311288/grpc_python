import grpc
from concurrent import futures
import Filetransfer_pb2
import Filetransfer_pb2_grpc
from moviepy.editor import VideoFileClip

class FileTransferServicer(Filetransfer_pb2_grpc.FileTransferServicer):
    def ProcessData(self, request_iterator, context):
        received_data = b''

        # Receiving and accumulating data
        for chunk in request_iterator:
            received_data += chunk.data

        # Save received data to a temporary file
        temp_file_path = 'received_data.mp4'
        with open(temp_file_path, 'wb') as output_file:
            output_file.write(received_data)

        # Process the received data (e.g., compress a video file)
        compressed_file_path = 'compressed_data.mp4'
        try:
            video_clip = VideoFileClip(temp_file_path)

            # Resize the video clip
            resized_clip = video_clip.resize(width=video_clip.w // 2, height=video_clip.h // 2)

            # Write the resized clip to the compressed file
            resized_clip.write_videofile(compressed_file_path, codec='libx264', bitrate='5000k')

            # Close the clips
            video_clip.close()
            resized_clip.close()

        except Exception as e:
            return Filetransfer_pb2.DataResponse(message=f"Error processing data: {e}")

        # Respond with a success message
        return Filetransfer_pb2.DataResponse(message="Data received, processed, and saved!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port('127.0.0.1:50051')  # Server listening on specified IP and port
    server.start()
    print("Server started. Listening on port 127.0.0.1:50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
