#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

AIR = "."
ROCK = "#"
SOURCE = "+"
SAND = "o"

## parse

paths = IO.foreach(File.join(__dir__, input), chomp: true).map do |line|
  line.scan(/\d+/).map(&:to_i).each_slice(2).to_a
end

start_c, start_r = 500, 0

min_c, max_c = [start_c, *paths.flatten(1).map(&:first)].minmax
min_r, max_r = [start_r, *paths.flatten(1).map(&:last)].minmax


## translate paths

paths.map! do |line|
  line.map { |c, r| [c - min_c, r - min_r] }
end

start_c -= min_c
start_r -= min_r

## fill matrix

matrix = Array.new(max_r - min_r + 1) { Array.new(max_c - min_c + 1, AIR) }

paths.each do |pts|
  pts.each_cons(2).each do |(c,r), (c2,r2)|
    if c == c2
      a,b = [r, r2].sort
      (a..b).each { |r| matrix[r][c] = ROCK }
    else
      a,b = [c, c2].sort
      (a..b).each { |c| matrix[r][c] = ROCK }
    end
  end
end

height = max_r - min_r + 1

def print_matrix(matrix)
  if false
    sleep 0.02
    print "\e[#{matrix.size}A"
    puts matrix.map { _1 * "" }
  end
end

matrix[start_r][start_c] = SOURCE

def fall(matrix, r, c, &block)
  return false if r >= matrix.size - 1

  matrix[r][c] = AIR
  r += 1

  if matrix[r][c] == AIR
    matrix[r][c] = SAND
    block.call matrix
    fall(matrix, r, c, &block)
  elsif matrix[r][c-1] == AIR
    matrix[r][c-1] = SAND
    block.call matrix
    fall(matrix, r, c-1, &block)
  elsif matrix[r][c+1] == AIR
    matrix[r][c+1] = SAND
    block.call matrix
    fall(matrix, r, c+1, &block)
  else
    matrix[r-1][c] = SAND
    return true
  end
end

print_matrix(matrix)
can_fall = true
count = 0
while can_fall
  count += 1
  can_fall = fall(matrix, start_r, start_c) do |step_matrix|
    print_matrix(step_matrix)
  end
end

puts count - 1
