Feature: Run Command
  As a QA engineer
  I want to run tests and generate reports
  So that I can analyze test results and get actionable insights

  Background:
    Given I have a testclerk CLI tool
    And I am in a temporary workspace
    And I have mocked external API calls

  Scenario: Run tests with default output
    When I run the command "run"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the file "report.md" should contain "Test Report"

  Scenario: Run tests with custom output file
    When I run the command "run --output custom_report.md"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "custom_report.md"
    And the file "custom_report.md" should contain "Test Report"

  Scenario: Run tests with quiet mode
    When I run the command "run --quiet"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "report.md"

  Scenario: Run specific test IDs
    When I run the command "run test_file.py::test_function"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "report.md"

  Scenario: Run multiple test IDs
    When I run the command "run test1.py test2.py::test_function"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "report.md"

  Scenario: Run with invalid output file extension
    When I run the command "run --output report.txt"
    Then the command should exit with code 2
    And the error output should contain "Output file must be a Markdown file"

  Scenario: Run with verbose output
    When I run the command "run -v"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "report.md"

  Scenario: Run with very verbose output
    When I run the command "run -vv"
    Then the command should exit with code 0
    And the API key should be loaded
    And pytest should be executed
    And the OpenAI API should be called
    And a file should be created at "report.md"
