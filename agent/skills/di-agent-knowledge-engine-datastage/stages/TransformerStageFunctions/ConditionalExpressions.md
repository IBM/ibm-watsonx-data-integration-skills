# DataStage Transformer Conditional Expressions

Reference for inline conditional (If...Then...Else) expressions in the Transformer stage

### If...Then...Else

- **Description**: Evaluates a boolean condition and returns one of two values depending on whether the condition is true or false. This is not a function call but a language construct used directly in the Derivation field of a Transformer stage output column.
- **Usage**: `If <condition> Then <true-value> Else <false-value>`
- **Notes**:
  - Keywords `If`, `Then`, and `Else` are case-insensitive (`IF`/`if`/`If` are all accepted).
  - The `Else` clause is **required**. Every `If...Then` must have a matching `Else`.
  - Conditions support standard comparison operators: `=`, `!=`, `<`, `>`, `<=`, `>=`.
  - Logical operators `And`, `Or`, and `Not` can combine multiple conditions.
  - Parentheses can be used to group conditions for clarity or to control evaluation order.
  - The true-value and false-value can be literals, column references, arithmetic expressions, or calls to other Transformer functions.
- **Example**: If mylink.score contains the score of an exam, the following expression assigns a pass/fail label: `If mylink.score >= 50 Then 'Pass' Else 'Fail'`

---

### Nested If...Then...Else

- **Description**: `If...Then...Else` can be nested to any depth. An `Else` branch can open a new `If...Then...Else` (chained else-if), and a `Then` branch can do the same (hierarchical nesting). Both styles can be combined freely.
- **Usage**:
  - Chained: `If <condition1> Then <value1> Else If <condition2> Then <value2> Else <default-value>`
  - Hierarchical: `If <condition1> Then If <condition2> Then <value1> Else <value2> Else <value3>`
- **Notes**:
  - Each `Else If` is evaluated only when all preceding conditions were false.
  - Each inner `Then If` is evaluated only when its outer `Then` branch is reached.
  - The final `Else` acts as the default/fallback for the entire chain.
  - Parentheses around nested conditions are optional but recommended for readability.
  - Deeply nested expressions reduce readability; consider stage variables to break up complex logic.
- **Examples**:
  - Three-tier classification: `If Link_1.CustomerSpending > 10000 Then 'High' Else If Link_1.CustomerSpending >= 5000 Then 'Medium' Else 'Low'`
  - Hierarchical reward points: `If Link_1.MonthlyIncome > 2500 And Link_1.QuarterlySpend > 4000 Then If Link_1.BadgeType = 'platinum' Then Link_1.AmountSpend * 1.5 Else If Link_1.BadgeType = 'diamond' Then Link_1.AmountSpend * 1.3 Else If Link_1.BadgeType = 'gold' Then Link_1.AmountSpend * 1.1 Else Link_1.AmountSpend Else If Link_1.MonthlyIncome < 2500 And Link_1.QuarterlySpend > 4000 Then Link_1.AmountSpend * 0.75 Else Link_1.AmountSpend * 0.25`

---

### If...Then...Else with Function Calls

- **Description**: The condition, true-value, or false-value can each be any valid Transformer expression, including calls to built-in functions such as `IsNull`, `Len`, `Contains`, `RegexMatch`, date functions, and others.
- **Usage**: `If <function-call> Then <value> Else <value>`
- **Examples**:
  - Null guard: `If IsNull(Link_1.StartTime) Or IsNull(Link_1.EndTime) Then -1 Else SecondsSinceFromTimestamp(Link_1.StartTime, Link_1.EndTime)`
  - String validation: `If Contains(Link_1.CustomerEmail, '@') And (EndsWith(Link_1.CustomerEmail, '.com') Or EndsWith(Link_1.CustomerEmail, '.org')) Then 1 Else 0`
  - Date comparison: `If DaysSinceFromDate(CurrentDate(), Link_1.OrderDate) > 30 Then 'Overdue' Else 'On Time'`
  - Environment variable: `If Link_1.OrderValue < GetEnvironment('MAX_THRESHOLD') Then Link_1.OrderValue * 3 Else Link_1.OrderValue`
