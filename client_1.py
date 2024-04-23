
import socket
import pickle
import cv2
import numpy as np

# Create a blank image for displaying trajectory coordinates


# Set up socket for client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

frame_data_bytes = client_socket.recv(4096)
frame_data = pickle.loads(frame_data_bytes)
frame_width = frame_data['width']
frame_height = frame_data['height']

# Create a blank image of the same size as the received frame dimensions
blank_image = np.zeros((frame_height, frame_width, 3), np.uint8)
person_colors = {}

while True:
    # Receive trajectory data from server
    trajectory_data_bytes = client_socket.recv(4096)
    trajectory_data = pickle.loads(trajectory_data_bytes)

    # Print trajectory data
    print(f"ID: {trajectory_data['id']}, Trajectory: {trajectory_data['trajectory']}")

    # Update the blank image with trajectory coordinates
    for i, point in enumerate(trajectory_data['trajectory']):
        # Assign a unique color for each person ID
        color = tuple(map(int, np.random.randint(0, 255, size=3)))

        # Display trajectory coordinates on the blank image
        cv2.circle(blank_image, point, 5, color, -1)


    # if frame_data['trajectory_data']['id'] not in person_colors:
    #     person_colors[frame_data['trajectory_data']['id']] = tuple(map(int, np.random.randint(0, 255, size=3)))

    # # Update the blank image with trajectory coordinates
    # for point in frame_data['trajectory_data']['trajectory']:
    #     # Get color for the current person ID
    #     color = person_colors[frame_data['trajectory_data']['id']]

    #     # Display trajectory coordinates on the blank image
    #     cv2.circle(blank_image, point, 5, color, -1)
    #     cv2.putText(blank_image, str(frame_data['trajectory_data']['id']), point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the blank image with trajectory coordinates
    cv2.imshow('Trajectory', blank_image)
    cv2.waitKey(1)

# Close socket
client_socket.close()








# import socket
# import pickle
# import cv2
# import numpy as np

# # Create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Define the host and port for communication
# host = "127.0.0.1"
# port = 12345

# # Connect to the server
# client_socket.connect((host, port))

# print("Connected to server...")

# while True:
#     # Receive trajectory data from the server
#     data = b""
#     while True:
#         packet = client_socket.recv(4096)
#         if not packet:
#             break
#         data += packet

#     # Deserialize received data
#     try:
#         received_data = pickle.loads(data)
#         track_id = received_data['id']
#         trajectory = received_data['trajectory']

#         # Process trajectory data
#         print(f"Received trajectory data for track ID {track_id}: {trajectory}")

#         # Example: Display received trajectory points on an image
#         # Create a blank image
#         image = np.zeros((720, 1280, 3), dtype=np.uint8)
#         # Plot received trajectory points
#         for point in trajectory:
#             cv2.circle(image, point, 5, (0, 255, 0), -1)
#         # Display image
#         cv2.imshow("Received Trajectory", image)
#         cv2.waitKey(0)

#     except pickle.UnpicklingError:
#         print("Error: Unable to deserialize received data")
#     except Exception as e:
#         print(f"Error: {e}")

# # Close the client socket
# client_socket.close()


# import socket
# import pickle
# import cv2
# import numpy as np

# # Create a blank image for displaying trajectory coordinates
# blank_image = np.zeros((500, 500, 3), np.uint8)

# # Set up socket for client
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('localhost', 5000))

# while True:
#     # Receive trajectory data from server
#     trajectory_data_bytes = client_socket.recv(4096)
#     trajectory_data = pickle.loads(trajectory_data_bytes)

#     # Print trajectory data
#     print(f"ID: {trajectory_data['id']}, Trajectory: {trajectory_data['trajectory']}")

#     # Display trajectory coordinates on the blank image
#     for point in trajectory_data['trajectory']:
#         cv2.circle(blank_image, point, 5, (0, 255, 0), -1)

#     # Display the blank image with trajectory coordinates
#     cv2.imshow('Trajectory', blank_image)
#     cv2.waitKey(1)

# # Close socket
# client_socket.close()