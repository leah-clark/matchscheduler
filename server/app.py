from flask import Flask, request, abort
from data_service import process_csvs
from core.scheduler import save_schedule

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/schedules', methods=["GET", "POST"])
def schedule_games():
    if request.method == "POST":
        if 'game_data' not in request.files:
            app.logger.error('No file part')
            abort(400, "Missing file for upload")
        matches_df, squad_preferences, squads_df, competitions = \
            process_csvs(request.files.getlist('game_data'))
        path = save_schedule(matches_df, squad_preferences, squads_df, competitions)
        # todo: remove the hardcoded paths here
        return {
            "schedule": str(path) + "/schedule.csv",
            "unfinished": str(path) + "/unfinished.csv"
        }


if __name__ == '__main__':
    app.run()
