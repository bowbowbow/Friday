from flask import Flask
from flask import request, Response, g
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
    code = api_call_main(sample, pathsaver, run_selenium, nlp, allennlp)
    print(code)

    return json.dumps({'code': code})


if __name__ == '__main__':
    run_selenium, use_corenlp, pathsaver, nlp, allennlp = get_api_daemon_object()
    app.run(host='0.0.0.0', debug=False, port=8081)
