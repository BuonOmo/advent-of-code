#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

require "ostruct"

# from head to tail
init_state = Array.new(10) { OpenStruct.new(c: 0, l: 0) }

instructions = IO.foreach(File.join(__dir__, input), chomp: true).flat_map do |line|
  dir, n = line.split
  [dir] * n.to_i
end

$history = [init_state]

def apply(instruction, state)
  state = state.map(&:dup)

  case instruction
  when "R" then state[0].c += 1
  when "L" then state[0].c -= 1
  when "U" then state[0].l -= 1
  when "D" then state[0].l += 1
  end

  (1...state.size).each do |i|
    dc = state[i-1].c - state[i].c
    dl = state[i-1].l - state[i].l

    if dc*dc + dl*dl > 2
      state[i].c += dc <=> 0
      state[i].l += dl <=> 0
    end
  end

  state
end

# If not for the viz, we could just store tail positions.
$history = instructions.reduce([init_state]) { |acc, ins| [*acc, apply(ins, acc.last)] }

$lmin, $lmax = $history.flat_map { |st| st.map(&:l) }.minmax
$cmin, $cmax = $history.flat_map { |st| st.map(&:c) }.minmax

$lsize = $lmax - $lmin + 1
$csize = $cmax - $cmin + 1

result = $history.map { |st| [st[-1].l, st[-1].c] }.uniq.count
puts(result:)

def translate(state)
  state.map do |pair|
    pair.l -= $lmin
    pair.c -= $cmin
    pair
  end
end

$history.map! { |st| translate st }

puts [nil]*$lsize
$history.each do |st|
  sleep 0.1
  print "\e[#{$lsize}A"
  matrix = Array.new($lsize) { "." * $csize }
  matrix[$history[0][0].l][$history[0][0].c] = "s"
  (1...st.size).each do |i|
    matrix[st[i].l][st[i].c] = i.to_s
  end
  matrix[st[0].l][st[0].c] = "H"
  puts matrix
end
