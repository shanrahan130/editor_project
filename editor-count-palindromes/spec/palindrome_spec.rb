require_relative '../app'
require 'rspec'

RSpec.describe 'Palindrome Count' do
  it 'counts the number of palindromes - simple text' do
    text = 'madam racecar apple'
    expected = 2
    expect(count_palindromes(text)).to eq(expected)
  end

  it 'counts the number of palindromes - empty string' do
    text = ''
    expected = 0
    expect(count_palindromes(text)).to eq(expected)
  end

  it 'counts the number of palindromes - no palindromes' do
    text = 'hello world'
    expected = 0
    expect(count_palindromes(text)).to eq(expected)
  end

  it 'counts the number of palindromes - mixed text' do
    text = 'wow madam kayak notapalindrome'
    expected = 3
    expect(count_palindromes(text)).to eq(expected)
  end
end
