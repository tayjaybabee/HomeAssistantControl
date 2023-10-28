import asyncio
import websockets
import json


class WebSocketClient:

    def __init__(self, client):
        """
        Initializes a new instance of the WebSocketClient class.

        Args:
            client (Client): An instance of the Client class.
        """
        self.client = client
        self.websocket = None

    async def connect(self):
        """
        Connect to the Home Assistant WebSocket API.

        Returns:
            None: Establishes the WebSocket connection.
        """
        self.websocket = await websockets.connect(f"{self.client.url}/api/websocket")
        print(f"Connected to WebSocket at {self.client.url}")

    async def authenticate(self):
        """
        Authenticate the WebSocket connection using the stored token.

        Returns:
            None: Sends the authentication message over the WebSocket.
        """
        auth_message = json.dumps({
                "type":         "auth",
                "access_token": self.client.token
                })
        await self.websocket.send(auth_message)

        # Wait for acknowledgment or error
        response = await self.websocket.recv()
        response_data = json.loads(response)

        if response_data["type"] == "auth_ok":
            print("WebSocket authentication successful")
        else:
            print(f"WebSocket authentication failed: {response_data.get('message', 'Unknown error')}")

    async def send_message(self, message: dict):
        """
        Send a message over the WebSocket connection.

        Args:
            message (dict): The message to send.

        Returns:
            None: Sends the message over the WebSocket.
        """
        await self.websocket.send(json.dumps(message))
        print(f"Sent message: {message}")

    async def receive_message(self):
        """
        Receive a message from the WebSocket connection.

        Returns:
            dict: The received message.
        """
        response = await self.websocket.recv()
        print(f"Received message: {response}")
        return json.loads(response)

    async def close(self):
        """
        Close the WebSocket connection.

        Returns:
            None: Closes the WebSocket connection.
        """
        await self.websocket.close()
        print("WebSocket connection closed")
