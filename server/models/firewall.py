"""
Models for the Firewall API
"""

from typing import Optional
from pydantic import BaseModel, Field, Json

from config.settings import settings

class SourceRequest(BaseModel):
	"""
	Request model for add source
	"""

	source_address: str = Field(..., description="Source address to add")

class SourceResponse(BaseModel):
	"""
	Response model for add source
	"""

	output: str = Field(..., description="Response from firewall for adding/removing source address in zone")