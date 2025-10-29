# frozen_string_literal: true

def priority(letter)
  ord = letter.ord - ?a.ord + 1
  ord = ord + ?a.ord - ?A.ord + 26 if ord < 0
  ord
end

r = IO.foreach("#{__dir__}/input", chomp: true).map(&:chars).each_slice(3).sum do |lines|
  priority lines.reduce(:&).first
end
p r
# 7718 too low
