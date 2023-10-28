# Home Assistant Control

## Overview

Home Assistant Control is a Python package for interacting with [Home Assistant](https://www.home-assistant.io/), a
popular platform for smart home automation. This package provides a simple and extensible interface for controlling Home
Assistant entities via RESTful and WebSocket APIs.

----

## Features

- **Entity Control**: Manipulate entities like lights, switches, etc., programmatically.
- **RESTful API**: Interact with Home Assistant via its RESTful API for synchronous tasks.
- **WebSocket Support**: Real-time updates and asynchronous operations via Home Assistant's WebSocket API.
- **Token Authentication**: Securely connect to your Home Assistant instance using authentication tokens.

----

## Requirements

- Python 3.x
- `requests` library for RESTful API
- `websockets` library for WebSocket API

----

## Installation

### Using pip

```bash
pip install home_assistant_control
```

### From Source

```bash
git clone https://github.com/your-repo/home_assistant_control.git
cd home_assistant_control
python setup.py install
```

----

## Quick Start

### RESTful API

```python
from home_assistant_control.client import Client
from home_assistant_control.controllers.lights import LightController

# Initialize client
client = Client('http://your-home-assistant:8123', 'your-long-lived-access-token')

# Refresh entity data
client.refresh()

# Interact with entities
light_controller = LightController(client.entities.get_all_in_category()[0])
light_controller.change_light_color('light.living_room', 'red')
```

### WebSocket API

```python
import asyncio
from home_assistant_control.client import Client
from home_assistant_control.client.websocket import WebSocketClient

# Initialize RESTful client
client = Client('http://your-home-assistant:8123', 'your-long-lived-access-token')

# Initialize WebSocket client
ws_client = WebSocketClient(client)


async def main():
    await ws_client.connect()
    await ws_client.authenticate()
    # ... other WebSocket operations ...


# Run the event loop
asyncio.get_event_loop().run_until_complete(main())
```

----

## Documentation

For more detailed documentation, check the docs/ folder. 
