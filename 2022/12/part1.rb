#!/usr/bin/env ruby

require "set"

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
      $matrix[i][j] = "a"
      $start = [i, j]
    when "E"
      $matrix[i][j] = "z"
      $end = [i, j]
    end

    curr = node(i, j)

    fill(curr, node(i-1, j)) if i > 0
    fill(curr, node(i, j-1)) if j > 0
  end
end

def dijkstra(from_x, from_y, to_x, to_y)
  unvisited = Set.new($graph.values.map(&:id))
  current = $graph[to_id(from_x, from_y)]
  current.dist = 0
  until unvisited.map(&$graph).all?{_1.dist == Float::INFINITY}
    # p current.dist
    current.neighbors.map(&$graph).select{unvisited.member? _1.id}.each do |neighbor|
      neighbor.dist = [neighbor.dist, current.dist + 1].min
    end
    break if current.id == to_id(to_x, to_y)
    unvisited.delete current.id
    current = unvisited.map(&$graph).min_by{_1.dist}
  end
  # pp unvisited.map(&$graph).map(&:dist).uniq
end

dijkstra(*$start, *$end)
# dijkstra(*$end, *$start)
# pp $graph.reject{_2.dist == Float::INFINITY}
# pp $start, $end
# pp $graph[to_id(*$start)]


def show_neighbors(id)
  pp({ me: $graph[id] })
  pp({ left: $graph[id-1]})
  pp({ right: $graph[id+1]})
  pp({ top: $graph[id-$len]})
  pp({ bottom: $graph[id+$len]})
end


# show_neighbors(6136)

(0...$matrix.length).each do |i|
  (0...$matrix.first.length).each do |j|
    n = node(i, j)
    sid = to_id(*$start)
    eid = to_id(*$end)
    case [to_id(i, j), n.value]
    in [^sid, *]
      print "\e[31mS\e[0m"
    in [^eid, *]
      print "\e[32mE\e[0m"
    in [*, /o/i]
      print n.dist == Float::INFINITY ? "\e[35m#{n.value.upcase}\e[0m" : n.value
    else
      print n.dist == Float::INFINITY ? "\e[34m#{n.value.upcase}\e[0m" : n.value
    end
  end
  puts
end

# TODO: diff between matrix and actual original to see if any issue -> no diff

# IO.write("my", $matrix.map{_1 * ""} * "\n")

pp $graph.values.map(&:dist).reject(&{Float::INFINITY => true}).max

# 531 (total) too high
# 379 (from start to max) too low
