import os
import asyncio


import nats
from nats.errors import TimeoutError, NoRespondersError


servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")


async def main():
    
    nc = await nats.connect(servers=servers)
    # NATS JetStream에서 메시지를 생성하고 소비하는 데 사용할 수 있는 컨텍스트를 반환
    js = nc.jetstream()
    
    await js.add_stream(name='hello', subjects=['hello'])
    #asyncnats.js.client.JetStreamContext.publish(self, subject, payload=b'', timeout=None, stream=None, headers=None)
    #ack = await js.publish(stream, payload)
    ack = await js.publish('hello', b'Hello JS!')
    
    print(f'Ack: stream={ack.stream}, sequence={ack.seq}')
    # Ack: stream=hello, sequence=1
    await nc.close()
 
if __name__ == '__main__':
    asyncio.run(main())