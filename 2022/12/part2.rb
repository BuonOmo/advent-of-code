#!/usr/bin/env ruby

require "set"
require "algorithms"


input = ARGV[0] == "ex" ? "example" : "input"

$matrix = IO.foreach(File.join(__dir__, input), chomp: true).map(&:chars)

(0...$matrix.length).each do |i|
  (0...$matrix.first.length).each do |j|
    case $matrix[i][j]
    when "S"
      $start = [i, j]
    when "E"
      $end = [i, j]
    end
  end
end

def height(x, y)
  return false if x < 0
  return false if y < 0

  case $matrix.dig(x, y)
  when nil then false # out of bound
  when "S" then 0
  when "E" then 25
  else
    $matrix[x][y].ord - ?a.ord
  end
end

def neighbors(x, y)
  h = height(x, y)
  ns = []
  [[-1, 0], [1, 0], [0, -1], [0, 1]].each do |dx, dy|
    a, b = x + dx, y + dy
    h2 = height(a, b)
    next unless h2
    next unless h <= h2 + 1

    ns.push([a, b])
  end
  ns
end

def dijkstra(from_x, from_y)
  visited = Set.new
  heap = Containers::MinHeap.new
  heap.push(0, [from_x, from_y])

  dists = []

  until heap.empty?
    dist = heap.next_key
    x, y = heap.pop
    next if visited.member?([x, y])

    visited.add([x, y])
    return dist if height(x, y) == 0

    neighbors(x, y).each { |neighbor| heap.push(dist + 1, neighbor) }
  end
end

p dijkstra(*$end)
