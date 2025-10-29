#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

it = IO.foreach(File.join(__dir__, input), chomp: true)
game = it.take_while { !_1.empty? }
instructions = it.drop_while { !_1.empty? }.drop(1)

# Parse Game

size = game.last.split.size
game = game[0...-1].map { |line|
  size.times.map { |i| line[i * 4 + 1]  } # 1 5 9
}.reverse.transpose.map { |col| col.reject { _1 == " " } }

# Parse Instructions

# intructions are [num, from, to] arrays of one move.
instructions = instructions.map { |l|l.scan(/\d+/).map(&:to_i).then {[_1, _2 - 1, _3 - 1]} }

# Play Game

instructions.each do
  game[_3].push *game[_2].pop(_1)
end

puts game.map(&:last).join
