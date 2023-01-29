from flask import jsonify
from views import create_user, get_token, delete_all_tokens, delete_token, AdvertisementView
from errors import HttpError
from app import app

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


app.add_url_rule('/create_user/', view_func=create_user, methods=['POST'])

app.add_url_rule('/token/create/', view_func=get_token, methods=['POST'])
app.add_url_rule('/token/delete_all/', view_func=delete_all_tokens, methods=['DELETE'])
app.add_url_rule('/token/delete/', view_func=delete_token, methods=['DELETE'])

app.add_url_rule('/advertisement/', view_func=AdvertisementView.as_view('create_advertisement'), methods=['POST'])
app.add_url_rule('/advertisement/<int:adv_id>',
                 view_func=AdvertisementView.as_view('advertisement'),
                 methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run()
