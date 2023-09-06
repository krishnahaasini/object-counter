from io import BytesIO

from flask import Flask
from flask_restx import Resource

from counter import config
from counter.entrypoints.models import (
    api,
    count_response,
    object_detection_request,
    prediction,
)

app = Flask(__name__)
app.config["RESTX_MASK_SWAGGER"] = False
api.init_app(app)

ns = api.namespace("", description="Object detection and count operations")


count_action = config.get_count_action()
detection_action = config.get_detection_action()


def get_request_data(object_detection_request) -> tuple[BytesIO, float]:
    """Get image and threshold from request data.

    Returns
    -------
    tuple[BytesIO, float]
        Image and threshold.
    """
    args = object_detection_request.parse_args()
    uploaded_file = args["file"]
    threshold = float(args["threshold"])
    image = BytesIO()
    uploaded_file.save(image)
    return image, threshold


@ns.route("/object-count")
class ObjectCount(Resource):
    @ns.expect(object_detection_request)
    @ns.marshal_with(count_response)
    def post(self):
        image, threshold = get_request_data(object_detection_request)
        count_response = count_action.execute(image, threshold)
        return count_response


@ns.route("/object-detection")
class ObjectDetection(Resource):
    @ns.expect(object_detection_request)
    @ns.marshal_with(prediction, as_list=True)
    def post(self):
        image, threshold = get_request_data(object_detection_request)
        detection_response = detection_action.execute(image, threshold)
        return detection_response


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
