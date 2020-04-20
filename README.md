# AWS Lambda functions
Serverless framework - https://serverless.com/

- deploy: `sls deploy -v`



# tests
- unit tests: `python -m pytest`

- integration tests: `sls test`
  
  `--function` - only run tests for the function specified. This requires that you've set endpoint.function
  
  `--name` - only run the test with the specified name

  test scenarios are described in the `serverless.test.yml`

