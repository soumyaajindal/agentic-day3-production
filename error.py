from dataclasses import dataclass
from enum import Enum, auto
import time


class ErrorCategory(str, Enum):
	RATE_LIMIT = "RATE_LIMIT"
	TIMEOUT = "TIMEOUT"
	CONTEXT_OVERFLOW = "CONTEXT_OVERFLOW"
	AUTH_ERROR = "AUTH_ERROR"
	UNKNOWN = "UNKNOWN"


@dataclass
class InvocationResult:
	success: bool
	content: str = ""
	error: str = ""
	error_category: ErrorCategory = ErrorCategory.UNKNOWN
	attempts: int = 0


def production_invoke(messages: list, max_retries: int = 3) -> InvocationResult:
	attempts = 0
	while attempts < max_retries:
		attempts += 1
		try:
			# replace with your own LLM/graph call
			response = llm.invoke(messages)
			return InvocationResult(
				success=True,
				content=response.content,
				attempts=attempts,
			)
		except Exception as e:  # replace with real SDK errors if you want
			message = str(e).lower()
			if "rate limit" in message:
				delay = 2 ** attempts  # 2s, 4s, 8s
				time.sleep(delay)
				continue
			if "context_length" in message or "maximum context length" in message:
				return InvocationResult(
					success=False,
					error=str(e),
					error_category=ErrorCategory.CONTEXT_OVERFLOW,
					attempts=attempts,
				)
			# fall-through for other errors
			return InvocationResult(
				success=False,
				error=str(e),
				error_category=ErrorCategory.UNKNOWN,
				attempts=attempts,
			)

	return InvocationResult(
		success=False,
		error="Max retries exceeded",
		error_category=ErrorCategory.RATE_LIMIT,
		attempts=attempts,
	)