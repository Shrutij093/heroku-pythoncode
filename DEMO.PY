from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# define the search API endpoint
@app.route('/search')
def search_comments():
    # parse the search parameters from the request URL
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    # construct the query string for the existing API
    query_params = {
        'author': search_author,
        'at_from': at_from,
        'at_to': at_to,
        'like_from': like_from,
        'like_to': like_to,
        'reply_from': reply_from,
        'reply_to': reply_to
    }
    query_string = '&'.join([f'{k}={v}' for k, v in query_params.items()])
    api_url = f'https://dev.ylytic.com/ylytic/test?{query_string}'

    # send a request to the existing API
    response = requests.get(api_url)

    # parse the response and filter the comments based on the search parameters
    comments = response.json()
    filtered_comments = []
    for comment in comments:
        if (not search_author or search_author in comment['author']) and \
           (not at_from or comment['at'] >= at_from) and \
           (not at_to or comment['at'] <= at_to) and \
           (not like_from or comment['like'] >= int(like_from)) and \
           (not like_to or comment['like'] <= int(like_to)) and \
           (not reply_from or comment['reply'] >= int(reply_from)) and \
           (not reply_to or comment['reply'] <= int(reply_to)) and \
           (not search_text or search_text in comment['text']):
            filtered_comments.append(comment)

    # return the filtered comments as a JSON response
    return jsonify(filtered_comments)

if __name__ == '__main__':
    app.run(debug=True)