from flask_api import status
from flask_restful import Resource

from managers.statistics import StatisticsManager


class GeneralStatsResource(Resource):
    def get(self):
        user_stats = StatisticsManager.get_users_stats()
        resource_stats = StatisticsManager.get_resources_stats()
        tag_stats = StatisticsManager.get_tags_stats()
        return {"messages": "Below are the most recent statistics from our database \N{slightly smiling face}"
                , "user_stats": user_stats
                , "resource_stats": resource_stats
                , "tag_stats": tag_stats}, status.HTTP_200_OK