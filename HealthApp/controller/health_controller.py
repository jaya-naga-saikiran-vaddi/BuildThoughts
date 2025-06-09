from flask import Blueprint, request, jsonify, render_template

from aiAnalysis import get_gpt_advice
from services.health_service import HealthService  # your service module

health_bp = Blueprint('health_bp', __name__)
service = HealthService()


@health_bp.route('', methods=['POST'])
def saveHealthInfo():
    return service.saveHealthInfo(request.get_json())


@health_bp.route('', methods=['GET'])
def fetch_all_health_info():
    data = service.fetch_all_health_info()
    return jsonify(data)


@health_bp.route('/<date>', methods=['GET'])
def fetch_health_info_by_data(date):
    return service.fetch_health_info_by_data(date)


@health_bp.route('/<date>', methods=['PUT'])
def update_health_info(date):
    return service.update_health_info(date, request.get_json())


@health_bp.route('/<date>', methods=['DELETE'])
def delete_health_info(date):
    return service.delete_health_info(date)


@health_bp.route('/health/info/summary', methods=['GET'])
def get_summary():
    print("Summary endpoint called")
    data = service.getLast5DaysSummary()
    if not data:
        print("No data found")
        return jsonify({"message": "No summary available"}), 404
    print(f"Returning data: {data}")
    return jsonify(data)


@health_bp.route("/all", methods=['GET'])
def show_all_entries():
    return render_template("all_entries.html")


@health_bp.route('/health/ai/advice', methods=['GET'])
def health_advice():

    summary_stats = service.fetch_all_health_info()

    if not summary_stats:
        return jsonify({"error": "No health summary data found"}), 404

    advice = get_gpt_advice(summary_stats)
    return jsonify({"advice": advice})
