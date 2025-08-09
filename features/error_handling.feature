Feature: Error Handling
  As a QA engineer
  I want the tool to handle errors gracefully
  So that I can understand what went wrong and how to fix it

  Background:
    Given I have a testclerk CLI tool
    And I am in a temporary workspace
    And I have mocked external API calls

  Scenario: Handle OpenAI API errors
    Given the OpenAI API returns an error
    When I run the command "run"
    Then the command should fail with error
    And the API error should be handled gracefully

  Scenario: Handle invalid API key
    Given the API key is invalid
    When I run the command "run"
    Then the command should fail with error
    And the invalid API key should be detected

  Scenario: Handle pytest execution failure
    Given pytest execution fails
    When I run the command "run"
    Then the command should fail with error
    And the pytest failure should be reported

  Scenario: Handle git operation failure
    Given git operations fail
    When I run the command "compare"
    Then the command should fail with error
    And the git operation failure should be handled

  Scenario: Handle invalid command arguments
    When I run an invalid command
    Then the command should fail with error
    And the error message should contain "No such command"

  Scenario: Handle missing required arguments
    When I run a command with missing required arguments
    Then the command should fail with error
    And the error message should contain "Error"

  Scenario: Handle invalid output file format for run command
    When I run the command "run --output report.txt"
    Then the command should fail with error
    And the error message should contain "Output file must be a Markdown file"

  Scenario: Handle invalid output file format for compare command
    When I run the command "compare --output report.txt"
    Then the command should fail with error
    And the error message should contain "Output file must be a Markdown file"

  Scenario: Handle non-existent test files
    When I run the command "run non_existent_test.py"
    Then the command should fail with error
    And the pytest failure should be reported

  Scenario: Handle non-existent directory for list command
    When I run the command "list --base-dir /non/existent/path"
    Then the command should exit with code 0
    And pytest should be executed
