#!/usr/bin/env ruby

require "set"
require "algorithms"


input = ARGV[0] == "ex" ? "example" : "input"

$matrix = IO.foreach(File.join(__dir__, input), chomp: true).map(&:chars)
$graph = {}

$len = $matrix.first.length

class Node < Struct.new(:id, :value, :neighbors, :dist)
end

def to_id(i, j)
  i * $len + j
end

def node(i, j)
  raise if $matrix[i][j].nil?
  $graph[to_id(i, j)] ||= Node.new(to_id(i, j), $matrix[i][j], Set.new, Float::INFINITY)
end

def fill(a, b, reverse = true)
  return unless (a.value.ord - b.value.ord).abs <= 1

  a.neighbors.add b.id

  fill(b, a, false) if reverse
end

(0...$matrix.length).each do |i|
  (0...$matrix.first.length).each do |j|
    case $matrix[i][j]
    when "S"
      # $matrix[i][j] = "a"
      $start = [i, j]
    when "E"
      # $matrix[i][j] = "z"
      $end = [i, j]
    end

    curr = node(i, j)

    fill(curr, node(i-1, j)) if i > 0
    fill(curr, node(i, j-1)) if j > 0
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
    next unless h2 <= h + 1

    ns.push([a, b])
  end
  ns
end

def dijkstra(from_x, from_y, to_x, to_y)
  visited = Set.new
  current = $matrix[from_x][from_y]
  heap = Containers::MinHeap.new
  heap.push(0, [from_x, from_y])

  until heap.empty?
    dist = heap.next_key
    x, y = heap.pop
    next if visited.member?([x, y])

    visited.add([x, y])
    return dist if x == to_x and y == to_y

    neighbors(x, y).each { |neighbor| heap.push(dist + 1, neighbor) }
  end
end

p dijkstra(*$start, *$end)
