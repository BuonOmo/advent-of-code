#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

cmds = IO.read(File.join(__dir__, input), chomp: true).split("$").drop(2)

path = ["base"]
data = Hash.new(0)
cmds.each do |cmd|
  if cmd.start_with?(" ls")
    data[path * ?/] += cmd.scan(/\d+/).sum{_1.to_i}
  elsif cmd.start_with?(" cd ..")
    data[path[0...-1] * "/"] += data[path * ?/]
    path.pop
  else
    dir = cmd[/^ cd (\w+)/, 1]
    path.push dir
  end
end


while path.size > 1
  data[path[0...-1] * "/"] += data[path * ?/]
  path.pop
end

p data.values.select { _1 <= 100_000 }.sum
