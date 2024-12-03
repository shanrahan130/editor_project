<?php
function testCommaCount($text, $expectedCount)
{
    $url = "http://localhost:5004/?text=" . urlencode($text);
    $response = file_get_contents($url);
    $data = json_decode($response, true);

    if ($data['answer'] === $expectedCount) {
        echo "Test Passed for text: '$text'. Expected: $expectedCount, Got: {$data['answer']} \n";
    } else {
        echo "Test Failed for text: '$text'. Expected: $expectedCount, Got: {$data['answer']} \n";
    }
}

// Running different test cases
testCommaCount("Hello, world, this is, a test", 3);  // Expected: 3 commas
testCommaCount("No commas here", 0);                 // Expected: 0 commas
testCommaCount("", 0);                                // Expected: 0 commas (empty string)
testCommaCount("This, is a, test", 2);                // Expected: 2 commas
testCommaCount("Special@#$%, characters!", 1);        // Expected: 1 comma
