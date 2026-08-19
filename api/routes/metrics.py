from flask import Blueprint, Response

from utils.metrics import get_metrics


metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/metrics", methods=["GET"])
def metrics():

    data, content_type = get_metrics()

    return Response(
        data,
        content_type=content_type
    )
