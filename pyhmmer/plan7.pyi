# coding: utf-8
import collections.abc
import datetime
import enum
import os
import sys
import types
import typing

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

from .utils import SizedIterator
from .easel import (
    Alphabet,
    Sequence,
    DigitalSequence,
    DigitalSequenceBlock,
    KeyHash,
    MSA,
    DigitalMSA,
    TextMSA,
    Randomness,
    SequenceFile,
    VectorF,
    VectorU8,
    MatrixU8,
)

BIT_CUTOFFS = Literal["gathering", "trusted", "noise"]
SORT_KEY = Literal["key", "seqidx"]
ARCHITECTURE = Literal["fast", "hand"]
WEIGHTING = Literal["pb", "gsc", "blosum", "none", "given"]
EFFECTIVE = Literal["entropy", "exp", "clust", "none"]
PRIOR_SCHEME = Literal["laplace", "alphabet"]
STRAND = Literal["watson", "crick"]
HITS_FORMAT = Literal["targets", "domain", "pfam"]
HITS_MODE = Literal["search", "scan"]

class Alignment(collections.abc.Sized):
    domain: Domain
    def __len__(self) -> int: ...
    def __getstate__(self) -> typing.Dict[str, object]: ...
    def __setstate__(self, state: typing.Dict[str, object]) -> None: ...
    @property
    def hmm_accession(self) -> bytes: ...
    @property
    def hmm_from(self) -> int: ...
    @property
    def hmm_name(self) -> bytes: ...
    @property
    def hmm_sequence(self) -> str: ...
    @property
    def hmm_to(self) -> int: ...
    @property
    def target_from(self) -> int: ...
    @property
    def target_name(self) -> bytes: ...
    @property
    def target_sequence(self) -> str: ...
    @property
    def target_to(self) -> int: ...
    @property
    def identity_sequence(self) -> str: ...

class Background(object):
    def __init__(self, alphabet: Alphabet, uniform: bool = False) -> None: ...
    def __copy__(self) -> Background: ...
    @property
    def L(self) -> int: ...
    @L.setter
    def L(self, L: int) -> None: ...
    @property
    def residue_frequencies(self) -> VectorF: ...
    @property
    def transition_probability(self) -> float: ...
    @property
    def omega(self) -> float: ...
    @omega.setter
    def omega(self, omega: float) -> None: ...
    def copy(self) -> Background: ...

class Builder(object):
    _ARCHITECTURE_STRATEGY: typing.ClassVar[typing.Dict[str, int]]
    _WEIGHTING_STRATEGY: typing.ClassVar[typing.Dict[str, int]]
    _EFFECTIVE_STRATEGY: typing.ClassVar[typing.Dict[str, int]]
    alphabet: Alphabet
    randomness: Randomness
    score_matrix: str
    architecture: ARCHITECTURE
    weighting: WEIGHTING
    effective_number: typing.Union[EFFECTIVE, int, float]
    prior_scheme: typing.Optional[PRIOR_SCHEME]
    popen: float
    pextend: float
    def __init__(
        self,
        alphabet: Alphabet,
        *,
        architecture: ARCHITECTURE = "fast",
        weighting: WEIGHTING = "pb",
        effective_number: typing.Union[EFFECTIVE, int, float] = "entropy",
        prior_scheme: typing.Optional[PRIOR_SCHEME] = "alphabet",
        symfrac: float = 0.5,
        fragthresh: float = 0.5,
        wid: float = 0.62,
        esigma: float = 45.0,
        eid: float = 0.62,
        EmL: int = 200,
        EmN: int = 200,
        EvL: int = 200,
        EvN: int = 200,
        EfL: int = 100,
        EfN: int = 200,
        Eft: float = 0.04,
        seed: int = 42,
        ere: typing.Optional[float] = None,
        popen: typing.Optional[float] = None,
        pextend: typing.Optional[float] = None,
        score_matrix: typing.Optional[str] = None,
        window_length: typing.Optional[int] = None,
        window_beta: typing.Optional[float] = None,
    ) -> None: ...
    def __copy__(self) -> Builder: ...
    @property
    def seed(self) -> int: ...
    @seed.setter
    def seed(self, seed: int) -> None: ...
    @property
    def window_length(self) -> typing.Optional[int]: ...
    @window_length.setter
    def window_length(self, window_length: typing.Optional[int]) -> None: ...
    @property
    def window_beta(self) -> typing.Optional[float]: ...
    @window_beta.setter
    def window_beta(self, window_beta: typing.Optional[float]) -> None: ...
    def build(
        self,
        sequence: DigitalSequence,
        background: Background,
    ) -> typing.Tuple[HMM, Profile, OptimizedProfile]: ...
    def build_msa(
        self,
        msa: DigitalMSA,
        background: Background,
    ) -> typing.Tuple[HMM, Profile, OptimizedProfile]: ...
    def copy(self) -> Builder: ...

class Cutoffs(object):
    def __init__(self, owner: typing.Union[Profile, HMM]) -> None: ...
    def __copy__(self) -> Cutoffs: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def gathering(self) -> typing.Optional[typing.Tuple[float, float]]: ...
    @gathering.setter
    def gathering(
        self, gathering: typing.Optional[typing.Tuple[float, float]]
    ) -> None: ...
    @gathering.deleter
    def gathering(self) -> None: ...
    @property
    def gathering1(self) -> typing.Optional[float]: ...
    @property
    def gathering2(self) -> typing.Optional[float]: ...
    @property
    def trusted(self) -> typing.Optional[typing.Tuple[float, float]]: ...
    @trusted.setter
    def trusted(self, trusted: typing.Optional[typing.Tuple[float, float]]) -> None: ...
    @trusted.deleter
    def trusted(self) -> None: ...
    @property
    def trusted1(self) -> typing.Optional[float]: ...
    @property
    def trusted2(self) -> typing.Optional[float]: ...
    @property
    def noise(self) -> typing.Optional[typing.Tuple[float, float]]: ...
    @noise.setter
    def noise(self, noise: typing.Optional[typing.Tuple[float, float]]) -> None: ...
    @noise.deleter
    def noise(self) -> None: ...
    @property
    def noise1(self) -> typing.Optional[float]: ...
    @property
    def noise2(self) -> typing.Optional[float]: ...
    def gathering_available(self) -> bool: ...
    def trusted_available(self) -> bool: ...
    def noise_available(self) -> bool: ...
    def as_vector(self) -> VectorF: ...

class Domain(object):
    alignment: Alignment
    hit: Hit
    def __getstate__(self) -> typing.Dict[str, object]: ...
    def __setstate__(self, state: typing.Dict[str, object]) -> None: ...
    @property
    def env_from(self) -> int: ...
    @property
    def env_to(self) -> int: ...
    @property
    def score(self) -> float: ...
    @property
    def bias(self) -> float: ...
    @property
    def correction(self) -> float: ...
    @property
    def envelope_score(self) -> float: ...
    @property
    def c_evalue(self) -> float: ...
    @property
    def i_evalue(self) -> float: ...
    @property
    def pvalue(self) -> float: ...
    @property
    def included(self) -> bool: ...
    @included.setter
    def included(self, included: bool) -> None: ...
    @property
    def reported(self) -> bool: ...
    @reported.setter
    def reported(self, reported: bool) -> None: ...

class Domains(typing.Sequence[Domain]):
    hit: Hit
    def __len__(self) -> int: ...
    def __getstate__(self) -> typing.List[typing.Dict[str, object]]: ...
    @typing.overload
    def __getitem__(self, index: int) -> Domain: ...
    @typing.overload
    def __getitem__(self, index: slice) -> typing.Sequence[Domain]: ...
    @property
    def reported(self) -> SizedIterator[Domain]: ...
    @property
    def included(self) -> SizedIterator[Domain]: ...

class EvalueParameters:
    def __init__(self, owner: typing.Union[Profile, HMM]) -> None: ...
    def __copy__(self) -> EvalueParameters: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def m_mu(self) -> typing.Optional[float]: ...
    @m_mu.setter
    def m_mu(self, m: typing.Optional[float]) -> None: ...
    @property
    def m_lambda(self) -> typing.Optional[float]: ...
    @m_lambda.setter
    def m_lambda(self, l: typing.Optional[float]) -> None: ...
    @property
    def v_mu(self) -> typing.Optional[float]: ...
    @v_mu.setter
    def v_mu(self, m: typing.Optional[float]) -> None: ...
    @property
    def v_lambda(self) -> typing.Optional[float]: ...
    @v_lambda.setter
    def v_lambda(self, l: typing.Optional[float]) -> None: ...
    @property
    def f_tau(self) -> typing.Optional[float]: ...
    @f_tau.setter
    def f_tau(self, t: typing.Optional[float]) -> None: ...
    @property
    def f_lambda(self) -> typing.Optional[float]: ...
    @f_lambda.setter
    def f_lambda(self, l: typing.Optional[float]) -> None: ...
    def as_vector(self) -> VectorF: ...

class Hit(object):
    hits: TopHits
    def __getstate__(self) -> typing.Dict[str, object]: ...
    @property
    def name(self) -> bytes: ...
    @name.setter
    def name(self, name: bytes) -> None: ...
    @property
    def accession(self) -> typing.Optional[bytes]: ...
    @accession.setter
    def accession(self, accession: typing.Optional[bytes]) -> None: ...
    @property
    def description(self) -> typing.Optional[bytes]: ...
    @description.setter
    def description(self, description: typing.Optional[bytes]) -> None: ...
    @property
    def score(self) -> float: ...
    @property
    def pre_score(self) -> float: ...
    @property
    def sum_score(self) -> float: ...
    @property
    def bias(self) -> float: ...
    @property
    def evalue(self) -> float: ...
    @property
    def pvalue(self) -> float: ...
    @property
    def domains(self) -> Domains: ...
    @property
    def best_domain(self) -> Domain: ...
    @property
    def included(self) -> bool: ...
    @included.setter
    def included(self, included: bool) -> None: ...
    @property
    def reported(self) -> bool: ...
    @reported.setter
    def reported(self, reported: bool) -> None: ...
    @property
    def new(self) -> bool: ...
    @new.setter
    def new(self, new: bool) -> None: ...
    @property
    def dropped(self) -> bool: ...
    @dropped.setter
    def dropped(self, dropped: bool) -> None: ...
    @property
    def duplicate(self) -> bool: ...
    @duplicate.setter
    def duplicate(self, duplicate: bool) -> None: ...

class HMM(object):
    alphabet: Alphabet
    @classmethod
    def sample(
        cls,
        alphabet: Alphabet,
        M: int,
        randomness: Randomness,
        ungapped: bool = False,
        enumerate: bool = False,
    ) -> HMM: ...
    def __init__(self, alphabet: Alphabet, M: int, name: bytes) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __copy__(self) -> HMM: ...
    def __deepcopy__(self, memo: typing.Dict[int, object]) -> HMM: ...
    def __sizeof__(self) -> int: ...
    def __getstate__(self) -> typing.Dict[str, object]: ...
    def __setstate__(self, state: typing.Dict[str, object]) -> None: ...
    @property
    def M(self) -> int: ...
    @property
    def name(self) -> bytes: ...
    @name.setter
    def name(self, name: bytes) -> None: ...
    @property
    def accession(self) -> typing.Optional[bytes]: ...
    @accession.setter
    def accession(self, accession: typing.Optional[bytes]) -> None: ...
    @property
    def checksum(self) -> typing.Optional[int]: ...
    @property
    def composition(self) -> typing.Optional[VectorF]: ...
    @property
    def description(self) -> typing.Optional[bytes]: ...
    @description.setter
    def description(self, description: typing.Optional[bytes]) -> None: ...
    @property
    def consensus(self) -> typing.Optional[str]: ...
    @property
    def consensus_structure(self) -> typing.Optional[str]: ...
    @property
    def consensus_accessibility(self) -> typing.Optional[str]: ...
    @property
    def command_line(self) -> typing.Optional[str]: ...
    @command_line.setter
    def command_line(self, cli: typing.Optional[str]) -> None: ...
    @property
    def nseq(self) -> typing.Optional[int]: ...
    @property
    def nseq_effective(self) -> typing.Optional[int]: ...
    @property
    def creation_time(self) -> typing.Optional[datetime.datetime]: ...
    @creation_time.setter
    def creation_time(self, ctime: typing.Optional[datetime.datetime]) -> None: ...
    @property
    def evalue_parameters(self) -> EvalueParameters: ...
    @property
    def cutoffs(self) -> Cutoffs: ...
    def copy(self) -> HMM: ...
    def match_occupancy(self) -> VectorF: ...
    def mean_match_entropy(self) -> float: ...
    def mean_match_information(self, background: Background) -> float: ...
    def mean_match_relative_entropy(self, background: Background) -> float: ...
    def renormalize(self) -> None: ...
    def scale(self, scale: float, exponential: bool = False) -> None: ...
    def set_composition(self) -> None: ...
    def to_profile(
        self, 
        background: typing.Optional[Background] = None,
        L: int = 400, 
        multihit: bool = True,
        local: bool = True,
    ) -> Profile: ...
    def validate(self, tolerance: float = ...) -> None: ...
    def write(self, fh: typing.BinaryIO, binary: bool = False) -> None: ...
    def zero(self) -> None: ...

class HMMFile(typing.ContextManager[HMMFile], typing.Iterator[HMM]):
    _FORMATS: typing.ClassVar[typing.Dict[str, int]]
    _MAGIC: typing.ClassVar[typing.Dict[int, int]]
    def __init__(
        self,
        file: typing.Union[typing.AnyStr, os.PathLike[typing.AnyStr], typing.BinaryIO],
        db: bool = True,
    ) -> None: ...
    def __enter__(self) -> HMMFile: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> bool: ...
    def __iter__(self) -> HMMFile: ...
    def __next__(self) -> HMM: ...
    def __repr__(self) -> str: ...
    @property
    def closed(self) -> bool: ...
    @property
    def name(self) -> typing.Optional[str]: ...
    def close(self) -> None: ...
    def is_pressed(self) -> bool: ...
    def read(self) -> typing.Optional[HMM]: ...
    def rewind(self) -> None: ...
    def optimized_profiles(self) -> HMMPressedFile: ...

class HMMPressedFile(typing.Iterator[OptimizedProfile]):
    def __init__(
        self,
        file: typing.Union[typing.AnyStr, os.PathLike[typing.AnyStr]],
    ) -> None: ...
    def __enter__(self) -> HMMPressedFile: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> bool: ...
    def __iter__(self) -> HMMPressedFile: ...
    def __next__(self) -> OptimizedProfile: ...
    @property
    def closed(self) -> bool: ...
    @property
    def name(self) -> str: ...
    def close(self) -> None: ...
    def read(self) -> typing.Optional[OptimizedProfile]: ...
    def rewind(self) -> None: ...

class IterationResult(typing.NamedTuple):
    hmm: HMM
    hits: TopHits
    msa: DigitalMSA
    converged: bool
    iteration: int

class IterativeSearch(typing.Iterator[IterationResult]):
    pipeline: Pipeline
    builder: Builder
    query: typing.Union[DigitalSequence, HMM]
    converged: bool
    targets: DigitalSequenceBlock
    ranking: KeyHash
    iteration: int
    def __init__(
        self,
        pipeline: Pipeline,
        builder: Builder,
        query: typing.Union[DigitalSequence, HMM],
        targets: DigitalSequenceBlock,
        select_hits: typing.Optional[typing.Callable[[TopHits], None]] = None,
    ) -> None: ...
    def __iter__(self) -> IterativeSearch: ...
    def __next__(self) -> IterationResult: ...

class OptimizedProfile(object):
    alphabet: Alphabet
    def __init__(self, M: int, abc: Alphabet) -> None: ...
    def __copy__(self) -> OptimizedProfile: ...
    def __deepcopy__(self, memo: typing.Dict[int, object]) -> OptimizedProfile: ...
    def __eq__(self, other: object) -> bool: ...
    def __sizeof__(self) -> int: ...
    @property
    def M(self) -> int: ...
    @property
    def L(self) -> int: ...
    @L.setter
    def L(self, L: int) -> None: ...
    @property
    def name(self) -> typing.Optional[bytes]: ...
    @property
    def accession(self) -> typing.Optional[bytes]: ...
    @property
    def description(self) -> typing.Optional[bytes]: ...
    @property
    def consensus(self) -> typing.Optional[str]: ...
    @property
    def consensus_structure(self) -> typing.Optional[str]: ...
    @property
    def tbm(self) -> int: ...
    @property
    def tec(self) -> int: ...
    @property
    def tjb(self) -> int: ...
    @property
    def base(self) -> int: ...
    @property
    def bias(self) -> int: ...
    @property
    def sbv(self) -> MatrixU8: ...
    @property
    def rbv(self) -> MatrixU8: ...
    @property
    def offsets(self) -> Offsets: ...
    @property
    def evalue_parameters(self) -> EvalueParameters: ...
    @property
    def cutoffs(self) -> Cutoffs: ...
    @property
    def local(self) -> bool: ...
    @property
    def multihit(self) -> bool: ...
    @multihit.setter
    def multihit(self, multihit: bool) -> None: ...
    def copy(self) -> OptimizedProfile: ...
    def write(
        self, fh_filter: typing.BinaryIO, fh_profile: typing.BinaryIO
    ) -> None: ...
    def convert(self, profile: Profile) -> None: ...
    def ssv_filter(self, seq: DigitalSequence) -> typing.Optional[float]: ...

class OptimizedProfileBlock(typing.MutableSequence[OptimizedProfile]):
    alphabet: Alphabet
    def __init__(
        self, alphabet: Alphabet, iterable: typing.Iterable[OptimizedProfile] = ()
    ) -> None: ...
    def __len__(self) -> int: ...
    @typing.overload
    def __getitem__(self, index: int) -> OptimizedProfile: ...
    @typing.overload
    def __getitem__(self, index: slice) -> OptimizedProfileBlock: ...
    @typing.overload
    def __setitem__(self, index: int, optimized_profile: OptimizedProfile) -> None: ...
    @typing.overload
    def __setitem__(
        self, index: slice, optimized_profile: typing.Iterable[OptimizedProfile]
    ) -> None: ...
    @typing.overload
    def __delitem__(self, index: int) -> None: ...
    @typing.overload
    def __delitem__(self, index: slice) -> None: ...
    def __repr__(self) -> str: ...
    def __contains__(self, item: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __copy__(self) -> OptimizedProfileBlock: ...
    def copy(self) -> OptimizedProfileBlock: ...
    def clear(self) -> None: ...
    def append(self, optimized_profile: OptimizedProfile) -> None: ...
    def extend(self, iterable: typing.Iterable[OptimizedProfile]) -> None: ...
    def pop(self, index: int = -1) -> OptimizedProfile: ...
    def insert(self, index: int, optimized_profile: OptimizedProfile) -> None: ...
    def index(
        self,
        optimized_profile: OptimizedProfile,
        start: int = 0,
        end: int = sys.maxsize,
    ) -> int: ...
    def remove(self, optimized_profile: OptimizedProfile) -> None: ...

class Offsets(object):
    def __init__(self, owner: typing.Union[Profile, OptimizedProfile]) -> None: ...
    def __copy__(self) -> Offsets: ...
    def __repr__(self) -> str: ...
    @property
    def model(self) -> typing.Optional[int]: ...
    @model.setter
    def model(self, model: typing.Optional[int]) -> None: ...
    @property
    def filter(self) -> typing.Optional[int]: ...
    @filter.setter
    def filter(self, filter: typing.Optional[int]) -> None: ...
    @property
    def profile(self) -> typing.Optional[int]: ...
    @profile.setter
    def profile(self, profile: typing.Optional[int]) -> None: ...

class Pipeline(object):
    M_HINT: typing.ClassVar[int] = 100
    L_HINT: typing.ClassVar[int] = 100
    _BIT_CUTOFFS: typing.ClassVar[typing.Dict[str, int]]
    alphabet: Alphabet
    background: Background
    profile: typing.Optional[Profile]
    randomness: Randomness
    def __init__(
        self,
        alphabet: Alphabet,
        background: typing.Optional[Background] = None,
        *,
        bias_filter: bool = True,
        null2: bool = True,
        seed: int = 42,
        Z: typing.Optional[float] = None,
        domZ: typing.Optional[float] = None,
        F1: float = 0.02,
        F2: float = 1e-3,
        F3: float = 1e-5,
        E: float = 10.0,
        T: typing.Optional[float] = None,
        domE: float = 10.0,
        domT: typing.Optional[float] = None,
        incE: float = 0.01,
        incT: typing.Optional[float] = None,
        incdomE: float = 0.01,
        incdomT: typing.Optional[float] = None,
        bit_cutoffs: typing.Optional[BIT_CUTOFFS] = None,
    ) -> None: ...
    @property
    def Z(self) -> typing.Optional[float]: ...
    @Z.setter
    def Z(self, Z: typing.Optional[float]) -> None: ...
    @property
    def domZ(self) -> typing.Optional[float]: ...
    @domZ.setter
    def domZ(self, domZ: typing.Optional[float]) -> None: ...
    @property
    def null2(self) -> bool: ...
    @null2.setter
    def null2(self, null2: bool) -> None: ...
    @property
    def bias_filter(self) -> bool: ...
    @bias_filter.setter
    def bias_filter(self, bias_filter: bool) -> None: ...
    @property
    def F1(self) -> float: ...
    @F1.setter
    def F1(self, F1: float) -> None: ...
    @property
    def F2(self) -> float: ...
    @F2.setter
    def F2(self, F2: float) -> None: ...
    @property
    def F3(self) -> float: ...
    @F3.setter
    def F3(self, F3: float) -> None: ...
    @property
    def E(self) -> float: ...
    @E.setter
    def E(self, E: float) -> None: ...
    @property
    def T(self) -> typing.Optional[float]: ...
    @T.setter
    def T(self, T: typing.Optional[float]) -> None: ...
    @property
    def domE(self) -> float: ...
    @domE.setter
    def domE(self, domE: float) -> None: ...
    @property
    def domT(self) -> typing.Optional[float]: ...
    @domT.setter
    def domT(self, domT: typing.Optional[float]) -> None: ...
    @property
    def incE(self) -> float: ...
    @incE.setter
    def incE(self, incE: float) -> None: ...
    @property
    def incT(self) -> typing.Optional[float]: ...
    @incT.setter
    def incT(self, incT: typing.Optional[float]) -> None: ...
    @property
    def incdomE(self) -> float: ...
    @incdomE.setter
    def incdomE(self, incdomE: float) -> None: ...
    @property
    def incdomT(self) -> typing.Optional[float]: ...
    @incdomT.setter
    def incdomT(self, incdomT: typing.Optional[float]) -> None: ...
    @property
    def bit_cutoffs(self) -> typing.Optional[BIT_CUTOFFS]: ...
    @bit_cutoffs.setter
    def bit_cutoffs(self, bit_cutoffs: typing.Optional[BIT_CUTOFFS]) -> None: ...
    @property
    def strand(self) -> typing.Optional[STRAND]: ...
    @strand.setter
    def strand(self, strand: typing.Optional[STRAND]) -> None: ...
    def arguments(self) -> typing.List[str]: ...
    def clear(self) -> None: ...
    def search_hmm(
        self,
        query: typing.Union[HMM, Profile, OptimizedProfile],
        sequences: typing.Union[DigitalSequenceBlock, SequenceFile],
    ) -> TopHits: ...
    def search_msa(
        self,
        query: DigitalMSA,
        sequences: typing.Union[DigitalSequenceBlock, SequenceFile],
        builder: typing.Optional[Builder] = None,
    ) -> TopHits: ...
    def search_seq(
        self,
        query: DigitalSequence,
        sequences: typing.Union[DigitalSequenceBlock, SequenceFile],
        builder: typing.Optional[Builder] = None,
    ) -> TopHits: ...
    def scan_seq(
        self,
        query: DigitalSequence,
        optimized_profiles: typing.Union[OptimizedProfileBlock, HMMPressedFile],
    ) -> TopHits: ...
    def iterate_seq(
        self,
        query: DigitalSequence,
        sequences: DigitalSequenceBlock,
        builder: typing.Optional[Builder] = None,
        select_hits: typing.Optional[typing.Callable[[TopHits], None]] = None,
    ) -> IterativeSearch: ...
    def iterate_hmm(
        self,
        query: HMM,
        sequences: DigitalSequenceBlock,
        builder: typing.Optional[Builder] = None,
        select_hits: typing.Optional[typing.Callable[[TopHits], None]] = None,
    ) -> IterativeSearch: ...

class LongTargetsPipeline(Pipeline):
    def __init__(
        self,
        alphabet: Alphabet,
        background: typing.Optional[Background] = None,
        *,
        B1: int = 100,
        B2: int = 240,
        B3: int = 1000,
        block_length: int = 1024 * 256,
        bias_filter: bool = True,
        null2: bool = True,
        seed: typing.Optional[int] = None,
        Z: typing.Optional[float] = None,
        domZ: typing.Optional[float] = None,
        F1: float = 0.02,
        F2: float = 1e-3,
        F3: float = 1e-5,
        E: float = 10.0,
        T: typing.Optional[float] = None,
        domE: float = 10.0,
        domT: typing.Optional[float] = None,
        incE: float = 0.01,
        incT: typing.Optional[float] = None,
        incdomE: float = 0.01,
        incdomT: typing.Optional[float] = None,
        bit_cutoffs: typing.Optional[BIT_CUTOFFS] = None,
    ) -> None: ...
    @property
    def B1(self) -> int: ...
    @B1.setter
    def B1(self, B1: int) -> None: ...
    @property
    def B2(self) -> int: ...
    @B2.setter
    def B2(self, B2: int) -> None: ...
    @property
    def B3(self) -> int: ...
    @B3.setter
    def B3(self, B3: int) -> None: ...
    @property
    def strand(self) -> typing.Optional[STRAND]: ...
    @strand.setter
    def strand(self, strand: typing.Optional[STRAND]) -> None: ...

class Profile(object):
    alphabet: Alphabet
    def __init__(self, M: int, alphabet: Alphabet) -> None: ...
    def __copy__(self) -> Profile: ...
    def __deepcopy__(self, memo: typing.Dict[int, object]) -> Profile: ...
    def __eq__(self, other: object) -> bool: ...
    def __sizeof__(self) -> int: ...
    @property
    def M(self) -> int: ...
    @property
    def name(self) -> typing.Optional[bytes]: ...
    @property
    def accession(self) -> typing.Optional[bytes]: ...
    @property
    def description(self) -> typing.Optional[bytes]: ...
    @property
    def consensus(self) -> typing.Optional[str]: ...
    @property
    def consensus_structure(self) -> typing.Optional[str]: ...
    @property
    def cutoffs(self) -> Cutoffs: ...
    @property
    def evalue_parameters(self) -> EvalueParameters: ...
    @property
    def offsets(self) -> Offsets: ...
    @property
    def local(self) -> bool: ...
    @property
    def multihit(self) -> bool: ...
    @multihit.setter
    def multihit(self, multihit: bool) -> None: ...
    def clear(self) -> None: ...
    def configure(
        self,
        hmm: HMM,
        background: Background,
        L: int = 400,
        multihit: bool = True,
        local: bool = True,
    ) -> None: ...
    def copy(self) -> Profile: ...
    def to_optimized(self) -> OptimizedProfile: ...

class ScoreData(object):
    Kp: int
    def __init__(self, gm: Profile, om: OptimizedProfile) -> None: ...
    def __copy__(self) -> ScoreData: ...
    def copy(self) -> ScoreData: ...

class TopHits(typing.Sequence[Hit]):
    def __init__(self) -> None: ...
    def __bool__(self) -> bool: ...
    def __copy__(self) -> TopHits: ...
    def __deepcopy__(self, memo: typing.Dict[int, object]) -> TopHits: ...
    def __len__(self) -> int: ...
    @typing.overload
    def __getitem__(self, index: int) -> Hit: ...
    @typing.overload
    def __getitem__(self, index: slice) -> typing.Sequence[Hit]: ...
    def __iadd__(self, other: TopHits) -> TopHits: ...
    def __getstate__(self) -> typing.Dict[str, object]: ...
    def __setstate__(self, state: typing.Dict[str, object]) -> None: ...
    @property
    def mode(self) -> HITS_MODE: ...
    @property
    def query_name(self) -> typing.Optional[bytes]: ...
    @property
    def query_accession(self) -> typing.Optional[bytes]: ...
    @property
    def Z(self) -> float: ...
    @property
    def domZ(self) -> float: ...
    @property
    def long_targets(self) -> bool: ...
    @property
    def E(self) -> float: ...
    @property
    def T(self) -> typing.Optional[float]: ...
    @property
    def domE(self) -> float: ...
    @property
    def domT(self) -> typing.Optional[float]: ...
    @property
    def incE(self) -> float: ...
    @property
    def incT(self) -> typing.Optional[float]: ...
    @property
    def incdomE(self) -> float: ...
    @property
    def incdomT(self) -> typing.Optional[float]: ...
    @property
    def bit_cutoffs(self) -> typing.Optional[BIT_CUTOFFS]: ...
    @property
    def searched_models(self) -> int: ...
    @property
    def searched_nodes(self) -> int: ...
    @property
    def searched_sequences(self) -> int: ...
    @property
    def searched_residues(self) -> int: ...
    @property
    def strand(self) -> typing.Optional[STRAND]: ...
    @property
    def block_length(self) -> typing.Optional[int]: ...
    @property
    def reported(self) -> SizedIterator[Hit]: ...
    @property
    def included(self) -> SizedIterator[Hit]: ...
    def compare_ranking(self, ranking: KeyHash) -> int: ...
    def sort(self, by: SORT_KEY = "key") -> None: ...
    def is_sorted(self, by: SORT_KEY = "key") -> bool: ...
    def copy(self) -> TopHits: ...
    def merge(self, *others: TopHits) -> TopHits: ...
    def to_msa(
        self,
        alphabet: Alphabet,
        sequences: typing.Optional[typing.List[Sequence]] = None,
        traces: typing.Optional[typing.List[Trace]] = None,
        *,
        trim: bool = False,
        digitize: bool = False,
        all_consensus_cols: bool = False,
    ) -> MSA: ...
    def write(
        self,
        fh: typing.BinaryIO,
        format: HITS_FORMAT = "targets",
        header: bool = True,
    ) -> None: ...

class Trace(object):
    def __init__(self, posteriors: bool = False) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def M(self) -> int: ...
    @property
    def L(self) -> int: ...
    @property
    def posterior_probabilities(self) -> typing.Optional[VectorF]: ...
    def expected_accuracy(self) -> float: ...

class Traces(typing.Sequence[Trace]):
    def __init__(self) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __len__(self) -> int: ...
    @typing.overload
    def __getitem__(self, index: int) -> Trace: ...
    @typing.overload
    def __getitem__(self, index: slice) -> typing.Sequence[Trace]: ...

class TraceAligner(object):
    def __init__(self) -> None: ...
    def compute_traces(
        self,
        hmm: HMM,
        sequences: DigitalSequenceBlock,
    ) -> Traces: ...
    @typing.overload
    def align_traces(
        self,
        hmm: HMM,
        sequences: DigitalSequenceBlock,
        traces: Traces,
        digitize: Literal[True],
        trim: bool = False,
        all_consensus_cols: bool = False,
    ) -> DigitalMSA: ...
    @typing.overload
    def align_traces(
        self,
        hmm: HMM,
        sequences: DigitalSequenceBlock,
        traces: Traces,
        digitize: Literal[False],
        trim: bool = False,
        all_consensus_cols: bool = False,
    ) -> TextMSA: ...
    @typing.overload
    def align_traces(
        self,
        hmm: HMM,
        sequences: DigitalSequenceBlock,
        traces: Traces,
        digitize: bool = False,
        trim: bool = False,
        all_consensus_cols: bool = False,
    ) -> MSA: ...

class Transitions(enum.IntEnum):
    MM = ...
    MI = ...
    MD = ...
    IM = ...
    II = ...
    DM = ...
    DD = ...