from openai import OpenAI

from testclerk.core.errors import TestClerkGenerationError


class ReportScanner:
    """Class for generating test code."""

    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__base_url = "https://openrouter.ai/api/v1"
        self.__model = "deepseek/deepseek-r1:free"
        self.__client = OpenAI(api_key=self.__api_key, base_url=self.__base_url)
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

    def analyze_tests(self, test_output: str, timeout: float = 60.0) -> str:
        """Read the test execution output and generate a report.

        Args:
            test_output (str): Pytest execution output

        Raises:
            CLIGenerationError: If LLM API call fails

        Returns:
            str: Generated test summary report
        """
        message = f"Generate a report for the following test output:\n\n{test_output}"
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
            raise TestClerkGenerationError(
                message=f"Failed to generate code: {reason}",
                help_text="Please try again re-running the command",
            )
        return content
