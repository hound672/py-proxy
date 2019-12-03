# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

import asyncio

async def main():
    print('Start')

    reader, writer = await asyncio.open_connection(host='localhost', port=8888)

    while True:
        writer.write(b'!!!!!!')
        data = await reader.read(100)
        print('data: ', data)

        coro = reader.read(100)
        data = await asyncio.wait_for(coro, 1)

        print('data 2: ', data)


        break

    writer.close()

if __name__ == '__main__':
    asyncio.run(main())