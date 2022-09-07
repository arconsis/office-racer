from typing import Optional, Any

import websockets
from websockets import WebSocketServerProtocol
import asyncio

PORT = 7890
URL = "0.0.0.0"


def is_controller(websocket: WebSocketServerProtocol) -> bool:
    return websocket.path == "/controller"


def is_racer(websocket: WebSocketServerProtocol) -> bool:
    return websocket.path == "/racer"


class Server:
    racers = dict()  # <racer.ID, associated Racer>
    unassigned_racer_ids = set()

    controllers = dict()  # <controller.ID, associated Controller>
    unassigned_controller_ids = set()

    relationships = dict()  # <controller.ID, racer.ID>

    async def websocket_handler(self, websocket: WebSocketServerProtocol) -> None:
        await self.__register(websocket)
        await websocket.send("You are connected to the server")
        try:
            await self.__distribute(websocket)
        except KeyError:
            pass
        finally:
            await self.__unregister(websocket)

    async def __unregister(self, websocket: WebSocketServerProtocol) -> None:
        if is_controller(websocket):
            print("disconnect Controller")
            racer_id = self.relationships.pop(websocket.id, None)
            if racer_id is not None:
                self.unassigned_racer_ids.add(racer_id)
            self.controllers.pop(websocket.id, None)
        elif is_racer(websocket):
            print("disconnect Racer")
            controller_id = self.pop_relationship_with_racer_id(websocket.id)
            if controller_id is not None:
                self.unassigned_controller_ids.add(controller_id)
            self.racers.pop(websocket.id, None)

        print(f'controller: {len(self.controllers.keys())} | racer: {len(self.racers.keys())}')

    async def __register(self, websocket: WebSocketServerProtocol) -> None:
        if is_controller(websocket):
            self.controllers[websocket.id] = websocket
            print(f'Controller: {websocket.id} connected')
            if len(self.unassigned_racer_ids) == 0:
                self.unassigned_controller_ids.add(websocket.id)
            else:
                new_racer_id = self.unassigned_racer_ids.pop()
                self.relationships[websocket.id] = new_racer_id
                await self.__send_match_found_to(websocket.id, new_racer_id)

        elif is_racer(websocket):
            self.racers[websocket.id] = websocket
            print(f'Racer: {websocket.id} connected')
            # connect to unassigned controller
            if len(self.unassigned_controller_ids) == 0:
                self.unassigned_racer_ids.add(websocket.id)
            else:
                new_controller_id = self.unassigned_controller_ids.pop()
                self.relationships[new_controller_id] = websocket.id
                await self.__send_match_found_to(new_controller_id, websocket.id)
        else:
            print(f'Could not add client at {websocket.remote_address} for Path: {websocket.path}')
            await websocket.send("You shall not pass")

        print(f'ClientID: {websocket.id}')
        print(f'controller: {len(self.controllers.keys())} | racer: {len(self.racers.keys())}')

    async def __distribute(self, websocket: WebSocketServerProtocol) -> None:
        async for message in websocket:
            if is_controller(websocket):
                if websocket.id in self.relationships.keys():
                    racer_id = self.relationships[websocket.id]
                    racer = self.racers[racer_id]
                    await racer.send(message)

    async def __send_match_found_to(self, controller_id: str, racer_id: str) -> None:
        controller = self.controllers[controller_id]
        await controller.send(f'paired to racer: {racer_id}')
        racer = self.racers[racer_id]
        await racer.send(f'paired to controller: {controller_id}')

    def pop_relationship_with_racer_id(self, racer_id: str) -> Optional[str]:
        for key in self.relationships.keys():
            found_racer_id = self.relationships[key]
            if found_racer_id == racer_id:
                del self.relationships[key]
                return key
        return None


if __name__ == '__main__':
    print("Initialize Server")
    server = Server()
    start_server = websockets.serve(server.websocket_handler, URL, PORT)
    print(f'Start with {len(start_server.ws_server.websockets)} active Websockets')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
