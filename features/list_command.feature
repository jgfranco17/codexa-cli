Feature: List Command
  As a QA engineer
  I want to list available tests
  So that I can see what tests are available to run

  Background:
    Given I have a testclerk CLI tool
    And I am in a temporary workspace
    And I have mocked external API calls

  Scenario: List tests with default directory
    When I run the command "list"
    Then the command should exit with code 0
    And pytest should be executed
    And the output should contain "1."

  Scenario: List tests with custom base directory
    When I run the command "list --base-dir /custom/tests"
    Then the command should exit with code 0
    And pytest should be executed
    And the output should contain "1."

  Scenario: List tests in JSON format
    When I run the command "list --json"
    Then the command should exit with code 0
    And pytest should be executed
    And the output should contain "{"
    And the output should contain "}"

  Scenario: List tests with verbose output
    When I run the command "list -v"
    Then the command should exit with code 0
    And pytest should be executed
    And the output should contain "1."

  Scenario: List tests with very verbose output
    When I run the command "list -vv"
    Then the command should exit with code 0
    And pytest should be executed
    And the output should contain "1."

  Scenario: List tests with non-existent directory
    When I run the command "list --base-dir /non/existent/path"
    Then the command should exit with code 0
    And pytest should be executed
