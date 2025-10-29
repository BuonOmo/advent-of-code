#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

require "ostruct"

init_state = OpenStruct.new(
  hc: 0,
  hl: 0,
  tc: 0,
  tl: 0
)

instructions = IO.foreach(File.join(__dir__, input), chomp: true).flat_map do |line|
  dir, n = line.split
  [dir] * n.to_i
end

$history = [init_state]

def apply(instruction, state)
  state = state.dup
  case instruction
  when "R" then state.hc += 1
  when "L" then state.hc -= 1
  when "U" then state.hl -= 1
  when "D" then state.hl += 1
  end

  dc = state.hc - state.tc
  dl = state.hl - state.tl

  if dc*dc + dl*dl > 2
    state.tc += dc <=> 0
    state.tl += dl <=> 0
  end

  $history << state
  state
end

r = instructions.reduce(init_state) { |state, ins| apply(ins, state) }

$lmin, $lmax = $history.flat_map { |st| [st.hl, st.tl] }.minmax
$cmin, $cmax = $history.flat_map { |st| [st.hc, st.tc] }.minmax

$lsize = $lmax - $lmin + 1
$csize = $cmax - $cmin + 1

result = $history.map { |st| [st.tl, st.tc] }.uniq.count
puts(result:)

def translate(state)
  state = state.dup
  state.hl -= $lmin
  state.tl -= $lmin
  state.hc -= $cmin
  state.tc -= $cmin
  state
end

$history.map! { |st| translate st }

# cursorup(n) CUU       Move cursor up n lines                 ^[[<n>A
# cursordn(n) CUD       Move cursor down n lines               ^[[<n>B
# cursorrt(n) CUF       Move cursor right n lines              ^[[<n>C
# cursorlf(n) CUB       Move cursor left n lines               ^[[<n>D


puts [nil]*$lsize
$history.each do |st|
  sleep 0.1
  print "\e[#{$lsize}A"
  matrix = Array.new($lsize) { "." * $csize }
  matrix[$history[0].hl][$history[0].hc] = "s"
  matrix[st.tl][st.tc] = "T"
  matrix[st.hl][st.hc] = "H"
  puts matrix
end
