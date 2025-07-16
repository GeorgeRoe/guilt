from guilt.dependencies.injector import DependencyInjector
from abc import ABC, abstractmethod
from dataclasses import dataclass
import pytest

class NewsProviderInterface(ABC):
  @abstractmethod
  def get_news(self) -> str:
    pass
  
class BBC(NewsProviderInterface):
  def get_news(self) -> str:
    return "blah blah blah"
  
class ITV(NewsProviderInterface):
  def get_news(self) -> str:
    return "bleh bleh bleh"

class NewsConsumerInterface(ABC):
  @abstractmethod
  def consume_news(self) -> None:
    pass
  
  @abstractmethod
  def has_consumed_news(self) -> bool:
    pass
  
class NewsWatcher(NewsConsumerInterface):
  def __init__(self, news_provider: NewsProviderInterface) -> None:
    self.news_provider = news_provider
    self._has_consumed_news = False
    
  def consume_news(self) -> None:
    self.news_provider.get_news()
    self._has_consumed_news = True
    
  def has_consumed_news(self) -> bool:
    return self._has_consumed_news
  
class UntypedNewsWatcher(NewsConsumerInterface):
  def __init__(self, untyped_dependency) -> None: # type: ignore[reportMissingParameterType]
    self.dependency = untyped_dependency
    
  def consume_news(self) -> None:
    pass
  
  def has_consumed_news(self) -> bool:
    return False
  
@dataclass
class NewsContext:
  provider: NewsProviderInterface
  consumer: NewsConsumerInterface
  
class NotADataclass:
  pass
  
def test_bind_success() -> None:
  di = DependencyInjector()
  di.bind(NewsProviderInterface, BBC)
  di.bind(NewsConsumerInterface, NewsWatcher)
  news_watcher = di.resolve(NewsConsumerInterface) # type: ignore[type-abstract]
  
  assert isinstance(news_watcher, NewsWatcher)
  assert isinstance(news_watcher.news_provider, BBC)
  
def test_register_instance_success() -> None:
  di = DependencyInjector()
  
  bbc = BBC()
  
  di.register_instance(NewsProviderInterface, bbc)
  di.bind(NewsConsumerInterface, NewsWatcher)
  
  news_watcher = di.resolve(NewsConsumerInterface) # type: ignore[type-abstract]
  
  assert isinstance(news_watcher, NewsWatcher)
  assert news_watcher.news_provider is bbc
  
def test_resolve_untyped_raises() -> None:
  di = DependencyInjector()
  di.bind(NewsProviderInterface, ITV)
  di.bind(NewsConsumerInterface, UntypedNewsWatcher)
  
  with pytest.raises(Exception):
    di.build(NewsContext)

def test_build_success() -> None:
  di = DependencyInjector()
  di.bind(NewsProviderInterface, ITV)
  di.bind(NewsConsumerInterface, NewsWatcher)
  context = di.build(NewsContext)
  
  assert isinstance(context, NewsContext)
  assert isinstance(context.provider, ITV)
  assert isinstance(context.consumer, NewsWatcher)
  
def test_build_not_dataclass_raises() -> None:
  di = DependencyInjector()
  di.bind(NewsProviderInterface, ITV)
  di.bind(NewsConsumerInterface, UntypedNewsWatcher)
  
  with pytest.raises(TypeError):
    di.build(NotADataclass)