#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

sprite = 1
puts IO.read(input).split.map(&:to_i).map.with_index {
  diff = (sprite - (_2 % 40)).abs
  char = diff < 2 || diff > 38 ? ?# : ?.
  sprite = (sprite + _1) % 40
  char
}.each_slice(40).map(&:join)


x=1
c=[]
`dd`.split.map{c<<((c.size%40-x).abs<2??#:?.)
x+=_1.to_i}
c.each_slice(40){puts _1*""}
