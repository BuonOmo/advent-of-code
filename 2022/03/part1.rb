# frozen_string_literal: true

r = IO.foreach("#{__dir__}/input", chomp: true).map(&:chars).sum do |line|
  s = line.size / 2
  ord = (line[0...s] & line[s..]).first.ord - ?a.ord + 1
  ord = ord + ?a.ord - ?A.ord + 26 if ord < 0
  ord
end
p r
# 7718 too low
