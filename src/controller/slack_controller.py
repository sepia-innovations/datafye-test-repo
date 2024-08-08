import logging
from fastapi import APIRouter, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.slack_service import SlackService
from models.add_users_request import AddUserToChannelRequest
from models.create_channel_request import CreateChannelRequest
from models.post_message_request import PostMessageRequest
from models.set_owner_request import SetOwnerRequest


# Create an APIRouter instance
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SlackController:
    def __init__(self, logger):
        self.logger = logger
        self.slack_service = SlackService(logger)

        self.logger.info("Initialized slack controller")
    

# Instantiate the controller
slack_controller = SlackController(logger)


async def create_json_response(status_code: int, response: dict) -> JSONResponse:
    json_encode_response = jsonable_encoder(response)
    return JSONResponse(content=json_encode_response, media_type="application/json", status_code=status_code)


@router.post("/create_channel")
async def create_channel(request: CreateChannelRequest):
    logger.info(f"Received request to create channel - Payload: {request}, Headers: {Header}")

    status_code, response = await slack_controller.slack_service.create_channel(request)

    return await create_json_response(status_code, response)


@router.post("/channel/{channel_id}/set_owner")
async def set_channel_owner(channel_id: str, request: SetOwnerRequest):
    logger.info(f"Received request to set channel owner - Channel: {channel_id}, Payload: {request}, Headers: {Header}")

    status_code, response = await slack_controller.slack_service.set_channel_owner(channel_id, request)

    return await create_json_response(status_code, response)


@router.post("/channel/{channel_id}/users/add")
async def add_users_to_channel(channel_id: str, request: AddUserToChannelRequest):
    logger.info(f"Received request to add users to channel - Channel: {channel_id}, Payload: {request}, Headers: {Header}")

    status_code, response = await slack_controller.slack_service.add_users_to_channel(channel_id, request)

    return await create_json_response(status_code, response)


@router.post("/channel/{channel_id}/post_message")
async def post_message_on_channel(channel_id: str, request: PostMessageRequest):
    logger.info(f"Received request to post message on channel - Channel: {channel_id}, Payload: {request}, Headers: {Header}")

    status_code, response =  await slack_controller.slack_service.post_message_on_channel(channel_id, request)

    return await create_json_response(status_code, response)
