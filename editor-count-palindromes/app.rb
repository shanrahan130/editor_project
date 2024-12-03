require 'sinatra'
require 'json'

before do
  # Add CORS headers to allow cross-origin requests
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
end

get '/' do
  text = params['text'] || ""
  words = text.split(" ")
  count = words.select { |word| word.downcase == word.downcase.reverse }.count

  response = {
    error: false,
    string: "Contains #{count} palindromes",
    answer: count
  }

  content_type :json
  response.to_json
end

set :bind, '0.0.0.0'
set :port, 80
