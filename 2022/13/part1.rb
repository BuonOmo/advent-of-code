#!/usr/bin/env ruby

require "json"

input = ARGV[0] == "ex" ? "example" : "input"

pairs = IO.foreach(File.join(__dir__, input), chomp: true).chunk(&:empty?).reject(&:first).map(&:last)

def norm(val)
  if val.is_a?(String)
    JSON.parse(val)
  else
    val.dup
  end
end

def equalize(a, b)
  sa, sb = [a, b].map(&:size)
  a.concat([-1] * (sb - sa)) if sb > sa
  b.concat([-1] * (sa - sb)) if sa > sb
  [a, b]
end

def cmp(a, b)
  # p [:cmp, a, b]
  a = norm(a)
  b = norm(b)

  case [a, b]
  in [Integer, Integer]
    a <=> b
  in [Array, Array]
    p [:ary_ary, a, b] if $t
    a, b = equalize(a, b)
    p [:eq_done, a, b] if $t
    a.zip(b).each do |x, y|
      r = cmp(x, y)
      p [:cmp, x, y, r] if $te
      return r if r != 0
    end
    0
  in [-1, []] then -1
  in [[], -1] then 1
  else
    cmp(Array(a), Array(b))
  end
end

def test(a, b, ex)
  res = cmp(a, b)
  if res != ex
    p a, b, "#{res} != #{ex}"
    puts "=" * 50, nil
  end
end

# test([1, 1], [1, 2], -1)
# test([], [], 0)
# test([], [[]], -1)
# test([1], [[1]], 0)
# $t = true
# test([[1],[2,3,4]], [[1],4], -1)
# test([9], [[8,7,6]], 1)
els = pairs.flat_map { [JSON.parse(_1), JSON.parse(_2)] }
els.push([[2]], [[6]])

s= els.sort{ cmp(_1, _2) }

p (s.index([[2]]) + 1) * (s.index([[6]]) + 1)
