#!/usr/bin/env ruby

require "set"
require "capture_mouse"

input = ARGV[0] == "ex" ? "example" : "input"

result = IO.foreach(File.join(__dir__, input), chomp: true).map do |line|
  line.chars.map(&:to_i)
end

def dbg(...)
  # print("DBG ", ...)
  # puts
end

$matrix = result

# [ result, # (left-right)
#   result.transpose, # (top-bottom)
#   result.reverse.transpose, # (bottom-top)
#   result.map{_1.reverse} ] # (right-left)
# .each do |matrix|
#   matrix.each do |line|
#     max = -1
#     line.each do |el, x, y|
#       if el > max
#         max = el
#         is.add [x,y]
#       end
#     end
#   end
# end

$size = size = result.size

def scenic_score(x, y)
  el = $matrix[x][y]
  # down (x-)
  down = (0...x).to_a.reverse.take_until { |nx| $matrix[nx][y] >= el }.size
  # up (x+)
  up = ((x+1)...$size).to_a.take_until { |nx| $matrix[nx][y] < el }.size
  # left (y-)
  left = (0...y).to_a.reverse.take_until { |ny| $matrix[x][ny] < el }.size
  # right (y+)
  right = ((y+1)...$size).to_a.take_until { |ny| $matrix[x][ny] < el }.size
  result = up * down * left * right
  dbg(x:, y:, el:, up:, down:, left:, right:, result:)
  result
end

def scenic_score(x, y)
  el = $matrix[x][y]
  # down (x-)
  tick = false
  down = (0...x).to_a.reverse.take_while { |nx| !tick && $matrix[nx][y] < el || (tick = !tick) }.size
  # up (x+)
  tick = false
  up = ((x+1)...$size).to_a.take_while { |nx| !tick && $matrix[nx][y] < el || (tick = !tick) }.size
  # left (y-)
  tick = false
  left = (0...y).to_a.reverse.take_while { |ny| #p [tick, x, ny, $matrix[x][ny], el]
    !tick && $matrix[x][ny] < el || (tick = !tick) }.size
  # right (y+)
  tick = false
  right = ((y+1)...$size).to_a.take_while { |ny| !tick && $matrix[x][ny] < el || (tick = !tick) }.size
  result = up * down * left * right
  dbg(x:, y:, el:, up:, down:, left:, right:, result:)
  result
end


p (0...$size).to_a.permutation(2).map { |x,y| scenic_score(x, y) }.max

# col, line = Termouse.cursor_pos
# puts IO.read(File.join(__dir__, input))
# ncol, nline = Termouse.get_click
# scenic_score(ncol,nline)
# scenic_score(3,2)
