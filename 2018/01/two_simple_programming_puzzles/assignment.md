# Question 1:

Write a function `solution(A)` that, given an array A consisting of N integers, returns the maximum among all non-positive integers.

For example, given array A as follows:
`[-6, -91, 1011, -100, 84, -22, 0, 1, 473]`
the function should return 0.

Assume that:

- N is an integer within the range [1..1,000];
- each element of array A is an integer within the range [−10,000..10,000];
- there is at least one element in array A which satisfies the condition in the task statement.

# Question 2:

Write a function `solution(N)` that, given a positive integer N, prints the consecutive numbers from 1 to N, each on a separate line.
However, any number divisible by 3, 5 or 7 should be replaced by the word Fizz, Buzz or Woof respectively.

If a number is divisible by more than one of the numbers: 3, 5 or 7, it should be replaced by a concatenation of the respective words
Fizz, Buzz and Woof in this given order. For example, numbers divisible by both 3 and 5 should be replaced by FizzBuzz and numbers
divisible by all three numbers: 3, 5 and 7, should be replaced by FizzBuzzWoof.

For example, here is the output for N = 24:

`1 2 Fizz 4 Buzz Fizz Woof 8 Fizz Buzz 11 Fizz 13 Woof FizzBuzz 16 17 Fizz 19 Buzz FizzWoof 22 23 Fizz`

The function shouldn't return any value.

You can print a string to the output (without or with the end-of-line character) as follows:

`sys.stdout.write("sample string") sys.stdout.write("whole line\n")`

Assume that:

N is an integer within the range `[1..1,000]`.