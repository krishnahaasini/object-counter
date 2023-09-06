from flask_restx import Api, fields, reqparse
from werkzeug.datastructures.file_storage import FileStorage

api = Api(
    version="1.0",
    title="Object Detection API",
    description="A simple object detection API",
)

object_detection_request = reqparse.RequestParser()
object_detection_request.add_argument("file", type=FileStorage, location="files")
object_detection_request.add_argument(
    "threshold", type=float, default=0.5, location="form"
)

object_count = api.model(
    "Object Count",
    {
        "count": fields.Integer(description="Object count"),
        "object_class": fields.String(description="Object class name"),
    },
)
count_response = api.model(
    "Object Count Response",
    {
        "current_objects": fields.List(fields.Nested(object_count)),
        "total_objects": fields.List(fields.Nested(object_count)),
    },
)
box = api.model(
    "Box",
    {
        "xmax": fields.Float,
        "xmin": fields.Float,
        "ymax": fields.Float,
        "ymin": fields.Float,
    },
)
prediction = api.model(
    "Prediction",
    {"class_name": fields.String, "score": fields.Float, "box": fields.Nested(box)},
)
