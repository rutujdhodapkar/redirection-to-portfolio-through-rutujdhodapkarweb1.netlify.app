import asyncio
import websockets

# List to hold all connected clients
connected_clients = set()

async def handler(websocket, path):
    # Add the new connection to the set of connected clients
    connected_clients.add(websocket)
    try:
        # Wait for incoming messages from the client
        async for message in websocket:
            # Broadcast the message to all other connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("A client disconnected.")
    finally:
        # Remove the client from the list of connected clients when they disconnect
        connected_clients.remove(websocket)

# Start the WebSocket server
async def main():
    server = await websockets.serve(handler, "localhost", 8080)
    print("Server started on ws://localhost:8080")
    await server.wait_closed()

# Run the server
asyncio.run(main())
