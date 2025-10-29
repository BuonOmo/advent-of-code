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

# intructions are [from, to] arrays of one move.
instructions = instructions.flat_map { |line|
  line[/move (\d+) from (\d+) to (\d+)/]
  [[$2.to_i - 1, $3.to_i - 1]] * $1.to_i
}

# Play Game

instructions.each do
  game[_2].push game[_1].pop
end

puts game.map(&:last).join
