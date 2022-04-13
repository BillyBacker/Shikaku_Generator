import json
import requests


generator_url = 'http://localhost:9001/'
solver_url = 'http://localhost:9000/'
strategies = ['breath-first-search', 'depth-first-search']

BOARD_SIZE = (5, 5)
RATIO = 0.5
NUMBER_OF_TESTS = 1

res = requests.get(f'{generator_url}{BOARD_SIZE[0]}-{BOARD_SIZE[1]}/{RATIO}')

game = res.json()

test_request = {'gameState': {**game}, 'n': NUMBER_OF_TESTS}
for strategy in strategies:
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res2 = requests.post(f'{solver_url}test-{strategy}', data=json.dumps(test_request), headers=headers)

    test_result = {'type': strategy, **res2.json()}
    print(res2.json())
    with open(f'test_result_{strategy}', 'w') as fp:
        json.dump(test_result, fp, indent=4) 
print('FINISHED')