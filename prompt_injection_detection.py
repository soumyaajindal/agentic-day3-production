import re
from typing import Final


INJECTION_PATTERNS: Final[list[str]] = [
	r"ignore (your |all |previous )?instructions",
	r"system prompt.*disabled",
	r"new role",
	r"repeat.*system prompt",
	r"jailbreak",
]


def detect_injection(user_input: str) -> bool:
	"""Return True if the input looks like a prompt injection attempt."""
	text = user_input.lower()
	for pattern in INJECTION_PATTERNS:
		if re.search(pattern, text):
			return True
	return False