from json import encoder


# noinspection PyArgumentList,PyShadowingNames,PyShadowingNames
class AsdictSupportJSONEncoder(encoder.JSONEncoder):  # xxx 標準モジュールからパクったところが警告いっぱい出る

	def iterencode(self, o, _one_shot=False):
		"""Encode the given object and yield each string
		representation as available.

		For example::

				for chunk in JSONEncoder().iterencode(bigobject):
						mysocket.write(chunk)

		"""
		if self.check_circular:
			markers = {}
		else:
			markers = None
		if self.ensure_ascii:
			_encoder = encoder.encode_basestring_ascii
		else:
			_encoder = encoder.encode_basestring

		def floatstr(o, allow_nan=self.allow_nan, _repr=float.__repr__, _inf=encoder.INFINITY, _neginf=-encoder.INFINITY):
			# Check for specials.  Note that this type of test is processor
			# and/or platform-specific, so do tests which don't depend on the
			# internals.

			if o != o:
				text = 'NaN'
			elif o == _inf:
				text = 'Infinity'
			elif o == _neginf:
				text = '-Infinity'
			else:
				return _repr(o)

			if not allow_nan:
				raise ValueError("Out of range float values are not JSON compliant: " + repr(o))

			return text

		_iterencode = _make_iterencode(
			markers, self.default, _encoder, self.indent, floatstr,
			self.key_separator, self.item_separator, self.sort_keys,
			self.skipkeys, _one_shot)

		return _iterencode(o, 0)


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingBuiltins,PyShadowingBuiltins,PyShadowingBuiltins,PyShadowingBuiltins,PyShadowingBuiltins,PyShadowingBuiltins,PyShadowingBuiltins
def _make_iterencode(markers, _default, _encoder, _indent, _floatstr, _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot,
										 ## HACK: hand-optimized bytecode; turn globals into locals
										 ValueError=ValueError,
										 dict=dict,
										 float=float,
										 id=id,
										 int=int,
										 isinstance=isinstance,
										 list=list,
										 str=str,
										 tuple=tuple,
										 _intstr=int.__str__,
										 ):  # xxx 標準モジュールからパクったところが警告いっぱい出る
	if _indent is not None and not isinstance(_indent, str):
		_indent = ' ' * _indent

	# noinspection PyArgumentList,PyUnboundLocalVariable,PyProtectedMember
	def _iterencode_list(lst, _current_indent_level):  # xxx 標準モジュールからパクったところが警告いっぱい出る
		if not lst:
			yield '[]'
			return
		if markers is not None:
			markerid = id(lst)
			if markerid in markers:
				raise ValueError("Circular reference detected")
			markers[markerid] = lst
		buf = '['
		if _indent is not None:
			_current_indent_level += 1
			newline_indent = '\n' + _indent * _current_indent_level
			separator = _item_separator + newline_indent
			buf += newline_indent
		else:
			newline_indent = None
			separator = _item_separator
		first = True
		for value in lst:
			if first:
				first = False
			else:
				buf = separator
			if isinstance(value, str):
				yield buf + _encoder(value)
			elif value is None:
				yield buf + 'null'
			elif value is True:
				yield buf + 'true'
			elif value is False:
				yield buf + 'false'
			elif isinstance(value, int):
				# Subclasses of int/float may override __str__, but we still
				# want to encode them as integers/floats in JSON. One example
				# within the standard library is IntEnum.
				yield buf + _intstr(value)
			elif isinstance(value, float):
				# see comment above for int
				yield buf + _floatstr(value)
			else:
				yield buf
				if hasattr(value, '_asdict'):
					chunks = _iterencode_dict(value._asdict(), _current_indent_level)
				elif isinstance(value, (list, tuple)):
					chunks = _iterencode_list(value, _current_indent_level)
				elif isinstance(value, dict):
					chunks = _iterencode_dict(value, _current_indent_level)
				else:
					chunks = _iterencode(value, _current_indent_level)
				yield from chunks
		if newline_indent is not None:
			_current_indent_level -= 1
			yield '\n' + _indent * _current_indent_level
		yield ']'
		if markers is not None:
			del markers[markerid]

	# noinspection PyArgumentList,PyUnboundLocalVariable,PyProtectedMember
	def _iterencode_dict(dct, _current_indent_level):  # xxx 標準モジュールからパクったところが警告いっぱい出る
		if not dct:
			yield '{}'
			return
		if markers is not None:
			markerid = id(dct)
			if markerid in markers:
				raise ValueError("Circular reference detected")
			markers[markerid] = dct
		yield '{'
		if _indent is not None:
			_current_indent_level += 1
			newline_indent = '\n' + _indent * _current_indent_level
			item_separator = _item_separator + newline_indent
			yield newline_indent
		else:
			newline_indent = None
			item_separator = _item_separator
		first = True
		if _sort_keys:
			items = sorted(dct.items(), key=lambda kv: kv[0])
		else:
			items = dct.items()
		for key, value in items:
			if isinstance(key, str):
				pass
			# JavaScript is weakly typed for these, so it makes sense to
			# also allow them.  Many encoders seem to do something like this.
			elif isinstance(key, float):
				# see comment for int/float in _make_iterencode
				key = _floatstr(key)
			elif key is True:
				key = 'true'
			elif key is False:
				key = 'false'
			elif key is None:
				key = 'null'
			elif isinstance(key, int):
				# see comment for int/float in _make_iterencode
				key = _intstr(key)
			elif _skipkeys:
				continue
			else:
				raise TypeError("key " + repr(key) + " is not a string")
			if first:
				first = False
			else:
				yield item_separator
			yield _encoder(key)
			yield _key_separator
			if isinstance(value, str):
				yield _encoder(value)
			elif value is None:
				yield 'null'
			elif value is True:
				yield 'true'
			elif value is False:
				yield 'false'
			elif isinstance(value, int):
				# see comment for int/float in _make_iterencode
				yield _intstr(value)
			elif isinstance(value, float):
				# see comment for int/float in _make_iterencode
				yield _floatstr(value)
			else:
				if hasattr(value, '_asdict'):
					chunks = _iterencode_dict(value._asdict(), _current_indent_level)
				elif isinstance(value, (list, tuple)):
					chunks = _iterencode_list(value, _current_indent_level)
				elif isinstance(value, dict):
					chunks = _iterencode_dict(value, _current_indent_level)
				else:
					chunks = _iterencode(value, _current_indent_level)
				yield from chunks
		if newline_indent is not None:
			_current_indent_level -= 1
			yield '\n' + _indent * _current_indent_level
		yield '}'
		if markers is not None:
			del markers[markerid]

	# noinspection PyArgumentList,PyUnboundLocalVariable,PyProtectedMember
	def _iterencode(o, _current_indent_level):  # xxx 標準モジュールからパクったところが警告いっぱい出る
		if isinstance(o, str):
			yield _encoder(o)
		elif o is None:
			yield 'null'
		elif o is True:
			yield 'true'
		elif o is False:
			yield 'false'
		elif isinstance(o, int):
			# see comment for int/float in _make_iterencode
			yield _intstr(o)
		elif isinstance(o, float):
			# see comment for int/float in _make_iterencode
			yield _floatstr(o)
		elif hasattr(o, '_asdict'):
			yield from _iterencode_dict(o._asdict(), _current_indent_level)
		elif isinstance(o, (list, tuple)):
			yield from _iterencode_list(o, _current_indent_level)
		elif isinstance(o, dict):
			yield from _iterencode_dict(o, _current_indent_level)
		else:
			if markers is not None:
				markerid = id(o)
				if markerid in markers:
					raise ValueError("Circular reference detected")
				markers[markerid] = o
			o = _default(o)
			yield from _iterencode(o, _current_indent_level)
			if markers is not None:
				del markers[markerid]

	return _iterencode
