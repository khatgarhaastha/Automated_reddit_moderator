from lambda_function import lambda_handler, fetch_items_from_dynamodb, parse_nsfw_sfw

# test 1 
def test_lambda_handler():
    event = {}
    context = {}
    assert lambda_handler(event, context) == {
        'statusCode': 200,
        'body': 'NSFW/SFW classification completed!'
    }

# test 2
def test_fetch_items_from_dynamodb():
    table_name = 'reddit-submissions'
    items = fetch_items_from_dynamodb(table_name)
    assert  len(items) > 0
    assert type(items) == list

# test 3
def test_parse_nsfw_sfw():
    submissions = [
        {
            'submission_text': 'This is a test submission'
        }
    ]
    result = parse_nsfw_sfw(submissions)
    assert len(result) == 1
    assert 'nsfw_tags' in result[0]



# Run the tests
test_lambda_handler()
test_fetch_items_from_dynamodb()
test_parse_nsfw_sfw()
print("All tests passed!")


