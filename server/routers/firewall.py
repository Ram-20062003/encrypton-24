import subprocess
import shlex

from fastapi import APIRouter, HTTPException, status

from config.settings import settings
from config.dependencies import restart_docker, restart_firewalld

from server.models.exceptions import GenericError, SuccessResponse
from server.models.firewall import SourceRequest, SourceResponse

router = APIRouter(
	prefix="/firewall",
	tags=["firewall"],
)

#Add source address to blacklist
@router.post("/add-source-blklst",
			 responses={
				 status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": GenericError},
				 status.HTTP_201_CREATED: {"model": SourceResponse},
			 })
async def addSourceBlk(request: SourceRequest) -> SourceResponse:
	"""
	Execute add source address to blacklist request
	"""
	try:
		if "/0" in request.source_address:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Addess with /0 should not be added to blacklist",
			)
		
		process = subprocess.Popen(f"""echo {shlex.quote(str(settings.sudo_passwd))} | sudo -p '' -S firewall-cmd \
						 --permanent \
						 --zone={shlex.quote(str(settings.dploy_blacklist_zone))} \
						 --add-source={shlex.quote(str(request.source_address))} && \
						 echo {shlex.quote(str(settings.sudo_passwd))} | sudo -p '' -S firewall-cmd --complete-reload""",
						 shell=True,
						 stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE)
		
		_, error = process.communicate()
		if error and "ALREADY_ENABLED" not in error.decode('utf-8'):
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail=error.decode('utf-8'),
			)

		restart_docker()
		restart_firewalld()

	except OSError as exception:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error adding source {request.source_address} - {exception.strerror.decode('utf-8')}",
		)
	return SourceResponse(output=f"Source {request.source_address} added to blacklist successfully")

#Remove source address from blacklist
@router.post("/remove-source-blklst",
			 responses={
				 status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": GenericError},
				 status.HTTP_200_OK: {"model": SourceResponse},
			 })
async def removeSourceBlk(request: SourceRequest) -> SourceResponse:
	"""
	Execute remove source address from blacklist request
	"""
	try:
		process = subprocess.Popen(f"""echo {shlex.quote(str(settings.sudo_passwd))} | sudo -p '' -S firewall-cmd \
						 --permanent \
						 --zone={shlex.quote(str(settings.dploy_blacklist_zone))} \
						 --remove-source={shlex.quote(str(request.source_address))} && \
						 echo {shlex.quote(str(settings.sudo_passwd))} | sudo -p '' -S firewall-cmd --complete-reload""",
						 shell=True,
						 stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE)
		
		_, error = process.communicate()
		if error and "NOT_ENABLED" not in error.decode('utf-8'):
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail=error.decode('utf-8'),
			)
	
		restart_docker()
		restart_firewalld()
		
	except OSError as exception:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error removing source {request.source_address} from blacklist - {exception.strerror.decode('utf-8')}",
		)
	return SourceResponse(output=f"Source {request.source_address} removed from blacklist successfully")
