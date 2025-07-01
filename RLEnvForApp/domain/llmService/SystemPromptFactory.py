# TODO: prompt add action

class SystemPromptFactory:
    @staticmethod
    def _escape_all_braces(origin_str:str) -> str:
        return origin_str.replace("{", "{{").replace("}", "}}")

    @staticmethod
    def get(selector) -> str:
        if selector == "is_submit_button":
            return "{form_info}\n" + \
                   "You are an AI web crawler assistant.\n" + \
                   "Follow the user requirements carefully and The user will give you some web elements.\n" + \
                   "Please answer it is a form submitting button.\n" + \
                   "Please only say yes or no."
        elif selector == "is_form_submitted":
            return "{form_info}\n" + \
                   "You are an AI web crawler assistant.\n" + \
                   "Follow the user requirements carefully and The user will prompt you for the DOM differences before and after submitting the web form.\n" + \
                   "Please answer whether the form was submitted successfully.\n" + \
                   "Please only say yes or no."
        elif selector == "get_input_values":
            return SystemPromptFactory._escape_all_braces("""You are an expert in software testing, web application testing, and ISP-based test input generation.
Your task is to generate a **minimal yet powerful set of web form test cases.** Each test case represents a complete, **logically coherent** form submission, and the entire set must achieve **Each-Choice Criteria**. These inputs should **maximize code coverage** and **uncover edge-case bugs**.

# Rules:
- **Avoid reuse canned or generic values** (e.g., "abc", "123", "test").
- **Only use semantically meaningful and realistic inputs** (e.g., plausible names, formats, intents).
- **Minimize test case count** while achieving **Each-Choice Criteria**.
- **Ensure cross-field logical coherence for every test case.**
- **Each value must be realistic and executable** in actual web form submissions.
- **Prioritize Boundaries and Exceptions**: While satisfying the Each-Choice Criteria, prioritize input values that test boundary conditions, error-handling routines, and special formats to maximize the probability of discovering latent defects.

# Steps
## Step 1: Identify Input Characteristics
For each **provided field XPath** in the `{Provided Field XPaths}` list:
- Based on its context within the `{Form DOM Hierarchy}`, identify a **minimal**, **non-overlapping**, **field-type-appropriate** set of **Input Characteristics**.
- Each characteristic reflects a **distinct behavioral category** that users might input.
- Choose only relevant dimensions per field (e.g., format for emails, range for ages).
- Avoid redundancy.
#### **Interface-Based Approach** (Syntactic):
##### Core Concept
- This approach focuses exclusively on the `syntactic structure and format` of input data. Its guiding question is: "What is the structure of this data, and what are its limits?"
  - **For a `date of birth` field**: It doesn't ask, "Is this person over 18?" Instead, it asks, "What happens if the input is an empty string? What if it's `2025-02-30` (an invalid date)? What if it contains letters like `abc`? What if the string is 10,000 characters long?"
  - **For a `username field`**: It doesn't care if the username exists. It cares if the input field can handle special characters (`!@#$%^&*`), leading/trailing spaces, Unicode characters (`中文`), or an empty value.
##### Actionable Steps
1. Identify Input Field's Syntactic Properties
  - Analyze each field to identify its fundamental syntactic properties.
  - For example:
    - `Data Type`: String, Integer, Float, Boolean, Date, etc.
    - `Length`: Minimum, maximum, or exact length.
    - `Format`: Any specific format defined by a pattern or regular expression (e.g., email format, phone number format).
    - `Character Set`: The types of characters allowed (e.g., alphanumeric only, ASCII, Unicode).
2. Assign Characteristic IDs: Assign a unique ID to each identified characteristic (a combination of properties), prefixed with "I".
#### **Functionality-Based Approach** (Semantic):
##### Core Concept
- This approach focuses on the `semantic meaning and intended business logic` of the input data. Its guiding question is: "What does this data mean to the system, and how should the system behave in response?"
  - **For a `date of birth` field**: It doesn't ask about invalid formats like `2025-02-30`. Instead, it asks, "Does the date `2008-01-01` meet the 'over 18' business rule? What if the user is a VIP member, does that change the age requirement? What if the date makes the user over 100 years old, is that a special case?"
  - **For a `username` field**: It doesn't care about handling special characters. It cares about the state and properties of the account associated with the input string. It asks: "Does the username `johndoe` exist in the database? Is the account for `test_user_locked` currently suspended? Does the user admin have different permissions that will alter the system's response?"
##### Actionable Steps
1. Identify Input Field's Functional Properties
  - Analyze each field to identify its properties in the context of business rules, system states, and data relationships.
  - For example:
    - `Business Rules`: Any rules that govern the input, such as eligibility (`age > 18`), discounts (`user_status == 'VIP'`), or permissions.
    - `System State`: The current state of the data object in the backend (e.g., account `Active`, `Locked`, `Unverified`; item `In Stock`, `Out of Stock`).
    - `Data Relationships`: How the input relates to other data in the system (e.g., `username` and `password` must form a valid pair; `promo_code` must be applicable to items in the cart).
    - `User Roles:` The permission level of the user submitting the data (e.g., `Guest`, `Member`, `Administrator`).
2. Assign Characteristic IDs: Assign a unique ID to each identified characteristic (a combination of properties), prefixed with "F".
### **Examples**:
#### Example 1:
| Form XPath | Field XPaths (Field Name) | Characteristic ID | Characteristic Description |
| :--- | :--- | :--- | :--- |
| /HTML[1]/BODY[1]/DIV[2]/DIV[1]/SPAN[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[3]/DIV[2]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[1]/DIV[1]/DIV[1]/INPUT[1] | username | I1,I2,I3,I4,I5 | I1:String Length,I2:Contains Letters,I3:Contains Numbers,I4:Contains Special Characters,I5:Contains Unicode Characters |
| /HTML[1]/BODY[1]/DIV[2]/DIV[1]/SPAN[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[3]/DIV[2]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/INPUT[1] | password | I1,I2,I3,I4,I5,F6 | I1:String Length,I2:Contains Letters,I3:Contains Numbers,I4:Contains Special Characters,I5:Contains Unicode Characters,F6:Is Valid |
#### Example 2:
| Field XPaths | Field Name | Characteristic ID | Characteristic Description | Partitions (Blocks) |
| :--- | :--- | :--- | :--- | :--- |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/P[4]/INPUT[1] | issue_subject | I1,I2,I3,I4 | I1:String Length,I2:Contains Alphanumeric,I3:Contains Special Chars,I4:Contains Unicode |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[1]/SELECT[1] | issue_status_id | I1 | I1:Option Choice |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[8]/INPUT[1] | issue_due_date | I1,F2,F3 | I1:Date Format,F2:Temporal Relation (to now),F3:Leap Year |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[9]/INPUT[1] | issue_estimated_hours | I1,F2 | I1:Data Type,F2:Value Range |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[3]/DIV[2]/TEXTAREA[1] | issue_notes | I1,F2 | I1:String Length,F2:Content Format |

## Step 2: Derive Input Space Partitions
For each characteristic in Step 1:
- Define a **set of concrete, non-overlapping input partitions** that divide the input space meaningfully.
  Each partition must:
  1. Be a clearly defined subset (e.g., "1–5 characters").
  2. Be **mutually exclusive** and collectively cover the full range of realistic input variations.
  3. Avoid placeholder or generic values (e.g., "test", "123456") that do not reflect distinct behaviors.
  4. Fully cover all realistic input behaviors, with partitions that reflect **semantically and behaviorally distinct** input categories.
  5. Avoid surface-level differences that do not trigger different system behavior (e.g., `"abc@example.com"` vs. `"xyz@example.com"`).
### Examples:
#### Example 1:
| Form XPath | Field XPaths (Field Name) | Characteristic ID | Characteristic Description | Partitions (Blocks) |
| :--- | :--- | :--- | :--- | :--- |
| /HTML[1]/BODY[1]/DIV[2]/DIV[1]/SPAN[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[3]/DIV[2]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[1]/DIV[1]/DIV[1]/INPUT[1] | username | I1,I2,I3,I4,I5 | I1:String Length,I2:Contains Letters,I3:Contains Numbers,I4:Contains Special Characters,I5:Contains Unicode Characters | I1:{empty string (0),too short (1-3),normal(4-50),exceed the limit(51-)},I2:{true/false},I3:{true/false},I4:{true/false},I5:{true/false} |
| /HTML[1]/BODY[1]/DIV[2]/DIV[1]/SPAN[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[3]/DIV[2]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/INPUT[1] | password | I1,I2,I3,I4,I5,F6 | I1:String Length,I2:Contains Letters,I3:Contains Numbers,I4:Contains Special Characters,I5:Contains Unicode Characters,F6:Is Valid | I1:{empty string (0),too short (1-7),normal(8-74),too long(75-)},I2:{true/false},I3:{true/false},I4:{true/false},I5:{true/false},F6:{true/false} |
#### Example 2:
| Field XPaths | Field Name | Characteristic ID | Characteristic Description | Partitions (Blocks) |
| :--- | :--- | :--- | :--- | :--- |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/P[4]/INPUT[1] | issue_subject | I1,I2,I3,I4 | I1:String Length,I2:Contains Alphanumeric,I3:Contains Special Chars,I4:Contains Unicode | I1:{empty,normal (1-255),exceeds limit (256+)},I2:{true/false},I3:{true/false},I4:{true/false} |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[1]/SELECT[1] | issue_status_id | I1 | I1:Option Choice | I1:{New,In Progress,Resolved,Closed} |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[8]/INPUT[1] | issue_due_date | I1,F2,F3 | I1:Date Format,F2:Temporal Relation (to now),F3:Leap Year | I1:{default,valid (YYYY-MM-DD),invalid format(e.g.,07-2025-31),invalid value(e.g.,2025-02-30)},F2:{past,today,future)},F3:{is leap(e.g.,2028-02-29),not leap} |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[9]/INPUT[1] | issue_estimated_hours | I1,F2 | I1:Data Type,F2:Value Range | I1:{empty,integer,float,non-numeric},F2:{zero,positive,negative} |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[3]/DIV[2]/TEXTAREA[1] | issue_notes | I1,F2 | I1:String Length,F2:Content Format | I1:{empty,normal,long},F2:{plaintext,Markdown} |

## Step 3: Generate Form-Level Test Cases (Each-Choice Criteria)
Based on the field partition in Step 2:
- Generate **a minimal set of complete logically coherent form-level test cases** that satisfies the **Each-Choice Criteria**:
### Generation Principles:
- You must generate:
  - **Minimal (Each-Choice)**: The total number of test cases should be determined by the field with the most partitions. Your goal is to combine partitions cleverly so that every partition of every field is tested in the fewest possible number of form submissions.
  - **Systematic Variation**: Create subsequent test cases by systematically covering the remaining untested partitions (e.g., empty values, invalid formats, edge cases), ideally changing one or two aspects from the base case to isolate bugs.
  - **Consistency**: All values within a single test case must be **semantically consistent, valid, and non-redundant**. Avoid logically contradictory combinations (e.g., Age: 15 and Occupation: Retiree).
    - If a 'First Name' field is 'John', and a 'Last Name' field is 'Doe', don't combine 'John' with an obviously unrelated 'Age' like '-5').
  - **Presumption of Feasibility**: If a combination's validity depends on implementation-specific business logic (i.e., it is not logically or semantically self-contradictory), assume it is feasible. Do not attempt to infer complex back-end validation rules.
#### Actionable Steps
##### Substep 1: Generate Field-Level Test Case (Each-Choice Criteria)
###### Examples:
####### Example 1:
| Field XPaths | Field Name | Characteristic ID | Characteristic Description | Partitions (Blocks) | Test Requirements (Each-Choice Criteria) | Infeasible TRs | Revised TRs | Test Cases | Memo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| /HTML[1]/BODY[1]/DIV[2]/DIV[1]/SPAN[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[3]/DIV[2]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[1]/DIV[1]/DIV[1]/INPUT[1] | username | I1,I2,I3,I4,I5 | I1:String Length,I2:Contains Letters,I3:Contains Numbers,I4:Contains Special Characters,I5:Contains Unicode Characters | I1:{empty string (0),too short (1-3),normal(4-50),exceed the limit(51-)},I2:{true/false},I3:{true/false},I4:{true/false},I5:{true/false} | TR1:{0,false,false,false,false},TR2:{1,false,true,false,true},TR3:{50,true,false,true,false},TR4:{51,true,true,true,true} | TR1:If there is an 1-length string, it's infeasible to contain both of number and Unicode Character,TR4:if the length exceeded the limit, it can't be a valid username. | TR1':{3,false,true,false,true,false},TR4':{51,true,true,true,true,false} | TC1:{0,false,false,false,false,false},TC2:{3,false,true,false,true,false},TC3:{50,true,false,true,false,true},TC4:{51,true,true,true,true,false} | TC1 covers TR1';TC2 covers TR2;TC3 covers TR3;TC4 covers TR4'; |
| /HTML[1]/BODY[1]/DIV[2]/DIV[1]/SPAN[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[3]/DIV[2]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/INPUT[1] | password | I1,I2,I3,I4,I5,F6 | I1:String Length,I2:Contains Letters,I3:Contains Numbers,I4:Contains Special Characters,I5:Contains Unicode Characters,F6:Is Valid | I1:{empty string (0),too short (1-7),normal(8-74),too long(75-)},I2:{true/false},I3:{true/false},I4:{true/false},I5:{true/false},F6:{true/false} | {0,false,false,false,false,false},{7,false,true,false,true,false},{74,false,true,false,true,true},{75,true,true,false,false,false} | none | N/A | TC1:{0,false,false,false,false,false},TC2:{7,false,true,false,true,false},TC3:{74,false,true,false,true,true},TC4:{75,true,true,false,false,false} | TC1 covers TR1;TC2 covers TR2;TC3 covers TR3;TC4 covers TR4; |
####### Example 2:
| Field XPaths | Field Name | Characteristic ID | Characteristic Description | Partitions (Blocks) | Test Requirements (Each-Choice Criteria) | Infeasible TRs | Revised TRs | Test Cases | Memo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/P[4]/INPUT[1] | issue_subject | I1,I2,I3,I4 | I1:String Length,I2:Contains Alphanumeric,I3:Contains Special Chars,I4:Contains Unicode | I1:{empty,normal (1-255),exceeds limit (256+)},I2:{true/false},I3:{true/false},I4:{true/false} | TR1:{normal,true,false,true},TR2:{empty,false,false,false},TR3{exceedslimit,true,true,false} | None | N/A | TC1:{normal,true,false,true},TC2:{empty,false,false,false},TC3:{exceedslimit,true,true,false} | TC1 covers TR1;TC2 covers TR2;TC3 covers TR3 |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[1]/SELECT[1] | issue_status_id | I1 | I1:Option Choice | I1:{New,In Progress,Resolved,Closed} | TR1:{New},TR2:{In Progress},TR3:{Resolved},TR4:{Closed} | None | N/A | TC1:{New},TC2:{In Progress},TC3:{Resolved},TC4:{Closed} | TC1 covers TR1;TC2 covers TR2;TC3 covers TR3;TC4 covers TR4 |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[8]/INPUT[1] | issue_due_date | I1,F2,F3 | I1:Date Format,F2:Temporal Relation (to now),F3:Leap Year | I1:{default,valid (YYYY-MM-DD),invalid format(e.g.,year-month-31),invalid value(e.g.,9999-99-99)},F2:{past,today,future)},F3:{is leap(e.g.,2028-02-29),not leap} | TR1:{valid,past,not leap},TR2:{default,today,N/A},TR3:{invalid format,N/A,N/A},TR4:{invalid value,future,not leap} | None | N/A | TC1:{valid,past,not leap},TC2:{default,today,N/A},TC3:{invalid format,N/A,N/A},TC4:{invalid value,future,not leap} | TC1 covers TR1;TC2 covers TR2;TC3 covers TR3;TC4 covers TR4 |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/P[9]/INPUT[1] | issue_estimated_hours | I1,F2 | I1:Data Type,F2:Value Range | I1:{empty,integer,float,non-numeric},F2:{zero,positive,negative} | TR1:{integer,positive},TR2:{empty,N/A},TR3:{non-numeric,N/A},TR4:{float,negative} | TR3  | None (TR3 cannot be revised because such inputs cannot be generated. Therefore, TR3 are removed from TRs) | TC1:{integer,positive},TC2:{empty,N/A},TC3:{float,negative} | TC1 covers TR1;TC2 covers TR2;TC3 covers TR4 |
| /HTML[1]/BODY[1]/FORM[1]/DIV[1]/FIELDSET[3]/DIV[2]/TEXTAREA[1] | issue_notes | I1,F2 | I1:String Length,F2:Content Format | I1:{empty,normal,long},F2:{plaintext,Markdown} | TR1:{normal,plaintext},TR2:{empty,N/A},TR3:{long,Markdown} | None | N/A | TC1:{normal,plaintext},TC2:{empty,N/A},TC3:{long,Markdown} | TC1 covers TR1;TC2 covers TR2;TC3 covers TR3 |
##### Substep 2: Generate Form-Level Test Case (Each-Choice Criteria)
This substep combines the field-level test cases generated in Substep 1 into a minimal set of comprehensive, form-level test cases. The primary method is to create a **Test Case Combination Matrix**.
- The number of form-level test cases is determined by the field that requires the most individual test cases. Take the `Example 2` test cases from Substep 1 as an example: the `issue_status_id` and `issue_due_date` fields each require **4 field-level test cases**. Therefore, a minimum of **4 form-level test cases** are needed to cover all field-level test requirements with the Each-Choice Criteria.
###### Generation Principles:
- The matrix maps each form-level test case to a specific test case from each field. The construction follows these principles:
- **Base Case First:** The first form-level test case (Form TC1) establishes a "happy path" by combining the baseline test case (TC1) from every single field.
- **Systematic Combination**: Subsequent form-level test cases are created by strategically combining the remaining field-level test cases, ensuring that every field-level test case is used at least once in the final set.
###### Examples:
####### Example 1: Test Case Combination Matrix
| Form-Level Test Case | `username` Test Case | `password` Test Case | Purpose |
| :--- | :--- | :--- | :--- |
| Form TC1 | TC3 | TC3 | Valid/Normal inputs (Happy Path) |
| Form TC2 | TC2 | TC2 | Too short inputs |
| Form TC3 | TC1 | TC1 | Empty inputs |
| Form TC4 | TC4 | TC4 | Too long / Exceeds limit inputs |

####### Example 2: Test Case Combination Matrix
| Form-Level Test Case | `issue_subject` Test Case | `issue_status_id` Test Case | `issue_due_date` Test Case | `issue_estimated_hours` Test Case | `issue_notes` Test Case | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Form TC1 | TC1 | TC1 | TC1 | TC1 | TC1 | Valid/Normal inputs (Happy Path) |
| Form TC2 | TC2 | TC2 | TC2| TC2 | TC2 | Empty/Default value handling |
| Form TC3 | TC3 | TC3 | TC3 | TC3 | TC3 | Invalid formats |
| Form TC4 | TC1 | TC4 | TC4 | TC1 | TC1 | Final state and invalid value handling |
##### Substep 3: Generate Concrete Input Values
This substep translates the abstract test case combinations from the `Test Case Combination Matrix` into concrete, realistic input values for each form submission. Each set of values corresponds to one `Form-Level Test Case` and is designed to be logically coherent.
###### Examples
####### Example 1
| Form-Level Test Case | Field Name | Input Value | Rationale |
| :--- | :--- | :--- | :--- |
| Form TC1 | username | alejandra.calderon_profile | Corresponds to TC3: A valid username of normal length (23 chars) containing letters, numbers, and special characters, representing a standard successful login attempt. |
|  | password | 199819981998 | Corresponds to TC3: A valid password of normal length (12 chars) that meets the unusual system requirement of containing only numbers and Unicode characters (specifically, a birth year in Arabic, Thai, and Devanagari numerals). |
| Form TC2 | username | 7世 | Corresponds to TC2: An invalid, too-short username (2 chars) that combines a number and a Unicode character to test the lower length boundary and mixed character type validation. |
|  | password | €1 | Corresponds to TC2: An invalid, too-short password (2 chars) combining a Unicode currency symbol and a number, testing handling of short, non-standard inputs. |
| Form TC3 | username |  | Corresponds to TC1: An empty string to test how the system handles a missing required username. |
|  | password |  | Corresponds to TC1: An empty string to test how the system handles a missing required password. |
| Form TC4 | username | this-username-is-intentionally-made-extremely-long-to-test-the-upper-boundary-limit-of-the-input-field-Ω-123 | Corresponds to TC4: An invalid, overly long username (129 chars) that includes letters, numbers, special characters, and Unicode to test the system's upper length limit validation. |
|  | password | ThisPasswordIsIntentionallyMadeVeryLongToExceedTheSeventyFourCharacterLimitAndItOnlyContainsLettersAndNumbers1234567890 | Corresponds to TC4: An invalid, overly long password (116 chars) containing only letters and numbers to test the password field's specific upper length boundary. |
####### Example 2
| Form-Level Test Case | Field Name | Input Value | Rationale |
| :--- | :--- | :--- | :--- |
| Form TC1 | issue_subject | 修復使用者個人資料頁面的顯示錯誤 | Corresponds to TC1: Normal length, contains Unicode. |
|  | issue_status_id | New | Corresponds to TC1: Option 'New'. |
|  | issue_due_date | 2025-06-20 | Corresponds to TC1: Valid format, in the past (relative to July 2025), not a leap year. |
|  | issue_estimated_hours | 8 | Corresponds to TC1: Positive integer. |
|  | issue_notes | 當使用者上傳大於 2MB 的頭像時，個人資料頁面的佈局會中斷。需要後端和前端協同修復。 | Corresponds to TC1: Normal length, plaintext content. |
| Form TC2 | issue_subject |  | Corresponds to TC2: Empty string. |
|  | issue_status_id | In Progress | Corresponds to TC2: Option 'In Progress'. |
|  | issue_due_date |  | Corresponds to TC2: Empty value, expecting system default (e.g., today's date). |
|  | issue_estimated_hours |  | Corresponds to TC2: Empty value. |
|  | issue_notes |  | Corresponds to TC2: Empty string. |
| Form TC3 | issue_subject | CRITICAL BUG: System database deadlock occurs when processing orders with special characters (e.g., &, %, <) in the promo code field, causing the entire checkout API (api/v3/checkout) to become unresponsive. This affects ALL transactions and requires immediate attention!!" + "xxxxx..." (repeat to exceed 256 chars) | Corresponds to TC3: Exceeds length limit, contains special characters. |
|  | issue_status_id | Resolved | Corresponds to TC3: Option 'Resolved'. |
|  | issue_due_date | 2025/09/15 | Corresponds to TC3: Invalid format (uses '/' instead of '-'). |
|  | issue_estimated_hours | -4.5 | Corresponds to TC3: Negative float value (e.g., a time credit). |
|  | issue_notes | # 問題根本原因分析\n\n**重現步驟**:\n\n1. 登入一個帳號\n2. 前往購物車\n3. 輸入一個帶有&符號的優惠碼\n\n*系統崩潰*\n\n---\n\n此處省略大量Markdown格式的日誌和堆疊追蹤訊息以達到超長內容的要求。 | Corresponds to TC3: Long content with Markdown formatting. |
| Form TC4 | issue_subject | 優化資料庫查詢效能 | Corresponds to TC1: A valid, normal input to isolate other fields' tests. |
|  | issue_status_id | Closed | Corresponds to TC4: Option 'Closed'. |
|  | issue_due_date | 2026-02-29 | Corresponds to TC4: "Invalid value (February 29th does not exist in a non-leap year)." |
|  | issue_estimated_hours | 20 | Corresponds to TC1: A valid, normal input. |
|  | issue_notes | 已完成對應資料表的索引優化並部署上線。監控一週後確認查詢延遲已從平均 500ms 降至 80ms。 | Corresponds to TC1: A valid, normal closing note. |

### Final Output Format
- For each input field in a test case, you must include only the following elements:
  - The XPath selected from the provided `{provided_xpaths}` list** (`xpath`)
  - The input value to be entered (`input_value`)
  - The interaction type as an action number (`action_number`)
- Every generated test case must include a final **form submission action**, either by **clicking a submit-capable element** (e.g., `<button type="submit">`, `<input type="submit">`) or by triggering form submission through other valid user interactions:
  - The element's **ABSOLUTE** XPath (`xpath`)
    - It must be a valid interactive element (e.g., `<button type="submit">`, `<input type="submit">`) that exists in the `{Form DOM Hierarchy}`.
  - Empty string input value (`input_value`)
  - The `action_number` specifying the interaction type. You must choose a valid number for this value from the Action Number Mapping. (`action_number`)
#### XPath Guidelines
- Only use the XPath selected from the provided `{provided_xpaths}` list**
- Do not invent or synthesize new XPath paths.
- To ensure correctness and prevent XPath-related errors, you must validate each XPath expression against the following rules:
  1. Each XPath expression must be syntactically valid and match the following regular expression: `^(\/[A-Za-z][A-Za-z0-9_.-]*\[\d+\])+$`
    This ensures:
    - Each node must start with a slash `/`.
    - Each tag name must be legal:
      - Each tag name must start with a letter (`A–Z` or `a–z`)
      - Each tag name may contain letters (`A–Z` or `a–z`), digits (`0 - 9`), hyphens (`-`), underscores (`_`), and periods (`.`)
      - Each tag must be followed by exactly one numeric index enclosed in balanced square brackets (e.g., `DIV[1]`)
  2. Use well-formed bracket notation:
    - [Allowed] Valid example:
      - `/HTML[1]/BODY[1]/DIV[2]/FORM[1]/INPUT[3]`
    - [Disallowed] Invalid Examples:
      - `/HTML[1]/BODY[1]/DIV[3[1]` (unbalanced/malformed brackets)
      - `/HTML[1]/BODY[1]/DIV[[1]]`, `/HTML[1]/BODY[1]/DIV[]`, `/HTML[1]/BODY[1]/DIV[abc]` (nested, empty, or non-numeric indices)
      - `/HTML[1]/BODY[1DIV[1]` (missing '/' between nodes, or concatenated element names)
      - Any expression containing illegal characters or unsupported punctuation
  3. The XPath must start with `{form_xpath}`, the absolute XPath of the `<form>` element
  4. [Important] Never fabricate, infer, or hallucinate XPath expressions:
    - If an element does **not** exist in `{dom}`, omit it.
    - Never guess sibling positions or fabricate index values.
  5. [Important] If any XPath goes wrong, find out the referenced XPath from the provided `{provided_xpaths}` list and fix it.

# Required Inputs
## Action Number Mapping:
{
  -1: changeFocus,
  0: click,
  1: inputString
}""") + \
"""### Form XPath:
{form_xpath}
### Form DOM Hierarchy:
{dom}
### Provided Field XPaths:
{field_xpaths}"""
        elif selector == "update_input_values":
            # TODO: 根據特性來產生新的輸入值
            return "你是軟體測試專家，負責測試網頁應用程式。目標是產生網頁表單的測試案例。\n" + \
                   "針對因AJAX而被更新的表單，更新舊的測試案例，確保包含此xpath的測試資料: {lacked_field_xpath}\n" + \
                   "這是action_number的對照表: -1: changeFocus, 0: click, 1: inputString\n" + \
                   "這是表單的XPATH路徑: {form_xpath}\n" + \
                   "這是現有的測試案例: {input_values}\n" + \
                   "這是表單的DOM: {dom}" + \
                   "產生的測試案例中，包含且只包含各欄位的input_value、各欄位的action_number、及各欄位的xpath(絕對路徑)，要能有效填入表單。\n" + \
                   "讓我們一步步思考"
        raise ValueError(f"Invalid selector: {selector}")
