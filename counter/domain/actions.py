from io import BytesIO
from typing import List

from PIL import Image

from counter.debug import draw
from counter.domain.models import CountResponse, Prediction
from counter.domain.ports import ObjectCountRepo, ObjectDetector
from counter.domain.predictions import count, over_threshold


class CountDetectedObjects:
    """Count detected objects."""

    def __init__(
        self, object_detector: ObjectDetector, object_count_repo: ObjectCountRepo
    ):
        self.__object_detector = object_detector
        self.__object_count_repo = object_count_repo

    def execute(self, image: BytesIO, threshold: float) -> CountResponse:
        """Detect and count the objects in a given image above threshold.

        Parameters
        ----------
        image : BytesIO
            Image for object count.
        threshold : float
            Model prediction score threshold.

        Returns
        -------
        CountResponse
            Given image objects count and total objects count till now.
        """
        predictions = self.__find_valid_predictions(image, threshold)
        object_counts = count(predictions)
        self.__object_count_repo.update_values(object_counts)
        total_objects = self.__object_count_repo.read_values()
        return CountResponse(current_objects=object_counts, total_objects=total_objects)

    def __find_valid_predictions(self, image, threshold):
        predictions = self.__object_detector.predict(image)
        self.__debug_image(image, predictions, "all_predictions.jpg")
        valid_predictions = list(over_threshold(predictions, threshold=threshold))
        self.__debug_image(
            image,
            valid_predictions,
            f"valid_predictions_with_threshold_{threshold}.jpg",
        )
        return valid_predictions

    @staticmethod
    def __debug_image(image, predictions, image_name):
        if __debug__ and image is not None:
            image = Image.open(image)
            draw(predictions, image, image_name)


class DetectObjects:
    """Object detection."""

    def __init__(self, object_detector: ObjectDetector):
        self.__object_detector = object_detector

    def execute(self, image: BytesIO, threshold: float) -> List[Prediction]:
        """Object detection.

        Parameters
        ----------
        image : BytesIO
            Image for object detection.
        threshold : float
            Model prediction score threshold.

        Returns
        -------
        List[Prediction]
            Detected objects.
        """
        return self.__find_valid_predictions(image, threshold)

    def __find_valid_predictions(self, image, threshold):
        predictions = self.__object_detector.predict(image)
        self.__debug_image(image, predictions, "all_predictions.jpg")
        valid_predictions = list(over_threshold(predictions, threshold=threshold))
        self.__debug_image(
            image,
            valid_predictions,
            f"valid_predictions_with_threshold_{threshold}.jpg",
        )
        return valid_predictions

    @staticmethod
    def __debug_image(image, predictions, image_name):
        if __debug__ and image is not None:
            image = Image.open(image)
            draw(predictions, image, image_name)
