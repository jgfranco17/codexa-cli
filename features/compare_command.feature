Feature: Compare Command
  As a QA engineer
  I want to compare code changes and get test recommendations
  So that I can ensure proper test coverage for new changes

  Background:
    Given I have a testclerk CLI tool
    And I am in a temporary workspace
    And I have mocked external API calls

  Scenario: Compare with default settings
    When I run the command "compare"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with custom directory
    When I run the command "compare --directory /custom/path"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with custom reference branch
    When I run the command "compare --ref-branch feature-branch"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with custom output file
    When I run the command "compare --output diff_report.md"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "diff_report.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with quiet mode
    When I run the command "compare --quiet"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with all custom options
    When I run the command "compare --directory /custom/path --ref-branch main --output custom_diff.md --quiet"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "custom_diff.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with invalid output file extension
    When I run the command "compare --output report.txt"
    Then the command should exit with code 1
    And the error output should contain "Output file must be a Markdown file"

  Scenario: Compare with verbose output
    When I run the command "compare -v"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the output should contain "Recommendations for tests"

  Scenario: Compare with very verbose output
    When I run the command "compare -vv"
    Then the command should exit with code 0
    And the API key should be loaded
    And git operations should be performed
    And the OpenAI API should be called
    And a file should be created at "report.md"
    And the output should contain "Recommendations for tests"
