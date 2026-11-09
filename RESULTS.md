# API lab results
## Part 0
- Step 0.1, the number of pizza names: (ตัวเลขที่นับได้)
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: (ชื่อพิซซ่าที่ได้)
- Step 0.12, results of the three runs without a session (optional):
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, 3
## Defect report
- Title: Excluding all three tools makes POST /api/pizza answer 500
- Request: POST /api/pizza with token, body {"excludedTools": ["Knife","Pizza cutter","Scissors"]}
- Expected result: status 400 and a JSON error message
- Actual result: status 500 with an empty body
- Severity: Medium
## Part A
- Step A4, status codes when the other user reads, changes and deletes:
## Part B
1.
2.
3.
4.
5.
6.
7.
8.