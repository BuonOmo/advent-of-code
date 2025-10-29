#!/usr/bin/env ruby

require "set"

input = ARGV[0] == "ex" ? "example" : "input"

result = IO.foreach(File.join(__dir__, input), chomp: true).map do |line|
  line.chars.map(&:to_i)
end

result = result.map.with_index do |line, i|
  line.map.with_index do |el, j|
    [el, i, j]
  end
end

is = Set.new

[ result, # (left-right)
  result.transpose, # (top-bottom)
  result.reverse.transpose, # (bottom-top)
  result.map{_1.reverse} ] # (right-left)
.each do |matrix|
  matrix.each do |line|
    max = -1
    line.each do |el, x, y|
      if el > max
        max = el
        is.add [x,y]
      end
    end
  end
end

p is.size
