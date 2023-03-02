import os
import asyncio


import nats
from nats.errors import TimeoutError, NoRespondersError


servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")


async def main():
    
    nc = await nats.connect(servers=servers)
    # NATS JetStream에서 메시지를 생성하고 소비하는 데 사용할 수 있는 컨텍스트를 반환
    js = nc.jetstream()
    #add_stream creates a stream.
    await js.add_stream(name='hello', subjects=['hello'])
    #pub
    await js.publish('hello', b'Hello JS!')

    async def cb(msg):
      print('Received:', msg)

    # Ephemeral Async Subscribe
    await js.subscribe('hello', cb=cb)

    # Durable Async Subscribe
    # NOTE: Only one subscription can be bound to a durable name. It also auto acks by default.
    await js.subscribe('hello', cb=cb, durable='foo')
    
    # Durable Sync Subscribe
    # NOTE: Sync subscribers do not auto ack.
    await js.subscribe('hello', durable='bar')

    # Queue Async Subscribe
    # NOTE: Here 'workers' becomes deliver_group, durable name and queue name.
    await js.subscribe('hello', 'workers', cb=cb)
    
    await js.delete_stream('hello')

if __name__ == '__main__':
    asyncio.run(main())