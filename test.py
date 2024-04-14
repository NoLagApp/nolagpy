from nolagpy import WebSocketClient
import asyncio

try:
    async def main():
        device_token = "07b9b128b840b61a1d8c22a0063ae240"

        # Connect to Tunnel
        nolag_client = await WebSocketClient(device_token)

        nolag_client.subscribe("video", {
            "OR": [
                "test"
            ]
        })
        print(33333333)
        while True:
            nolag_client.onReceive(
                lambda received: print("received:", received))

        # get device token ID
        print(f"{nolag_client.deviceTokenId}")
    # main()
    asyncio.run(main())

except Exception as e:
    # Handle any other exception
    print(f"An error occurred: {e}")


# import websocket
# import time


# def on_message(ws, message):
#     print("Received message:", message)


# def on_error(ws, error):
#     print("Error:", error)


# def on_close(ws):
#     print("Connection closed")


# connectionOpen = False


# def on_open(ws):
#     connectionOpen = True
#     print("Connection opened")

#     # websocket.enableTrace(True)


# counter = 0
# with websocket.WebSocketApp("wss://echo.websocket.org/",
#                             on_message=on_message,
#                             on_error=on_error,
#                             on_close=on_close) as websocket:
#     websocket.run_forever()

# while True:
#     try:
#         # ws = websocket.WebSocketApp("wss://echo.websocket.org/",
#         #                             on_message=on_message,
#         #                             on_error=on_error,
#         #                             on_close=on_close)
#         # # ws.close()
#         # counter = counter + 1
#         # ws.on_open = lambda ws: on_open(ws)
#         print(connectionOpen)
#         # # ws.send(f"Hello: {counter}")
#         # ws.run_forever()
#         # print(connectionOpen)
#     except Exception as e:
#         print("Exception occurred:", e)
#         # Wait for a while before reconnecting
#         time.sleep(5)  # Adjust the interval as needed


# import asyncio
# from websockets.sync.client import connect


# def hello():
#     with connect("wss://echo.websocket.org") as websocket:
#         # print(f"send:")
#         # websocket.send("Hello world!")
#         # message = websocket.recv()
#         # print(f"Received: {message}")
#         return websocket


# ws = hello()
# ws.recv()
# print(f"recv")

# import keyboard  # pip install keyboard
# import websocket  # pip install websocket-client

# # WebSocket server URL
# WS_SERVER_URL = "wss://echo.websocket.org"


# def on_message(ws, message):
#     print("Received message from server:", message)


# def on_error(ws, error):
#     print("Error:", error)


# def on_close(ws):
#     print("WebSocket connection closed")


# def on_open(ws):
#     print("WebSocket connection established")


# def send_message(message):
#     ws.send(message)


# # Create WebSocket connection
# ws = websocket.WebSocketApp(WS_SERVER_URL,
#                             on_message=on_message,
#                             on_error=on_error,
#                             on_close=on_close)

# ws.on_open = on_open

# # Start the WebSocket connection
# # ws_thread = ws.run_forever()

# # Function to handle key press events


# def on_key_press(event):
#     if event.event_type == keyboard.KEY_DOWN:
#         # Send a message when a key is pressed
#         send_message("Key pressed: " + event.name)


# # Register the key press event handler
# keyboard.on_press(on_key_press)

# # Keep the main thread alive
# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     print("Exiting...")
#     ws.close()
#     ws_thread.join()
