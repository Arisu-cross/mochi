# 单端口合并入口:游戏本体(Flask)和 MCP(SSE)跑在同一个 uvicorn 进程里。
# 云平台(Zeabur 等)一个服务通常只暴露一个端口;原版双进程双端口要开两个服务,
# 存档文件还没法共享。合并后:/sse 和 /messages 归 MCP,其余全部归 Flask 网页。
import os

PORT = int(os.environ.get('PORT', 8080))
# MCP 工具通过 HTTP 调游戏 API;单进程模式下就是调自己(阻塞调用已在 mcp_server
# 里用 to_thread 隔离,不会死锁)。显式设了 MOCHI_API 则以设置为准。
os.environ.setdefault('MOCHI_API', f'http://127.0.0.1:{PORT}/api')

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from a2wsgi import WSGIMiddleware

import app as game
import mcp_server

app = Starlette(routes=[
    Route('/sse', endpoint=mcp_server.handle_sse),
    Mount('/messages/', app=mcp_server.logged_messages),
    Mount('/', app=WSGIMiddleware(game.app)),
])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=PORT)
