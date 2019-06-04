from flask import Flask
from flask import request
import json

from language_parser import get_api_daemon_object, api_call_main

app = Flask(__name__)


@app.route('/text2selenium', methods=['POST'])
def text2selenium():
    data = request.get_json()
    text = data['text']
    selectors = data['selectors']

    sample = {
        'text': text,
        'selectors': selectors,
    }

    result = {'code': '', 'error': ''}
    try:
        code = api_call_main(sample, pathsaver, run_selenium, nlp, allennlp)
        result['code'] = code
    except Exception as err:
        result['error'] = str(err)

    return json.dumps(result)


if __name__ == '__main__':
    run_selenium, use_corenlp, pathsaver, nlp, allennlp = get_api_daemon_object()
    app.run(host='0.0.0.0', debug=True, port=8081)
