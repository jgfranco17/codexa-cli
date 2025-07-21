from openai import OpenAI

from testclerk.core.errors import TestClerkAccessorError


class RemoteAIAccessor:
    """Class for interacting with remote LLM APIs.

    Uses the DeepSeek R1 free model by default.
    """

    def __init__(
        self,
        api_key: str,
        prompt: str,
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "deepseek/deepseek-r1:free",
    ) -> None:
        if not api_key:
            raise TestClerkAccessorError("API key is required")
        if not prompt:
            raise TestClerkAccessorError("Accessor requires setup prompt")
        self.__api_key = api_key
        self.__base_url = base_url
        self.__model = model
        self.__client = OpenAI(api_key=self.__api_key, base_url=self.__base_url)
        self.__setup_prompt = prompt

    @property
    def setup_prompt(self) -> str:
        """Return the setup prompt."""
        return self.__setup_prompt

    def make_request(self, message: str, timeout: float = 60.0) -> str:
        """Make a request to the LLM API.

        Args:
            message (str): Interaction message
            timeout (float, optional): Request timeout (s), defaults to 60.0.

        Raises:
            TestClerkGenerationError: If the LLM API call fails

        Returns:
            str: LLM response text
        """
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": self.__setup_prompt},
                {"role": "user", "content": message},
            ],
            stream=False,
            timeout=timeout,
        )
        content = response.choices[0].message.content
        if not content:
            reason = response.choices[0].message.refusal
            raise TestClerkAccessorError(
                message=f"Failed to generate code: {reason}",
                help_text="Please try again re-running the command",
            )
        return content


class ReportScanner(RemoteAIAccessor):
    """Class for generating test report summary."""

    def __init__(self, api_key: str):
        self.__setup_prompt = """Take on the role of a Senior QA Engineer.

        I need to implement testing in Python. I am using Pytest as my test harness.
        Your primary task is to read the Pytest execution output and write a summary
        report.

        Key requirements:
        1. Report should be written in a way that is easy to understand.
        2. Report must provide actionable steps for fixing the issues.
        3. Report should be written in Markdown syntax, properly formatted.

        Sections that the report must include:
        1. Summary of the test run
        2. Per error, a summary of the error and the steps to fix it
        3. Any other relevant information

        Please consider:
        - Test writing best practices
        - ISTQB Tester guidelines

        From this step forward, I will provide you with the execution output and you
        will write the report. Minimize chat response, focus on the code. Provide ONLY
        the summary, not write additional comments or greetings.
        """

        super().__init__(api_key, prompt=self.__setup_prompt)

    def analyze_tests(self, test_output: str, timeout: float = 60.0) -> str:
        """Read the test execution output and generate a report.

        Args:
            test_output (str): Pytest execution output

        Returns:
            str: Generated test summary report
        """
        message = f"Generate a report for the following test output:\n\n{test_output}"
        return self.make_request(message, timeout)


class RepoAnalyzer(RemoteAIAccessor):
    """Class for analyzing the repository."""

    def __init__(self, api_key: str):
        self.__setup_prompt = """# Overview

        Take on the role of a Senior Software Engineer,
        specializing in automated testing, code review, and test strategy.

        You will be given a `git diff` between the current working tree and a remote reference
        (usually the main branch). Your task is to analyze the diff and identify what areas of
        the codebase have changed, and what testing actions are necessary based on those changes.

        Your objective is to **guide the author on what tests are required or should be updated**.

        ## Goals
        - Review the changed files and modified code in the diff.
        - Identify which functions, classes, or modules have been added, modified, or removed.
        - Detect if new logic paths, branches, conditions, or data flows are introduced.
        - Determine whether the existing tests need to be updated or if new tests should be created.
        - Recommend specific **types of tests** required (e.g., unit, integration, regression, edge cases).
        - If test files are included in the diff, comment on their adequacy and suggest improvements.
        - Flag if changes to existing test cases might break or misrepresent the new behavior.
        - If no changes in test files are detected, but logic changes exist, point out the test coverage gap.

        ## Output Format

        Respond in **Markdown** with the following sections:

        - Summary
        - Areas Requiring Tests
        - Suggested Tests
        - Risks

        Follow proper Markdownlint formatting and syntax. Ensure to add spaces after headers.
        Don't put the triple-backticks (```) in the output, format the response as if it were
        to be pasted into a Markdown file directly.

        ## Additional Notes

        - Be precise and concise; prefer bullet points where helpful.
        - Favor actionable suggestions over verbose explanations.
        - You are not writing the tests — you are identifying and planning them.
        """

        super().__init__(api_key, prompt=self.__setup_prompt)

    def compare_diff(self, diff: str, timeout: float = 60.0) -> str:
        """Assess the repository changes and generate a report.

        Args:
            diff (str): Repository changes

        Returns:
            str: Generated test summary report
        """
        message = f"Prepare an analysis and report for this diff:\n\n{diff}"
        return self.make_request(message, timeout)
