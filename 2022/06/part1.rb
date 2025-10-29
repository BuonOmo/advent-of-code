#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

result = IO.read(File.join(__dir__, input)).chomp
i=0
c=4
result.chars.each_cons(c).find do |letters|
  i+=1
  letters.uniq.count == c
end
p i + c - 1
