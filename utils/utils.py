from flask import jsonify


def customResponse(response, status_code=200):
    return jsonify({"result": response}), status_code

# FIXME Function to validate member class instance input fields
# return error or data
# def validateMember():
