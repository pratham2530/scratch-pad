# Traversing through a Fenwick tree

In the following, Least Significant Bit is abbreviated to LSB. 

### Why `LSB(i) = i & (-i)`

In two's complement, `-i = ~i + 1`, where `~` flips every bit of `i`. Adding
one to `~i` flips the `i - 1` bits to the right of the lowest set bit back to
zero, and flips that lowest bit itself back to one. So `i` and `-i` agree on
a single `1` bit (the position of `i`'s lowest set bit) and disagree on
every bit elsewhere. ANDing them together leaves the LSB.

## Proof: why `update()` jumps by `i += i & (-i)`

Starting from index `i`, find every index whose stored sum includes the
element at `i`.

1. Index `i` itself is the sum of `LSB(i)` numbers ending at `i`, so it
   trivially contains `i`.
1. Index i is the sum of LSB(i) numbers ending in i so the sum clearly
   contains i.
2. If an index j > i is the sum of numbers including i then

       j - LSB(j) < i <= j

   is needed. j = i + LSB(i) clearly satisfies the right inequality. The left
   inequality is equivalent to:

       LSB(i) < LSB(i + LSB(i)) = LSB(j).

   A bit-wise carry i.e. doing i += i & (-i) ensures
   j := i + i & (-i) is the least j satisfying LSB(j) > LSB(i).

## Proof: why `prefix_query()` jumps down `i -= i & (-i)`

`self.state[i]` is the sum of numbers in the interval `(i - LSB(i), i]` by
definition.

Defining `j := i - LSB(i)`, `self.state[j]` is the sum of numbers in the
interval

    (j - LSB(j), j] = (j - LSB(j), i - LSB(i)]

Since `j < i` and `LSB(i) >= 1`, the algorithm will terminate.

Letting `i_{n+1} = i_n - LSB(i_n)` where `i_0 = i`, there exists some
non-negative integer `k` such that the union

    ∪_{n=0}^{k} (i_{n+1}, i] = [1, n]

Hence, we can calculate the prefix sum up to index `i`.
