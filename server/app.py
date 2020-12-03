
from flask import Flask, request, abort
from data_service import process_csvs
from core.game_scheduler import schedule

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/schedules', methods=["GET", "POST"])
def schedule_games():
    if request.method == "POST":
        if 'game_data' not in request.files:
            app.logger.error('No file part')
            abort(400, "Missing file for upload")
        squads_by_date, matches, squad_preferences = \
            process_csvs(request.files.getlist('game_data'))
        schedule(squads_by_date, matches)
        return {
            "success_upload": True,
            "collectors_test": str(squads_by_date.loc[0]['Total']),
            "matches_test": str(matches.loc[0]['Competition'])
            }

if __name__ == '__main__':
    app.run()
