import os
import json
import requests


if __name__ == "__main__":
    with open("result.json") as f:
        test_result = json.load(f)
    max_score = float(os.environ['MAX_SCORE'])
    score = max_score * test_result['tests_ok'] / test_result['tests_count']

    test_report = {
        'score': score,
        'detail': test_result.get('stderr', 'success'),
        'accepted': test_result['tests_ok'] == test_result['tests_count'],
        'solution_id': int(os.environ['SOLUTION_ID'])
    }

    print(test_report)

    print(
        os.environ["CALLBACK_URL"],
        len(os.environ["LMS_TOKEN"]),
    )

    headers = {
        "Authorization": "Token " + os.environ["LMS_TOKEN"],
        "Content-type": "application/json",
    }
    resp = requests.post(os.environ["CALLBACK_URL"], headers=headers, json=test_report)
    print(resp.content)
    print(resp.status_code)
