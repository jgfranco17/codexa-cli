from openai import OpenAI

from testclerk.core.errors import TestClerkGenerationError


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
            raise ValueError("API key is required")
        if not prompt:
            raise ValueError("Accessor requires setup prompt")
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
            raise TestClerkGenerationError(
                message=f"Failed to generate code: {reason}",
                help_text="Please try again re-running the command",
            )
        return content


class ReportScanner(RemoteAIAccessor):
    """Class for generating test code."""

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
