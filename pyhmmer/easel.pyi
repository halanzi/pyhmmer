# coding: utf-8
import abc
import array
import collections.abc
import os
import sys
import types
import typing

# --- Alphabet ---------------------------------------------------------------

class Alphabet(object):
    @classmethod
    def dna(self) -> Alphabet: ...
    @classmethod
    def rna(self) -> Alphabet: ...
    @classmethod
    def amino(self) -> Alphabet: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __reduce__(self) -> typing.Tuple[typing.Callable[[], Alphabet], typing.Tuple[()]]: ...
    def __sizeof__(self) -> int: ...
    @property
    def K(self) -> int: ...
    @property
    def Kp(self) -> int: ...
    @property
    def symbols(self) -> str: ...

# --- Bitfield ---------------------------------------------------------------

class Bitfield(typing.Sequence[bool]):
    def __init__(self, length: int) -> None: ...
    def __len__(self) -> int: ...
    @typing.overload
    def __getitem__(self, index: int) -> bool: ...
    @typing.overload
    def __getitem__(self, index: slice) -> typing.Sequence[bool]: ...
    def __setitem__(self, index: int, value: bool) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> typing.Dict[str, object]: ...
    def __setstate__(self, state: typing.Dict[str, object]) -> None: ...
    def __sizeof__(self) -> int: ...
    def count(self, value: bool = True) -> int: ...
    def toggle(self, index: int) -> None: ...

# --- KeyHash ----------------------------------------------------------------

class KeyHash(typing.Mapping[bytes, int]):
    def __init__(self) -> None: ...
    def __copy__(self) -> KeyHash: ...
    def __len__(self) -> int: ...
    def __contains__(self, value: object) -> bool: ...
    def __getitem__(self, item: bytes) -> int: ...
    def __iter__(self) -> typing.Iterator[bytes]: ...
    def __getstate__(self) -> typing.Dict[str, object]: ...
    def __setstate__(self, state: typing.Dict[str, object]) -> None: ...
    def __sizeof__(self) -> int: ...
    def clear(self) -> None: ...
    def copy(self) -> KeyHash: ...

# --- Matrix & Vector --------------------------------------------------------

_T = typing.TypeVar("_T")
_V = typing.TypeVar("_V")
_M = typing.TypeVar("_M")

class Vector(typing.Sequence[_T], typing.Generic[_T], abc.ABC):
    def __reduce__(self: _V) -> typing.Tuple[typing.Type[_V], typing.Tuple[array.array[typing.Any]]]: ...
    @abc.abstractmethod
    @classmethod
    def zeros(cls: typing.Type[_V], n: int) -> _V: ...
    @abc.abstractmethod
    def __init__(self, iterable: typing.Collection[_T]): ...
    def __copy__(self: _V) -> _V: ...
    @abc.abstractmethod
    def __eq__(self, other: object) -> bool: ...
    @typing.overload
    @abc.abstractmethod
    def __getitem__(self, index: int) -> _T: ...
    @typing.overload
    @abc.abstractmethod
    def __getitem__(self, index: slice) -> Vector[_T]: ...
    @typing.overload
    @abc.abstractmethod
    def __setitem__(self, index: int, value: _T) -> None: ...
    @typing.overload
    @abc.abstractmethod
    def __setitem__(self, index: slice, value: _T) -> None: ...
    @abc.abstractmethod
    def __iadd__(self: _V, other: typing.Union[_T, _V]) -> _V: ...
    @abc.abstractmethod
    def __imul__(self: _V, other: typing.Union[_T, _V]) -> _V: ...
    @abc.abstractmethod
    def __matmul__(self: _V, other: _V) -> _T: ...
    def __sizeof__(self) -> int: ...
    def __repr__(self) -> str: ...
    def __len__(self) -> int: ...
    @property
    def shape(self) -> typing.Tuple[int]: ...
    @property
    def strides(self) -> typing.Tuple[int]: ...
    @property
    @abc.abstractmethod
    def itemsize(self) -> int: ...
    @property
    @abc.abstractmethod
    def format(self) -> str: ...
    @abc.abstractmethod
    def argmax(self) -> int: ...
    @abc.abstractmethod
    def argmin(self) -> int: ...
    @abc.abstractmethod
    def copy(self: _V) -> _V: ...
    @abc.abstractmethod
    def max(self) -> _T: ...
    @abc.abstractmethod
    def min(self) -> _T: ...
    @abc.abstractmethod
    def reverse(self) -> None: ...
    @abc.abstractmethod
    def sum(self) -> _T: ...

class VectorF(Vector[float]):
    @classmethod
    def zeros(cls, n: int) -> VectorF: ...
    def __init__(self, iterable: typing.Optional[typing.Collection[float]] = None): ...
    def __copy__(self) -> VectorF: ...
    def __eq__(self, other: object) -> bool: ...
    @typing.overload
    def __getitem__(self, index: int) -> float: ...
    @typing.overload
    def __getitem__(self, index: slice) -> VectorF: ...
    @typing.overload
    def __setitem__(self, index: int, value: float) -> None: ...
    @typing.overload
    def __setitem__(self, index: slice, value: float) -> None: ...
    def __iadd__(self, other: typing.Union[float, VectorF]) -> VectorF: ...
    def __imul__(self, other: typing.Union[float, VectorF]) -> VectorF: ...
    def __matmul__(self, other: VectorF) -> float: ...
    def argmax(self) -> int: ...
    def argmin(self) -> int: ...
    def copy(self) -> VectorF: ...
    def max(self) -> float: ...
    def min(self) -> float: ...
    def normalize(self) -> None: ...
    def reverse(self) -> None: ...
    def sum(self) -> float: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def format(self) -> str: ...

class VectorU8(Vector[int]):
    @classmethod
    def zeros(cls, n: int) -> VectorU8: ...
    def __init__(self, iterable: typing.Optional[typing.Collection[int]] = None): ...
    def __copy__(self) -> VectorU8: ...
    def __eq__(self, other: object) -> bool: ...
    @typing.overload
    def __getitem__(self, index: int) -> int: ...
    @typing.overload
    def __getitem__(self, index: slice) -> VectorU8: ...
    @typing.overload
    def __setitem__(self, index: int, value: int) -> None: ...
    @typing.overload
    def __setitem__(self, index: slice, value: int) -> None: ...
    def __iadd__(self, other: typing.Union[int, VectorU8]) -> VectorU8: ...
    def __imul__(self, other: typing.Union[int, VectorU8]) -> VectorU8: ...
    def __matmul__(self, other: VectorU8) -> int: ...
    def argmax(self) -> int: ...
    def argmin(self) -> int: ...
    def copy(self) -> VectorU8: ...
    def max(self) -> int: ...
    def min(self) -> int: ...
    def reverse(self) -> None: ...
    def sum(self) -> int: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def format(self) -> str: ...

class Matrix(typing.Sequence[Vector[_T]], typing.Generic[_T], abc.ABC):
    def __reduce__(self: _V) -> typing.Tuple[typing.Type[_V], typing.Tuple[typing.List[Vector[_T]]]]: ...
    @abc.abstractmethod
    @classmethod
    def zeros(cls: typing.Type[_M], m: int, n: int) -> _M: ...
    @abc.abstractmethod
    def __init__(self, iterable: typing.Collection[typing.Collection[_T]]): ...
    @abc.abstractmethod
    def __copy__(self: _M) -> _M: ...
    def __len__(self) -> int: ...
    @abc.abstractmethod
    @typing.overload
    def __getitem__(self, index: int) -> Vector[_T]: ...
    @abc.abstractmethod
    @typing.overload
    def __getitem__(self, index: slice) -> Matrix[_T]: ...
    @abc.abstractmethod
    @typing.overload
    def __getitem__(self, index: typing.Tuple[int, int]) -> _T: ...
    @abc.abstractmethod
    def __setitem__(self, index: typing.Tuple[int, int], value: _T) -> None: ...
    @abc.abstractmethod
    def __add__(self: _M, other: typing.Union[_T, _M]) -> _M: ...
    @abc.abstractmethod
    def __iadd__(self: _M, other: typing.Union[_T, _M]) -> _M: ...
    @abc.abstractmethod
    def __mul__(self: _M, other: typing.Union[_T, _M]) -> _M: ...
    @abc.abstractmethod
    def __imul__(self: _M, other: typing.Union[_T, _M]) -> _M: ...
    @abc.abstractmethod
    def __repr__(self) -> str: ...
    @property
    def shape(self) -> typing.Tuple[int, int]: ...
    @property
    def strides(self) -> typing.Tuple[int, int]: ...
    @property
    @abc.abstractmethod
    def itemsize(self) -> int: ...
    @property
    @abc.abstractmethod
    def format(self) -> str: ...
    @abc.abstractmethod
    def argmax(self) -> typing.Tuple[int, int]: ...
    @abc.abstractmethod
    def argmin(self) -> typing.Tuple[int, int]: ...
    @abc.abstractmethod
    def copy(self: _M) -> _M: ...
    @abc.abstractmethod
    def max(self) -> _T: ...
    @abc.abstractmethod
    def min(self) -> _T: ...
    @abc.abstractmethod
    def sum(self) -> _T: ...

class MatrixF(Matrix[float]):
    @classmethod
    def zeros(cls, m: int, n: int) -> MatrixF: ...
    def __init__(self, iterable: typing.Collection[typing.Collection[float]]): ...
    def __copy__(self) -> MatrixF: ...
    def __eq__(self, other: object) -> bool: ...
    @typing.overload
    def __getitem__(self, index: int) -> VectorF: ...
    @typing.overload
    def __getitem__(self, index: slice) -> MatrixF: ...
    @typing.overload
    def __getitem__(self, index: typing.Tuple[int, int]) -> float: ...
    def __setitem__(self, index: typing.Tuple[int, int], value: float) -> None: ...
    def __add__(self, other: typing.Union[float, MatrixF]) -> MatrixF: ...
    def __iadd__(self, other: typing.Union[float, MatrixF]) -> MatrixF: ...
    def __mul__(self, other: typing.Union[float, MatrixF]) -> MatrixF: ...
    def __imul__(self, other: typing.Union[float, MatrixF]) -> MatrixF: ...
    def __repr__(self) -> str: ...
    def __sizeof__(self) -> int: ...
    def argmax(self) -> typing.Tuple[int, int]: ...
    def argmin(self) -> typing.Tuple[int, int]: ...
    def copy(self) -> MatrixF: ...
    def max(self) -> float: ...
    def min(self) -> float: ...
    def sum(self) -> float: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def format(self) -> str: ...

class MatrixU8(Matrix[int]):
    @classmethod
    def zeros(cls, m: int, n: int) -> MatrixU8: ...
    def __init__(self, iterable: typing.Collection[typing.Collection[float]]): ...
    def __copy__(self) -> MatrixU8: ...
    def __eq__(self, other: object) -> bool: ...
    @typing.overload
    def __getitem__(self, index: int) -> VectorU8: ...
    @typing.overload
    def __getitem__(self, index: slice) -> MatrixU8: ...
    @typing.overload
    def __getitem__(self, index: typing.Tuple[int, int]) -> int: ...
    def __setitem__(self, index: typing.Tuple[int, int], value: int) -> None: ...
    def __add__(self, other: typing.Union[int, MatrixU8]) -> MatrixU8: ...
    def __iadd__(self, other: typing.Union[int, MatrixU8]) -> MatrixU8: ...
    def __mul__(self, other: typing.Union[int, MatrixU8]) -> MatrixU8: ...
    def __imul__(self, other: typing.Union[int, MatrixU8]) -> MatrixU8: ...
    def __repr__(self) -> str: ...
    def __sizeof__(self) -> int: ...
    def argmax(self) -> typing.Tuple[int, int]: ...
    def argmin(self) -> typing.Tuple[int, int]: ...
    def copy(self) -> MatrixU8: ...
    def max(self) -> int: ...
    def min(self) -> int: ...
    def sum(self) -> int: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def format(self) -> str: ...

# --- Multiple Sequences Alignment -------------------------------------------

class _MSASequences(typing.Sequence[Sequence], abc.ABC):
    def __len__(self) -> int: ...
    @abc.abstractmethod
    def __getitem__(self, idx: int) -> Sequence: ...  # type: ignore

class MSA(abc.ABC, typing.Sized):
    @abc.abstractmethod
    def __init__(
        self, nsequences: int, length: typing.Optional[int] = None
    ) -> None: ...
    def __copy__(self) -> MSA: ...
    def __eq__(self, other: object) -> bool: ...
    def __len__(self) -> int: ...
    @property
    def accession(self) -> typing.Optional[bytes]: ...
    @accession.setter
    def accession(self, accession: typing.Optional[bytes]) -> None: ...
    @property
    def author(self) -> typing.Optional[bytes]: ...
    @author.setter
    def author(self, author: typing.Optional[bytes]) -> None: ...
    @property
    def name(self) -> typing.Optional[bytes]: ...
    @name.setter
    def name(self, name: typing.Optional[bytes]) -> None: ...
    @property
    def description(self) -> typing.Optional[bytes]: ...
    @description.setter
    def description(self, description: typing.Optional[bytes]) -> None: ...
    @property
    def names(self) -> typing.Tuple[bytes]: ...
    @abc.abstractmethod
    def copy(self) -> MSA: ...
    def checksum(self) -> int: ...
    def write(self, fh: typing.BinaryIO, format: str) -> None: ...

class _TextMSASequences(_MSASequences, typing.Sequence[TextSequence]):
    def __init__(self, msa: TextMSA) -> None: ...
    def __getitem__(self, idx: int) -> TextSequence: ...  # type: ignore
    def __setitem__(self, idx: int, item: TextSequence) -> None: ...

class TextMSA(MSA):
    def __init__(
        self,
        name: typing.Optional[bytes] = None,
        description: typing.Optional[bytes] = None,
        accession: typing.Optional[bytes] = None,
        sequences: typing.Optional[typing.Iterable[TextSequence]] = None,
        author: typing.Optional[bytes] = None,
    ) -> None: ...
    def __copy__(self) -> TextMSA: ...
    def copy(self) -> TextMSA: ...
    def digitize(self, alphabet: Alphabet) -> DigitalMSA: ...
    @property
    def alignment(self) -> typing.Tuple[str]: ...
    @property
    def sequences(self) -> _TextMSASequences: ...

class _DigitalMSASequences(_MSASequences, typing.Sequence[DigitalSequence]):
    alphabet: Alphabet
    def __init__(self, msa: DigitalMSA) -> None: ...
    def __getitem__(self, idx: int) -> DigitalSequence: ...  # type: ignore
    def __setitem__(self, idx: int, item: DigitalSequence) -> None: ...

class DigitalMSA(MSA):
    alphabet: Alphabet
    def __init__(
        self,
        alphabet: Alphabet,
        name: typing.Optional[bytes] = None,
        description: typing.Optional[bytes] = None,
        accession: typing.Optional[bytes] = None,
        sequences: typing.Optional[typing.Iterable[DigitalSequence]] = None,
        author: typing.Optional[bytes] = None,
    ) -> None: ...
    def __copy__(self) -> DigitalMSA: ...
    def copy(self) -> DigitalMSA: ...
    def textize(self) -> TextMSA: ...
    @property
    def sequences(self) -> _DigitalMSASequences: ...

# --- MSA File ---------------------------------------------------------------

class MSAFile(typing.ContextManager[MSAFile], typing.Iterator[MSA]):
    alphabet: typing.Optional[Alphabet]
    def __init__(
        self,
        file: typing.Union[typing.AnyStr, os.PathLike[typing.AnyStr], typing.BinaryIO],
        format: typing.Optional[str] = None
    ) -> None: ...
    def __enter__(self) -> MSAFile: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> bool: ...
    def __iter__(self) -> MSAFile: ...
    def __next__(self) -> MSA: ...
    def read(self) -> typing.Optional[MSA]: ...
    def close(self) -> None: ...
    def guess_alphabet(self) -> typing.Optional[Alphabet]: ...
    def set_digital(self, alphabet: Alphabet) -> Alphabet: ...

# --- Randomness -------------------------------------------------------------

class Randomness(object):
    def __init__(
        self, seed: typing.Optional[int] = None, fast: bool = False
    ) -> None: ...
    def __copy__(self) -> Randomness: ...
    def __getstate__(self) -> typing.Tuple[typing.Any, ...]: ...
    def __setstate__(self, state: typing.Tuple[typing.Any, ...]) -> None: ...
    def __sizeof__(self) -> int: ...
    def getstate(self) -> typing.Tuple[typing.Any, ...]: ...
    def setstate(self, state: typing.Tuple[typing.Any, ...]) -> None: ...
    def seed(self, n: typing.Optional[int] = None) -> None: ...
    def copy(self) -> Randomness: ...
    def random(self) -> float: ...
    def normalvariate(self, mu: float, sigma: float) -> float: ...
    def is_fast(self) -> bool: ...

# --- Sequence ---------------------------------------------------------------

class Sequence(typing.Sized, abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None: ...
    def __copy__(self) -> Sequence: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def accession(self) -> bytes: ...
    @accession.setter
    def accession(self, accession: bytes) -> None: ...
    @property
    def description(self) -> bytes: ...
    @description.setter
    def description(self, description: bytes) -> None: ...
    @property
    def name(self) -> bytes: ...
    @name.setter
    def name(self, name: bytes) -> None: ...
    @property
    def source(self) -> bytes: ...
    @source.setter
    def source(self, src: bytes) -> None: ...
    @property
    def taxonomy_id(self) -> typing.Optional[int]: ...
    @taxonomy_id.setter
    def taxonomy_id(self, tax_id: typing.Optional[int]) -> None: ...
    @property
    def residue_markups(self) -> typing.Dict[bytes, bytes]: ...
    @residue_markups.setter
    def residue_markups(self, xr: typing.Dict[bytes, bytes]) -> None: ...
    def checksum(self) -> int: ...
    def clear(self) -> None: ...
    @abc.abstractmethod
    def copy(self) -> Sequence: ...
    def write(self, fh: typing.BinaryIO) -> None: ...
    if sys.version_info >= (3, 8):
        @typing.overload
        def reverse_complement(self, inplace: typing.Literal[True]) -> None: ...
        @typing.overload
        def reverse_complement(
            self, inplace: typing.Literal[False] = False
        ) -> Sequence: ...
    else:
        @typing.overload
        def reverse_complement(
            self, inplace: bool = False
        ) -> typing.Optional[Sequence]: ...

class TextSequence(Sequence):
    def __init__(
        self,
        name: bytes = None,
        description: bytes = None,
        accession: bytes = None,
        sequence: str = None,
        source: bytes = None,
    ) -> None: ...
    def copy(self) -> TextSequence: ...
    def digitize(self, alphabet: Alphabet) -> DigitalSequence: ...
    @property
    def sequence(self) -> str: ...
    if sys.version_info >= (3, 8):
        @typing.overload
        def reverse_complement(self, inplace: typing.Literal[True]) -> None: ...
        @typing.overload
        def reverse_complement(
            self, inplace: typing.Literal[False] = False
        ) -> TextSequence: ...
    else:
        def reverse_complement(
            self, inplace: bool = False
        ) -> typing.Optional[TextSequence]: ...

class DigitalSequence(Sequence):
    alphabet: Alphabet
    def __init__(
        self,
        alphabet: Alphabet,
        name: bytes = None,
        description: bytes = None,
        accession: bytes = None,
        sequence: str = None,
        source: bytes = None,
    ) -> None: ...
    def copy(self) -> DigitalSequence: ...
    def textize(self) -> TextSequence: ...
    @property
    def sequence(self) -> VectorU8: ...
    if sys.version_info >= (3, 8):
        @typing.overload
        def reverse_complement(self, inplace: typing.Literal[True]) -> None: ...
        @typing.overload
        def reverse_complement(
            self, inplace: typing.Literal[False] = False
        ) -> DigitalSequence: ...
    else:
        def reverse_complement(
            self, inplace: bool = False
        ) -> typing.Optional[DigitalSequence]: ...

# --- Sequence File ----------------------------------------------------------

class SequenceFile(typing.ContextManager[SequenceFile], typing.Iterator[Sequence]):
    @classmethod
    def parse(cls, buffer: bytes, format: str) -> Sequence: ...
    @classmethod
    def parseinto(cls, seq: Sequence, buffer: bytes, format: str) -> Sequence: ...
    def __init__(
        self,
        file: typing.Union[typing.AnyStr, os.PathLike[typing.AnyStr], typing.BinaryIO],
        format: typing.Optional[str] = None,
        ignore_gaps: bool = False
    ) -> None: ...
    def __enter__(self) -> SequenceFile: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> bool: ...
    def __iter__(self) -> SequenceFile: ...
    def __next__(self) -> Sequence: ...
    def read(self) -> typing.Optional[Sequence]: ...
    def read_info(self) -> typing.Optional[Sequence]: ...
    def read_seq(self) -> typing.Optional[Sequence]: ...
    def readinto(self, seq: Sequence) -> typing.Optional[Sequence]: ...
    def readinto_seq(self, seq: Sequence) -> typing.Optional[Sequence]: ...
    def readinto_info(self, seq: Sequence) -> typing.Optional[Sequence]: ...
    def close(self) -> None: ...
    def guess_alphabet(self) -> typing.Optional[Alphabet]: ...
    def set_digital(self, alphabet: Alphabet) -> Alphabet: ...

# --- Sequence/Subsequence Index ---------------------------------------------

class SSIReader(object):
    def __init__(
        self, file: typing.Union[typing.AnyStr, os.PathLike[typing.AnyStr]]
    ) -> None: ...
    def __enter__(self) -> SSIReader: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> bool: ...
    def close(self) -> None: ...

class SSIWriter(object):
    def __init__(
        self, file: typing.Union[typing.AnyStr, os.PathLike[typing.AnyStr]]
    ) -> None: ...
    def __enter__(self) -> SSIWriter: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> bool: ...
    def add_alias(self, alias: bytes, key: bytes) -> None: ...
    def add_file(self, filename: str, format: int = 0) -> int: ...
    def add_key(
        self,
        key: bytes,
        fd: int,
        record_offset: int,
        data_offset: int = 0,
        record_length: int = 0,
    ) -> None: ...
    def close(self) -> None: ...
