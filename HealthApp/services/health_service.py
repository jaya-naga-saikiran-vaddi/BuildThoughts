from flask import jsonify

from Exception.AppException import AppException
from config.logger_config import setup_logger
from repository.health_repository import HealthRepository

logger = setup_logger("MainRunner")


def validateDetails(self, health_details):
    try:

        if not health_details or 'log_date' not in health_details:
            logger.error("Invalid health details received: %s", health_details)
            raise AppException(f"Invalid health details received ", 409)

        log_date = health_details['log_date']

        result = self.repo.validateDate(log_date)

        if result and result[0] > 0:
            logger.warning("Duplicate entry attempted for date: %s", log_date)
            raise Exception(f"Entry already exists for date: {log_date}")
    except AppException as ae:
        raise ae
    except Exception as e:
        logger.exception("Error occurred while validating health details: %s", str(e))
        raise Exception(str(e))


class HealthService:
    def __init__(self):
        self.repo = HealthRepository()

    def saveHealthInfo(self, healthDetails):
        try:
            validateDetails(self, healthDetails)
            self.repo.saveHealthInfo(healthDetails)
            return {"message": "Entry created successfully"}, 201
        except Exception as e:
            logger.error("Error occurred in saving health info :", e)
            return jsonify({"error": str(e)}), 400

    def fetch_all_health_info(self):
        entries = self.repo.fetch_all_health_info()
        return entries

    def fetch_health_info_by_data(self, date):
        entry = self.repo.fetch_health_info_by_date(date)
        if entry:
            return entry
        return {"message": "No entry found"}, 404

    def update_health_info(self, date, data):
        self.repo.update_health_info(date, data)
        return {"message": "Entry updated successfully"}

    def delete_health_info(self, date):
        try:
            self.repo.delete_health_info(date)
            return {"message": "Entry deleted successfully"}
        except Exception as e:
            logger.error("Error occurred in saving health info :", e)
            raise Exception("Unable to save Health info")

    def getLast5DaysSummary(self):
        return self.repo.fetchLast5DaysSummary()
