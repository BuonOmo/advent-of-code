#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

sum = 1
r = IO.read(input).split.map(&:to_i).map{sum += _1}
p (20..220).step(40).map { _1 * r[_1 - 2] }.sum
