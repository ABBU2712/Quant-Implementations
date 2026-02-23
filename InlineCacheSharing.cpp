//False sharing significantly degrades performance in low-latency trading systems by triggering excessive cache coherence traffic when threads modify independent variables on the same cache line. Mitigating this requires explicit memory alignment to ensure frequently updated atomic counters reside in separate cache lines.

//Task
//Implement a struct named CacheAlignedCounters containing two public std::atomic<int> members, a and b, both initialized to 0. Apply alignas using std::hardware_destructive_interference_size (or a fallback of 64 bytes if the constant is unavailable) to ensure the memory addresses of a and b are separated by at least the size of a CPU cacheline.


include <atomic>
#include <new>      // std::hardware_destructive_interference_size (if available)
#include <cstddef>  // std::size_t
#include <cstdint>  // std::uint8_t

#if defined(__cpp_lib_hardware_interference_size) && (__cpp_lib_hardware_interference_size >= 201703L)
inline constexpr std::size_t kCacheLineBytes = std::hardware_destructive_interference_size;
#else
inline constexpr std::size_t kCacheLineBytes = 64;
#endif

struct CacheAlignedCounters {
public:
    alignas(kCacheLineBytes) std::atomic<int> a{0};

private:
    // Pad so that b starts at least one cache line after a.
    // (We align b too, to guarantee it begins on a cache line boundary.)
    static constexpr std::size_t kPad =
        (kCacheLineBytes > sizeof(std::atomic<int>)) ? (kCacheLineBytes - sizeof(std::atomic<int>)) : 0;
    alignas(kCacheLineBytes) std::uint8_t pad[kPad]{};

public:
    alignas(kCacheLineBytes) std::atomic<int> b{0};
};
