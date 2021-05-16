from ..models import Msg, User
from app import db
from flask import request, make_response, jsonify
from loguru import logger


class MsgController:
    @staticmethod
    def new_msg(body):

        logger.info(f"_uuid {body['_uuid']}")
        logger.info(f"state {body['state']}")
        logger.info(f"message {body['message']}")
        logger.info(f"user_from {body['user_from']}")
        logger.info(f"user_to {body['user_to']}")




        try:
            _uuid = body['_uuid']
            state = body['state']
            message = body['message']
            user_from = body['user_from']
            user_to = body['user_to']
            msg = Msg(_uuid=_uuid, message=message, user_from=user_from, user_to=user_to, state=state)

        except Exception as e:
            logger.info(f'lol {e}')
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    "meta": {"status": "error"},
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = None

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    db.session.add(msg)
                    db.session.commit()
                    return make_response({
                        "meta": {"status": "Saved"},
                        "msg": msg.serialize()
                    }), 200

                except Exception as e:
                    return {
                               "meta": {"status": "error"},
                               "error": f'Try again. {e}'
                           }, 500

            responseObject = {
                "meta": {"status": "error"},
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
