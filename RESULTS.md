# API lab results
## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Hard Siciliana
- Step 0.12, results of the three runs without a session (optional): run 1 failed (401 at login), run 2 failed (401 at login), run 3 passed.
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, 3
## Defect report
- Title: Excluding all three tools makes POST /api/pizza answer 500
- Request: POST /api/pizza with token, body {"excludedTools": ["Knife","Pizza cutter","Scissors"]}
- Expected result: status 400 and a JSON error message
- Actual result: status 500 with an empty body
- Severity: Medium
## Part A
- Step A4, status codes when the other user reads, changes and deletes: read 404 ({"error":"not found"}), update 400 ({"error":"rating ID ... not found"}), delete 400 ({"error":"rating ID ... not found"})
## Part B

1. Tests against a real server can find failures that come from the way the parts work together. For example, they found the load balancer problem in Step 0.12, where a login fails because it reaches a server that does not know the user, and they found the 500 error in Step 0.16, where the real code path crashes on an input that no stub would have simulated. They can also find wrong status codes, missing authentication checks and differences between documentation and real behavior. A unit test with stubs cannot see these, because its neighbours are replaced by fake ones. I would still write unit tests with stubs because they are fast, they give the same result on every run, they need no network, and when one fails it points to a single function instead of a whole system.

2. The public token abcdef0123456789 is shared by everyone, so the ratings made with it belong to everyone. Another student could change or delete my data while my test runs, and my test would fail for a reason that has nothing to do with the code. A new user with a unique name gives each test its own private data, so tests stay independent and can run in any order. In Project 2 I will apply the same idea to the shop or hotel: each test will create its own products, carts or bookings with unique names, use only that data, remove it in a fixture after the test, and never touch data that belongs to other groups.

3. QuickPizza runs on several servers behind a load balancer, and each server keeps its own users. A requests.Session stores the AWSALB cookie that the load balancer sends, and it sends the cookie back with every request. This keeps all requests of the test run on the same server, so a user created in one request can be found in the next one. In Step 0.12, [describe your three runs: how many logins failed and with which status]. Without the cookie, the requests were spread over different servers, so the result changed from run to run, which is what makes a test flaky.

4. The block with all three tools excluded revealed the defect. The two original inputs excluded only one tool each, so they belonged to the same block and never reached this case. A 500 with an empty body is worse than a 400 with a message for an app that calls the API. The 400 tells the app that its own input was wrong and explains why, so it can show the user a clear message. The 500 says only that the server failed, gives no reason, and forces the app to guess. An empty body can also make the JSON parsing in the app crash. The test stays in the suite as xfail because it documents a known defect and keeps the rest of the suite green. With strict=True, the run fails as soon as QuickPizza fixes the defect, which tells us to remove the mark, so the test also works as a regression test and as evidence for the defect report.

5. The model in Step A1 has characteristics with 3, 4, 2 and 3 blocks. Base choice coverage needs one base test, plus one test for each block that is not the base: 1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9 tests. All combinations coverage needs one test for every combination of blocks: 3 × 4 × 2 × 3 = 72 tests. Base choice therefore needs far fewer tests, and each test changes only one characteristic, so a failure points to the block that caused it.

6. When the other user tried to read, change and delete the rating, the API answered 404 for the read, 400 for the update and 400 for the delete. All three attempts were refused, and when I read the rating as its owner afterwards, nothing had changed, so the main security rule holds. I expected a 403 Forbidden, or a 404 Not Found for all three operations, because the rating exists but belongs to someone else. The codes I got differ from this expectation in two ways. First, the three operations do not agree: reading uses 404, while updating and deleting use 400. Second, 400 means that the input broke a rule, but the request body was valid, and the message says "rating ID ... not found", so 404 would describe the situation better. I consider this a minor defect, an inconsistency in error handling rather than a security hole. The data is protected, and the "not found" message does not reveal that the rating exists, which is good practice. The cost is that a client developer cannot rely on one status code for "this rating is not available to you", and a 400 may wrongly suggest that the app sent a bad request.

7. The request with the made-up token 0000000000000000 returned status 200 OK and a body with a list of 50 ratings, for example {"ratings":[{"id":1,"stars":5,"pizza_id":1}, ...]}. This is a defect. The same endpoint answered 401 when I sent no token at all (Step 0.3), so the server checks that an Authorization header is present, but it does not check that the token was really issued by a login. A correct API should answer 401 for any token that it did not issue. On a real system, a stranger could invent any token and read data that belongs to real users, such as orders, addresses or messages, without ever logging in. Because other operations may use the same weak check, the stranger might also create, change or delete data, which would break both confidentiality and integrity. I only read with this token and created or changed nothing, as the lab rules require.

8. An API test checks logic and data rules better than a test through the web pages, for example status codes, error messages, boundary values and permission checks, and it is faster and less fragile because it does not depend on the layout of the page. Only a test through the web pages can check what the user sees and does in the browser, for example that a button is visible, that a form shows an error message in the right place, or that the page works on a small screen.



# API lab

## Install and run
pip install -r requirements.txt
pytest -v

## Input domain model for POST /api/ratings

| Characteristic | Block | Value in tests | Test |
|---|---|---|---|
| C1 Value of stars | below 1 | 0 | test_stars_out_of_range[0] |
| C1 Value of stars | 1 to 5 (base) | 3 | test_base_choice_is_saved |
| C1 Value of stars | above 5 | 6 | test_stars_out_of_range[6] |
| C2 Type of stars | whole number (base) | 3 | test_base_choice_is_saved |
| C2 Type of stars | decimal | 3.5 | (กรอกหลัง A2) |
| C2 Type of stars | text | "3" | (กรอกหลัง A2) |
| C2 Type of stars | missing | no field | (กรอกหลัง A2) |
| C3 Pizza | exists (base) | a new pizza | test_base_choice_is_saved |
| C3 Pizza | does not exist | 999999999 | (กรอกหลัง A2) |
| C4 Token | the user's own (base) | from auth | test_base_choice_is_saved |
| C4 Token | none | no header | (กรอกหลัง A2) |
| C4 Token | wrong length | token short | (กรอกหลัง A2) |