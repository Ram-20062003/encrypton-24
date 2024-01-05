from typing import Tuple
from collections import namedtuple
from decimal import Decimal
import base64, os
from uu import decode

from fastapi.param_functions import Depends
from sqlmodel import SQLModel, Session
from config.database import get_database
from server.models.schema import Transaction
from server.controller.ml import predict_autoencoder, predict_isolation
from config.socket import manager


current_directory = os.getcwd()


class SocketResponse(SQLModel):
    amount: Decimal
    is_fraud: int
    image: str
    confidence: float
    time : int

    

async def predict(transaction: Transaction,database: Session):
    CASH_IN = 0
    CASH_OUT = 0
    DEBIT = 0
    PAYMENT = 0
    TRANSFER = 0
    if transaction.transaction_type == 'CASH_IN':
        CASH_IN = 1
    elif transaction.transaction_type == 'CASH_OUT':
        CASH_OUT = 1
    elif transaction.transaction_type == 'DEBIT':
        DEBIT = 1
    elif transaction.transaction_type == 'PAYMENT':
        PAYMENT = 1
    elif transaction.transaction_type == 'TRANSFER':
        TRANSFER = 1
    inp = namedtuple('inp', ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'changebalanceOrig', 'changebalanceDest', 'hour', 'CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])
    transformed_data = inp(float(transaction.amount),float(transaction.sender_old_balance), float(transaction.sender_new_balance), float(transaction.receiver_old_balance), float(transaction.receiver_new_balance), float(transaction.sender_new_balance-transaction.sender_old_balance), float(transaction.receiver_new_balance-transaction.receiver_old_balance), transaction.time, CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER)
    if not transaction.id:
        return 0
    prediction_iso = predict_isolation(transformed_data,transaction.id)
    ae= predict_autoencoder(transformed_data)
    if len(ae)!=2:
        return 0
    prediction_ae = ae[0]
    confidence = ae[1]


    with open(f"{current_directory}/server/controller/ml/images/gg-{transaction.id}.png", "rb") as image_file:
        image = base64.b64encode(image_file.read())

    if prediction_ae == 1:
        transaction.is_fraud = 1
    else:
        transaction.is_fraud = 0
    database.add(transaction)
    database.commit()
    res = SocketResponse(amount=transaction.amount,is_fraud=prediction_iso,image=image.decode(), confidence=confidence, time=transaction.time)
    await manager.send_to_user(res,transaction.user_id)





