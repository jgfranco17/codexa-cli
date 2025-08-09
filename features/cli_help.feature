Feature: CLI Help and Version
  As a user
  I want to see help information and version details
  So that I can understand how to use the tool

  Background:
    Given I have a testclerk CLI tool
    And I am in a temporary workspace
    And I have mocked external API calls

  Scenario: Show main help
    When I run the command "--help"
    Then the command should exit with code 0
    And the output should contain "TestClerk: CLI tool for test automation assistance"
    And the output should contain "run"
    And the output should contain "list"
    And the output should contain "compare"

  Scenario: Show version
    When I run the command "--version"
    Then the command should exit with code 0
    And the output should contain "version 0.0.1"

  Scenario: Show run command help
    When I run the command "run --help"
    Then the command should exit with code 0
    And the output should contain "Analyze the contents of a file for testing"
    And the output should contain "--output"
    And the output should contain "--quiet"

  Scenario: Show list command help
    When I run the command "list --help"
    Then the command should exit with code 0
    And the output should contain "List all available tests"
    And the output should contain "--base-dir"
    And the output should contain "--json"

  Scenario: Show compare command help
    When I run the command "compare --help"
    Then the command should exit with code 0
    And the output should contain "Generate smart analysis from diff comparison"
    And the output should contain "--directory"
    And the output should contain "--ref-branch"
    And the output should contain "--output"
    And the output should contain "--quiet"

  Scenario: Show verbose help
    When I run the command "--help -v"
    Then the command should exit with code 0
    And the output should contain "TestClerk: CLI tool for test automation assistance"
    And the output should contain "run"
    And the output should contain "list"
    And the output should contain "compare"

  Scenario: Show very verbose help
    When I run the command "--help -vv"
    Then the command should exit with code 0
    And the output should contain "TestClerk: CLI tool for test automation assistance"
    And the output should contain "run"
    And the output should contain "list"
    And the output should contain "compare"
