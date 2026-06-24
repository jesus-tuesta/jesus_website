import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    path="/projects/multithreading",
    name="Multithreading on C++",
)

layout = dmc.Container(
    children=[
        dmc.Title("Multithreading on C++", order=1),
        dmc.Space(h=30),
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Badge("C++", size="lg", variant="dot"),
                        dmc.Badge("multithreading", size="lg", variant="dot"),
                        dmc.Badge("asynchronous programming", size="lg", variant="dot"),
                        dmc.Badge("lock free programming", size="lg", variant="dot"),
                    ]
                ),
                dmc.Text("Published: Jun 25, 2026", style={"color": "#555"}, size="sm"),
            ]
        ),
        dmc.Space(h=30),
        dmc.Card(
            children=[
                dmc.Group(
                    [
                        dmc.Text("Project Repository", size="sm"),
                        dmc.Anchor(
                            "View on GitHub",
                            href="https://github.com/andergod/OrderBookSimulator.git",
                            target="_blank",
                            variant="gradient",
                            gradient={"from": "indigo", "to": "cyan"},
                        ),
                    ],
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            p="md",
        ),
        dmc.Space(h=30),
        # Introduction – three parts
        dmc.Stack(
            [
                dmc.Title("Three Approaches to Concurrency", order=2),
                dmc.Text(
                    """This page explores three distinct approaches to handling concurrent workloads in C++,
                    each with its own trade-offs in complexity, performance, and expressiveness. My orderbook that 
                    connnects to exchange through I/O and processes data in real-time works as a 
                    simple producer–consumer channel as a good small example to showcase the differences.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.List(
                    [
                        dmc.ListItem("Part 1 — Asynchronous with Boost.ASIO"),
                        dmc.ListItem("Part 2 — Classic lock‑based multithreading"),
                        dmc.ListItem("Part 3 — Lock‑free with memory ordering"),
                    ],
                    withPadding=True,
                    style={"marginBottom": 10},
                ),
            ]
        ),
        dmc.Space(h=40),
        # =========================================================================
        # PART 1 – ASYNCHRONOUS PROGRAMMING WITH BOOST.ASIO
        # =========================================================================
        dmc.Stack(
            [
                dmc.Title("Part 1: Asynchronous Programming with Boost.Asio", order=2),
                dmc.Text(
                    """
                    I've been working with Boost for a while so the Asio library felt like the
                    natural next step. However,                     in hindsight I would think it was a mistake,
                    the internet is full of examples for other classical multithreading but
                    not so much for Asio.
                    It felt very low level, and the good news is that once you get it running
                    you can actually see and understand a bit more about how they handle async
                    programming and the use of coroutines. 
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                # Key concepts
                dmc.Title("Key Concepts", order=3),
                dmc.Text(
                    """Before diving into the channel implementation, it is helpful to understand
                    the main building blocks Asio exposes:""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.List(
                    [
                        dmc.ListItem(
                            [
                                dmc.Text(
                                    "io_context — ",
                                    span=True,
                                    style={"fontWeight": 600},
                                ),
                                dmc.Text(
                                    "the event loop that polls for completed operations and invokes their handlers.",
                                    span=True,
                                ),
                            ]
                        ),
                        dmc.ListItem(
                            [
                                dmc.Text(
                                    "any_io_executor — ",
                                    span=True,
                                    style={"fontWeight": 600},
                                ),
                                dmc.Text(
                                    "a wrapper around an execution context; it handles posting handlers and managing the order of execution.",
                                    span=True,
                                ),
                            ]
                        ),
                        dmc.ListItem(
                            [
                                dmc.Text(
                                    "awaitable<T> — ",
                                    span=True,
                                    style={"fontWeight": 600},
                                ),
                                dmc.Text(
                                    "the coroutine return type. A function returning awaitable<T> can use co_await to suspend without blocking a thread.",
                                    span=True,
                                ),
                            ]
                        ),
                        dmc.ListItem(
                            [
                                dmc.Text(
                                    "deque<any_completion_handler<void()>> — ",
                                    span=True,
                                    style={"fontWeight": 600},
                                ),
                                dmc.Text(
                                    """A queue of handlers representing the continuation of a suspended coroutine. Storing a handler so the coroutine can be resumed later.
                                    I see it as a way to store what we'll do next, and when we have the resources to do it, we can resume it.""",
                                    span=True,
                                ),
                            ]
                        ),
                        dmc.ListItem(
                            [
                                dmc.Text(
                                    "co_await/co_return ",
                                    span=True,
                                    style={"fontWeight": 600},
                                ),
                                dmc.Text(
                                    """Keywords used to suspend and resume coroutines. co_await suspends the coroutine until the awaited operation completes,
                                    while co_return returns a value from the coroutine.""",
                                    span=True,
                                ),
                            ]
                        ),
                    ],
                    withPadding=True,
                    style={"marginBottom": 10},
                ),
                dmc.Title("The Channel Abstraction", order=3),
                dmc.Text(
                    """The channel template below implements our bar generation system. Both send()
                    and receive() are coroutines that suspend when the channel is full or empty,
                    respectively, and resume when the opposite side makes progress.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """When the queue reaches capacity, send() stores its completion handler in
                    waiting_senders_ and suspends. Later, when receive() pops an element, it
                    wakes one waiting sender by posting its handler onto the executor. The same
                    logic applies in reverse when the queue is empty and a receiver must wait.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """Key design points:""",
                    style={"textAlign": "justify", "marginBottom": 5},
                ),
                dmc.List(
                    [
                        dmc.ListItem(
                            "No threads are blocked while waiting — the coroutine is suspended, and the thread is free to process other work."
                        ),
                        dmc.ListItem(
                            "Handlers are posted via boost::asio::post to ensure they run on the correct executor."
                        ),
                    ],
                    withPadding=True,
                    style={"marginBottom": 10},
                ),
                dcc.Markdown("""
```cpp
#include <boost/asio.hpp>
#include <boost/asio/any_completion_handler.hpp>
#include <boost/asio/any_io_executor.hpp>
#include <boost/asio/awaitable.hpp>
#include <boost/asio/post.hpp>
#include <boost/asio/use_awaitable.hpp>

#include <deque>
#include <iostream>
#include <queue>

template<typename T>
class channel {
public:
  explicit channel(boost::asio::any_io_executor ex, std::size_t capacity)
    : ex_(ex), capacity_(capacity)
  {
  }

  boost::asio::awaitable<void> send(T value)
  {
    if (queue_.size() >= capacity_) {
      std::cout << "Exceed capacity push out and save data" << std::endl;
      co_await boost::asio::
        async_initiate<const boost::asio::use_awaitable_t<>&, void()>(
          [this](auto handler) {
            waiting_senders_.push_back(std::move(handler));
          },
          boost::asio::use_awaitable);
    }

    std::cout << "Saving message on queue" << std::endl;
    queue_.push(std::move(value));

    if (!waiting_receivers_.empty()) {
      std::cout << "If we have any receiver, wake up and send data"
                << std::endl;
      auto h = std::move(waiting_receivers_.front());
      waiting_receivers_.pop_front();
      boost::asio::post(ex_, [h = std::move(h)]() mutable { std::move(h)(); });
    }
  }

  boost::asio::awaitable<T> receive()
  {
    if (queue_.empty()) {
      std::cout << "Nothing on queue, send handler to waiting_receiver, and go "
                   "back to send"
                << std::endl;
      co_await boost::asio::
        async_initiate<const boost::asio::use_awaitable_t<>&, void()>(
          [this](auto handler) {
            waiting_receivers_.push_back(std::move(handler));
          },
          boost::asio::use_awaitable);
    }
    std::cout << "Take value out of channel and sent it " << std::endl;
    T value = std::move(queue_.front());
    queue_.pop();

    if (!waiting_senders_.empty()) {
      auto h = std::move(waiting_senders_.front());
      std::cout << "If we have any sender, wake up and send data" << std::endl;
      waiting_senders_.pop_front();
      boost::asio::post(ex_, [h = std::move(h)]() mutable { std::move(h)(); });
    }

    co_return value;
  }

private:
  boost::asio::any_io_executor                            ex_;
  std::size_t                                             capacity_;
  std::queue<T>                                           queue_;
  std::deque<boost::asio::any_completion_handler<void()>> waiting_senders_;
  std::deque<boost::asio::any_completion_handler<void()>> waiting_receivers_;
};
```
                """),
            ]
        ),
        dmc.Space(h=50),
        # =========================================================================
        # PART 2 – LOCK-BASED MULTITHREADING
        # =========================================================================
        dmc.Stack(
            [
                dmc.Title("Part 2: Lock‑Based Multithreading", order=2),
                dmc.Text(
                    """The lock‑based version of the channel replaces Asio's coroutine suspension
                    with straightforward blocking on a std::condition_variable. Despite working
                    with classical multithreading, the resulting code is simpler — no coroutine
                    machinery, no executors, no completion handlers.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Title("How It Works", order=3),
                dmc.Text(
                    """send_impl acquires the mutex via std::unique_lock, then calls
                    not_full.wait(lock, predicate). The predicate checks that the queue is
                    below capacity or that the channel has been closed. If the predicate is
                    false the thread is suspended and the mutex is released atomically. When
                    a consumer pops an item, it calls not_full.notify_one(), which wakes a
                    waiting producer, who re‑acquires the lock and re‑checks the predicate.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """receive_impl mirrors the same pattern on the not_empty condition
                    variable. The done flag and the predicate guards together ensure that
                    spurious wake‑ups do not cause incorrect behaviour — the thread simply
                    re‑evaluates the condition and sleeps again if necessary.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Title("Key Design Points", order=3),
                dmc.List(
                    [
                        dmc.ListItem(
                            "RAII lock guards (unique_lock / lock_guard) guarantee the mutex is released even if an exception is thrown."
                        ),
                        dmc.ListItem(
                            "The predicate overload of condition_variable::wait eliminates the need for an explicit while loop against spurious wake‑ups."
                        ),
                        dmc.ListItem(
                            "Two separate condition variables (not_full, not_empty) avoid waking all threads when only one side can make progress."
                        ),
                        dmc.ListItem(
                            "The done flag provides a clean shutdown path: close_impl() sets done and notifies all waiters, causing them to exit."
                        ),
                        dmc.ListItem(
                            "std::atomic counters track producer/consumer activity without adding lock contention."
                        ),
                    ],
                    withPadding=True,
                    style={"marginBottom": 10},
                ),
                dcc.Markdown("""
```cpp
template<typename T>
class channel_lock_based : public channel_interface<channel_lock_based<T>, T> {
public:
  channel_lock_based(std::size_t capacity)
    : channel_interface<channel_lock_based<T>, T>(capacity)
  {
  }

  void send_impl(T value)
  {
    std::unique_lock<std::mutex> lock{mtx};
    not_full.wait(
      lock, [this] { return queue_.size() < this->capacity_ || done; });
    if (done)
      return;
    queue_.push(std::move(value));
    not_empty.notify_one();
    producer_count++;
  }

  bool receive_impl(T& out)
  {
    std::unique_lock<std::mutex> lock{mtx};
    not_empty.wait(lock, [this] { return !queue_.empty() || done; });
    if (queue_.empty() && done)
      return false;

    out = std::move(queue_.front());
    queue_.pop();
    not_full.notify_one();
    consumer_count++;

    return true;
  }

  thread_info current_status_impl()
  {
    return thread_info{
      std::chrono::steady_clock::now(),
      consumer_count,
      producer_count,
      this->size_impl()};
  }

  void close_impl()
  {
    std::lock_guard<std::mutex> lock{mtx};
    done = true;
    not_full.notify_all();
    not_empty.notify_all();
  }

  std::size_t size_impl()
  {
    std::lock_guard<std::mutex> lock{mtx};
    return queue_.size();
  }

  bool empty_impl()
  {
    std::lock_guard<std::mutex> lock{mtx};
    return queue_.empty();
  }

private:
  std::queue<T>           queue_;
  std::condition_variable not_full;
  std::condition_variable not_empty;
  bool                    done{false};
  std::mutex              mtx;
  std::atomic<int>        producer_count;
  std::atomic<int>        consumer_count;
};
```
                """),
                dmc.Space(h=20),
                dmc.Title(
                    "Lock‑Based vs. Asio: a Different Kind of Simplicity", order=3
                ),
                dmc.Text(
                    """The lock‑based channel is undeniably easier to read and maintain. I
                    grasp the concept of std::mutex and std::condition_variable way easier than
                    coroutine mechanics or executor models. The compile‑time
                    is lower (I will always complain about boost compile times) 
                    the binary is smaller, and there are no external dependencies
                    beyond the standard library.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """The trade‑off is that threads block. A blocked thread freezes while it sleeps,
                    it cannot be reused for other work. In a
                    highly concurrent system with many channels, this can lead to thread
                    explosion or excessive context switching. The Asio version, by contrast,
                    lets a single thread multiplex many thousands of channels because suspended
                    coroutines are just memory, they do not occupy a thread.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
            ]
        ),
        dmc.Space(h=50),
        # =========================================================================
        # PART 3 – LOCK-FREE PROGRAMMING
        # =========================================================================
        dmc.Stack(
            [
                dmc.Title(
                    "Part 3: Lock‑Free Programming with Memory Ordering", order=2
                ),
                dmc.Text(
                    """Finally, the third method I tried was the lock‑free version
                    which eliminates blocking entirely. There are no mutexes, no
                    condition variables — just std::atomic counters and careful use of the C++
                    memory model. This is an SPSC (single producer, single consumer) bounded queue.
                    Because there is only one writer and one reader, each side can advance
                    its own atomic index without contention.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """In order to not change the code each time, I implemented a CRTP-based approach
                    where the implementation is chosen based on a config variable. This allows me to reuse the
                    same interface and just swap the implementation. The lock free version
                    is a bit more verbose and requires more handholding, but it's a good exercise to understand
                    your code at each step.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Title("Memory Ordering: the Core Idea", order=3),
                dmc.Text(
                    """Each atomic operation carries a memory order tag that specifies what
                    visibility guarantees the compiler and CPU must enforce:""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.List(
                    [
                        dmc.ListItem(
                            "memory_order_relaxed — no ordering constraints beyond atomicity. Used here for the local slot computation and the close flag."
                        ),
                        dmc.ListItem(
                            "memory_order_acquire — reads that see the effects of a matching release on another thread. Used when loading tail from the producer side to check queue fullness safely."
                        ),
                        dmc.ListItem(
                            "memory_order_release — writes that become visible to a thread that does an acquire on the same variable. Used when publishing the new tail after storing into the buffer."
                        ),
                    ],
                    withPadding=True,
                    style={"marginBottom": 10},
                ),
                dmc.Text(
                    """The acquire/release pairing between the producer's tail.fetch_add(...,
                    release) and the consumer's tail.load(acquire) ensures that when the
                    consumer sees an updated tail, the corresponding channel writes are also
                    visible. The same pairing works in reverse for the head index.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """The cost of this method is verbosity and correctness difficulty. The memory ordering
                    tags must be chosen precisely; too weak and you get data races, too strong
                    and you pay unnecessary fencing costs. This implementation uses
                    std::this_thread::yield() as a back‑off strategy when the queue is full or
                    empty, which is a simple compromise between busy‑waiting and blocking.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """Key limitations: this is strictly SPSC. A multi‑producer or multi‑consumer
                    variant would require a more sophisticated protocol (e.g. CAS loops, hazard
                    pointers, or epoch‑based reclamation) and is considerably harder to get
                    right.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown("""
```cpp
template<typename T>
class channel_lock_free : public channel_interface<channel_lock_free<T>, T> {
public:
  channel_lock_free(std::size_t capacity)
    : channel_interface<channel_lock_free<T>, T>(capacity)
  {
    buffer.resize(capacity);
  }

  void send_impl(T value)
  {
    while (tail.load(std::memory_order_relaxed)
             - head.load(std::memory_order_acquire)
           >= static_cast<std::ptrdiff_t>(this->capacity_)) {
      if (done.load(std::memory_order_acquire))
        return;
      std::this_thread::yield();
    }
    auto slot    = tail.load(std::memory_order_relaxed) % this->capacity_;
    buffer[slot] = std::move(value);
    tail.fetch_add(1, std::memory_order_release);
    producer_count++;
  }

  bool receive_impl(T& out)
  {
    while (head.load(std::memory_order_relaxed)
           == tail.load(std::memory_order_acquire)) {
      if (done.load(std::memory_order_acquire))
        return false;
      std::this_thread::yield();
    }
    auto slot = head.load(std::memory_order_relaxed) % this->capacity_;
    out       = std::move(buffer[slot]);
    head.fetch_add(1, std::memory_order_release);
    consumer_count++;
    return true;
  }

  thread_info current_status_impl()
  {
    return thread_info{
      std::chrono::steady_clock::now(),
      consumer_count.load(std::memory_order_relaxed),
      producer_count.load(std::memory_order_relaxed),
      tail.load(std::memory_order_relaxed)
        - head.load(std::memory_order_relaxed)};
  }

  void close_impl()
  {
    done.store(true, std::memory_order_relaxed);
  }

private:
  std::vector<T>       buffer;
  std::atomic<size_t>  head{0};
  std::atomic<size_t>  tail{0};
  std::atomic<bool>    done{false};
  std::atomic<int32_t> producer_count{};
  std::atomic<int32_t> consumer_count{};
};
```
                """),
                dmc.Space(h=20),
                dmc.Title("Putting It All Together", order=3),
                dmc.Text(
                    """These three implementations: Asio async, lock‑based, and lock‑free,
                    solve the same problem with very different trade‑offs. The Asio version
                    composes well in asynchronous workflows but requires very specific Asio knowledge. 
                    The lock‑based version is the simplest to read and maintain but
                    pays context‑switch overhead under contention. The lock‑free version avoids
                    kernel freezes entirely but is restricted to SPSC and demands a precise
                    understanding of your code logic.""",
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
            ]
        ),
    ],
    size="xl",
    style={"padding": "2rem"},
)
