#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

result = IO.foreach(File.join(__dir__, input), chomp: true).count do |line|
  a,b,c,d=line.split(/[-,]/).map(&:to_i)
  ((a..b).cover?(c..d) || (c..d).cover?(a..b))
end

p result
