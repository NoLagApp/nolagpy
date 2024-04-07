from nolagpy import WebSocketClient
import asyncio

try:
    async def main():
        device_token = "07b9b128b840b61a1d8c22a0063ae240"

        # Connect to Tunnel
        nolag_client = await WebSocketClient(device_token)

        # get device token ID
        print(f"{nolag_client.deviceTokenId}")

    asyncio.run(main())

except Exception as e:
    # Handle any other exception
    print(f"An error occurred: {e}")
