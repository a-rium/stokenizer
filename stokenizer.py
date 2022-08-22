import sys
import dataclasses
import enum
import string

from typing import * 


QUOTES = {'"', "'", '`'}


class TokenKind(enum.Enum):
	NUMERIC = enum.auto()
	IDENTIFIER = enum.auto()
	OPERATOR = enum.auto()
	QUOTED = enum.auto()
	WHITESPACE = enum.auto()


@dataclasses.dataclass
class Token:
	text: str
	kind: str

	def unquoted(self):
		return self.text[1:len(self.text)-1]


def _is_identifier(c: str) -> bool:
	return c in string.ascii_lowercase or c in string.ascii_uppercase or c in string.digits or c == '_'


def _is_start_of_identifier(c: str) -> bool:
	return c in string.ascii_lowercase or c in string.ascii_uppercase or c == '_'
	

def _is_operator(c: str) -> bool:
	return c not in (QUOTES | {'_'}) and (c in string.punctuation or c in {'<', '>', '/'})

def _is_whitespace(c: str) -> bool:
	return c in string.whitespace


def skip_whitespaces(tokens: List[Token], current: int) -> Tuple[Token, int]:
	at = current
	while tokens[at].kind == TokenKind.WHITESPACE:
		at += 1
	return tokens[at], at


def advance(tokens: List[Token], current: int) -> Tuple[Token, int]:
	return skip_whitespaces(tokens, current + 1)


def tokenize(text: str, /, is_identifier=_is_identifier, is_operator=_is_operator, is_start_of_identifier=_is_start_of_identifier, is_whitespace=_is_whitespace) -> List[Token]:
	tokens: List[Token] = []
	at = 0
	while at < len(text):
		start = at
		while at < len(text) and is_whitespace(text[at]):
			at += 1
		if at > start:
			tokens.append(Token(text[start:at], TokenKind.WHITESPACE))
		if at >= len(text):
			break
		start = at
		if text[at] in string.digits:
			at += 1
			token_kind = TokenKind.NUMERIC
			while at < len(text) and (text[at] in string.digits or text[at] == '.'):
				at += 1
		elif text[at] in QUOTES:
			quote = text[at]
			at += 1
			token_kind = TokenKind.QUOTED
			escaped = False
			while at < len(text) and (text[at] != quote or escaped):
				if text[at] == '\\':
					escaped = not escaped
				else:
					escaped = False
				at += 1
			at += 1
		elif is_start_of_identifier(text[at]):
			at += 1
			token_kind = TokenKind.IDENTIFIER
			while at < len(text) and is_identifier(text[at]):
				at += 1
		elif is_operator(text[at]):
			at += 1
			token_kind = TokenKind.OPERATOR
		tokens.append(Token(text[start:at], token_kind))

	return tokens


def main() -> int:
	filename = sys.argv[1]
	with open(filename, 'r') as f:
		content = f.read()

	tokens = tokenize(content)
	print('\n'.join(str(it) for it in tokens))
	return 0


if __name__ == '__main__':
	raise SystemExit(main())