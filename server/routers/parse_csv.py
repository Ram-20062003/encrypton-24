
# import csv
# from fastapi import APIRouter, HTTPException, File, UploadFile
# from fastapi.param_functions import Depends
# from fastapi.responses import JSONResponse
# from server.controller.auth import get_current_user
# from sqlmodel import Session, select
# from server.models.schema import *
# from config.database import get_database
# import shutil
# from pathlib import Path
# from server.controller.auth import sign_jwt, JWTBearer
# from server.models.transaction import TransactionBase

# router = APIRouter(
# 	prefix="/input",
# )

# # Directory to save the uploaded files
# upload_dir = Path("uploads")
# upload_dir.mkdir(exist_ok=True)

# @router.post("/csv")
# async def upload_csv(
# 	file: UploadFile = File(...),
# 	bearer_token: str = Depends(JWTBearer()),
# 	db: Session = Depends(get_database)
# ):
# 	user = get_current_user(bearer_token, db)
# 	if not user or not user.id:
# 		raise HTTPException(status_code=401, detail="Invalid User")
# 	try:
# 		# Save the file in the "uploads" directory
# 		if not file.filename:
# 			raise HTTPException(status_code=400, detail="No file name")
# 		file_path = upload_dir / file.filename
# 		with file_path.open("wb") as buffer:
# 			shutil.copyfileobj(file.file, buffer)
# 		with open(file_path, newline='', encoding='utf-8') as csvfile:
# 			csv_reader = csv.reader(csvfile)
			
# 			# Read the header row to get field names
# 			headers = next(csv_reader)
# 			print("Field Names:", headers)

# 			# i=0
# 			for row in csv_reader:
# 				# Create a dictionary for each row
# 				row_data = {field_name: value for field_name, value in zip(headers, row)}
				
# 				print(row_data["amount"])
				
# 				new_data = {}
# 				new_data["user_id"]=user.id,
# 				# new_data["time"] = row_data["step"]
# 				new_data["time"] = row_data["time"]
# 				new_data["amount"] = row_data["amount"]
# 				new_data["sender_name"] = row_data["nameOrig"]
# 				new_data["sender_old_balance"] = row_data["oldbalanceOrg"]
# 				new_data["sender_new_balance"] = row_data["newbalanceOrig"]
# 				new_data["receiver_name"] = row_data["nameDest"]
# 				new_data["receiver_old_balance"] = row_data["oldbalanceDest"]
# 				new_data["receiver_new_balance"] = row_data["newbalanceDest"]
# 				new_data["transaction_type"] = row_data["type"]
# 				new_data["is_fraud"] = row_data["isFraud"]
				
# 				trans_instance = Transaction(**new_data)
# 				db.add(trans_instance)
# 				db.commit()
# 				db.close()

# 				print("------")
				
# 				# i+=1
# 				# if i>6:
# 				# 	break

# 	except Exception as e:
# 		raise HTTPException(
# 			status_code=500,
# 			detail=f"An error occurred while saving the file: {str(e)}",
# 		)

# 	return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename})