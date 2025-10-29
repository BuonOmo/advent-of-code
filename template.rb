#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

result = IO.foreach(File.join(__dir__, input), chomp: true).map do |line|
end

p result
