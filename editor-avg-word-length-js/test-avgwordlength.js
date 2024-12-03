var expect = require('chai').expect;
var avgWordLength = require('../avgWordLength');

it('Average Word Length Test - Simple Text', function() {
    var t = "this is a test";
    var expected = 3.5;
    expect(avgWordLength.calculate(t)).to.equal(expected);
});

it('Average Word Length Test - Empty String', function() {
    var t = "";
    var expected = 0;
    expect(avgWordLength.calculate(t)).to.equal(expected);
});

it('Average Word Length Test - Special Characters Only', function() {
    var t = "@#$% ^^&*";
    var expected = 0;
    expect(avgWordLength.calculate(t)).to.equal(expected);
});
