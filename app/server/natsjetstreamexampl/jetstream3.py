import os
import asyncio
import time

import nats
from nats.errors import TimeoutError, NoRespondersError


servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")


async def main():
    
    nc = await nats.connect(servers=servers)
    
    # NATS JetStream에서 메시지를 생성하고 소비하는 데 사용할 수 있는 컨텍스트를 반환
    js = nc.jetstream()
    
    #add_stream creates a stream. storage='NONE or FILE or MEMORY'
    await js.add_stream(name='events', subjects=['events.*']) #기본 stream
    #pub
    await js.publish('events.page_loaded',b'')
    await js.publish('events.mouse_clicked',b'')
    await js.publish('events.mouse_clicked',b'')
    await js.publish('events.page_loaded',b'')
    await js.publish('events.mouse_clicked',b'')
    await js.publish('events.input_focused',b'')
    print("published 6 messages","\n")

    #message 갯수 확인하기state=StreamState(messages=6
    print(await js.streams_info(),"\n")
    # streamconfig=nats.js.api.StreamConfig(name='event', subjects='event')
    # print(streamconfig)
    
    await js.update_stream(name='events', subjects=['events.*'],max_msgs=10)
    print("set max messages to 10","\n")
    
    #max_msgs 갯수 체크 max_msgs=10
    print(await js.streams_info(),"\n")
    
    await js.update_stream(name='events', subjects=['events.*'],max_msgs=10,max_bytes=300)
    print("set max bytes to 300","\n")
    
    #max_bytes 갯수 체크 max_bytes=10
    print(await js.streams_info(),"\n")
    
    await js.update_stream(name='events', subjects=['events.*'],max_msgs=10,max_bytes=300, max_age=0.1)
    print("set max age to one second","\n")
    
    #max_age 갯수 체크 max_age=1.0
    print(await js.streams_info(),"\n")
   
    
    time.sleep(10)
    #max_age 갯수 체크 max_age=1.0
    print(await js.streams_info())
   
    
    await js.delete_stream('events')

if __name__ == '__main__':
    asyncio.run(main())