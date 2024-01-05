import sys
from typing import Dict

from fastapi import FastAPI, HTTPException,WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from server.controller.auth import get_current_user
from config.database import get_database
from sqlmodel import Session, select
from config.dependencies import firewall_init_config, docker_init_config, \
									   check_sudo, restart_docker, restart_firewalld
from config.socket import manager

from server.routers import auth, parse_csv, transaction, firewall


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transaction.router)
# app.include_router(parse_csv.router)
app.include_router(firewall.router)

# check_sudo()
# docker_init_config()
# firewall_init_config()
# restart_docker()
# restart_firewalld()

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, database: Session = Depends(get_database)):
    user = get_current_user(token, database)
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid User")
    await manager.connect(websocket,user.id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user.id)
