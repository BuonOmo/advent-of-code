#!/usr/bin/env ruby

input = ARGV[0] == "ex" ? "example" : "input"

require "tqdm"

class Monkey
  attr_reader :items, :throw_count, :test_div

  def initialize(lines)
    @items = lines[1].scan(/\d+/).map(&:to_i)
    @op = lines[2].partition("=").last
    @test_div = lines[3][/\d+/].to_i
    @throws_to = lines[4, 2].map{_1[/\d+/].to_i}.then { |tru, fals| { true => tru,  false => fals } }
    @throw_count = 0
  end

  def inspect_and_throw
    item = @items.shift
    raise "no item" unless item

    @throw_count += 1
    item = run_op(item)
    item %= $max
    # item /= 3
    throws_to = @throws_to[item% @test_div == 0]
    $monkeys[throws_to].items.push(item)
  end

  private
  def run_op(old)
    eval @op
  end
end

$monkeys = IO.foreach(File.join(__dir__, input), chomp: true).
  chunk(&:empty?).
  reject(&:first).
  map(&:last).
  map{Monkey.new _1}


$max = $monkeys.map{_1.test_div}.reduce(:*)

count = 10_000

(0...count).tqdm.each do |round|
  $monkeys.each do |monkey|
    monkey.inspect_and_throw until monkey.items.empty?
  end
end

pp $monkeys.map(&:throw_count).max(2).reduce(:*)

