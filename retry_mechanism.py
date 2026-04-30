from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from enum import Enum, auto
from circuit_breaker import CircuitBreaker
import time

load_dotenv()

llm = ChatOpenAI(model ="gpt-4o-mini", temperature=0)


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

breaker = CircuitBreaker()

def guarded_invoke(messages: list) -> InvocationResult:
	if not breaker.allow_request():
		return InvocationResult(
			success=False,
			error="Circuit breaker open",
			error_category=ErrorCategory.UNKNOWN,
			attempts=0,
		)

	result = production_invoke(messages)
	if result.success:
		breaker.record_success()
	else:
		breaker.record_failure()
	return result

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