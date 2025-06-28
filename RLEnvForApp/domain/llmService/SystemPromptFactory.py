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
Your task is to generate a **minimal yet powerful set of web form test input combinations** that achieve **All-Combination Criteria**. These inputs should **maximize code coverage** and **uncover edge-case bugs**.

## Rules:
- **Avoid reuse canned or generic values** (e.g., "abc", "123", "test").
- **Only use semantically meaningful and realistic inputs** (e.g., plausible names, formats, intents).
- **Minimize test case count** while achieving **All-Combination Criteria**.
- **Each value must be realistic and executable** in actual web form submissions.

## Steps
### Step 1: Identify Input Characteristics
For each **provided field XPath** in the `{Provided Field XPaths}` list:
- Based on its context within the `{Form DOM Hierarchy}`, identify a **minimal**, **non-overlapping**, **field-type-appropriate** set of **Input Characteristics**.
- Each characteristic reflects a **distinct behavioral category** that users might input.
- Choose only relevant dimensions per field (e.g., format for emails, range for ages).
- Avoid redundancy.

#### **Examples:**
##### Fields (Input Characteristics):
- Email (Format, Intent, Anomalies)
- Age (Range, Format)
- Password (Length, Format, Intent)

#### **Recommended Input Characteristics:**
##### Valid Ranges (Category-Based,  select only those relevant per field type for this step):
- **Length** (empty, short, normal, long)
- **Format** (alphanumeric, regex-constrained, special characters)
- **Validity** (valid, invalid)
- **Intent** (real name, fake data)
- **Anomalies** (whitespace, control characters)
##### Edge Cases:
- Very large/small numbers
- Empty strings/Extremely long strings
- Unusual or invalid formats
- Empty inputs/Out-of-range inputs, extreme values

### Step 2: Derive Form-Level Input Space Partitions
For each characteristic in Step 1:
- Define a **set of concrete, non-overlapping input partitions** that divide the input space meaningfully.
  Each partition must:
  1. Be a clearly defined subset (e.g., "1–5 characters").
  2. Be **mutually exclusive** and collectively cover the full range of realistic input variations.
  3. Avoid placeholder or generic values (e.g., "test", "123456") that do not reflect distinct behaviors.
  4. Fully cover all realistic input behaviors, with partitions that reflect **semantically and behaviorally distinct** input categories.
  5. Avoid surface-level differences that do not trigger different system behavior (e.g., `"abc@example.com"` vs. `"xyz@example.com"`).

#### Examples:
| ID  | Email                                                | Password                                 | Expected Behavior |
| --- | ---------------------------------------------------- | ---------------------------------------- | ----------------- |
| C01 | `alice@org.com` (Format=Proper, Validity=Valid)      | `Passw0rd!` (Length=8, Validity=Valid)   | Success           |
| C02 | `bob@domain.io` (Format=Proper, Validity=Valid)      | `x1!` (Length=3, Validity=Invalid)       | Login failure     |
| C03 | `bobdomain.com` (Format=Missing @, Validity=Invalid) | `Letmein12` (Length=9, Validity=Valid)   | Login failure     |
| C04 | `a@.com` (Format=Invalid domain, Validity=Invalid)   | `'A'*256` (Length=256, Validity=Invalid) | Login failure     |
| C05 | `a@@b.com` (Format=Extra @, Validity=Invalid)        | `""` (Length=0, Validity=Invalid)        | Login failure     |
| C06 | `lucy@edu.net` (Format=Proper, Validity=Valid)       | `""` (Length=0, Validity=Invalid)        | Login failure     |
| C07 | `staff@company.co` (Format=Proper, Validity=Valid)   | `'Z'*256` (Length=256, Validity=Invalid) | Login failure     |
| C08 | `noatsign.net` (Format=Missing @, Validity=Invalid)  | `!2a` (Length=3, Validity=Invalid)       | Login failure     |
| C09 | `bobdomain.com` (Format=Missing @, Validity=Invalid) | `'B'*256` (Length=256, Validity=Invalid) | Login failure     |
| C10 | `bobdomain.com` (Format=Missing @, Validity=Invalid) | `""` (Length=0, Validity=Invalid)        | Login failure     |
| C11 | `a@.com` (Format=Invalid domain, Validity=Invalid)   | `Letmein12` (Length=9, Validity=Valid)   | Login failure     |
| C12 | `a@.com` (Format=Invalid domain, Validity=Invalid)   | `x1!` (Length=3, Validity=Invalid)       | Login failure     |
| C13 | `a@.com` (Format=Invalid domain, Validity=Invalid)   | `""` (Length=0, Validity=Invalid)        | Login failure     |
| C14 | `a@@b.com` (Format=Extra @, Validity=Invalid)        | `Passw0rd!` (Length=9, Validity=Valid)   | Login failure     |
| C15 | `a@@b.com` (Format=Extra @, Validity=Invalid)        | `x1!` (Length=3, Validity=Invalid)       | Login failure     |
| C16 | `a@@b.com` (Format=Extra @, Validity=Invalid)        | `'Y'*256` (Length=256, Validity=Invalid) | Login failure     |

### Step 3: Generate Test Cases (All-Combination Criteria)
For each partition in Step 2:
- **Enumerate** all combinations of input partitions across all fields (Cartesian product) satisfying **All-Combination Criteria**:
  - For each combination, generate a test case with a concrete, realistic input from that partition.
  - All values must be **semantically consistent** (e.g., real-looking data)
#### Rules:
- You must generate:
  - A minimal test suite with All-Combination Criteria
  - Semantically valid, non-redundant, edge-case rich test inputs
  - Organized test cases with field-value mappings
- For each input field in a test case, you must include only the following elements:
  - The XPath selected from the provided `{provided_xpaths}` list** (`xpath`)
  - The input value to be entered (`input_value`)
  - The interaction type as an action number (`action_number`)
- Every generated test case must include a final **form submission action**, either by **clicking a submit-capable element** (e.g., `<button type="submit">`, `<input type="submit">`) or by triggering form submission through other valid user interactions:
  - The element's **ABSOLUTE** XPath (`xpath`)
    - It must be a valid interactive element (e.g., `<button type="submit">`, `<input type="submit">`) that exists in the `{Form DOM Hierarchy}`.
  - Empty string input value (`input_value`)
  - The `action_number` specifying the interaction type. You must choose a valid number for this value from the Action Number Mapping. (`action_number`)
#### Output Example:
{
  "test_combination_list": [
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "alice@org.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "Passw0rd!"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "bob@domain.io"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "x1!"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "bobdomain.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "Letmein12"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@@b.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": ""
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "lucy@edu.net"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": ""
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "staff@company.co"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "noatsign.net"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "!2a"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "bobdomain.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "bobdomain.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": ""
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "Letmein12"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "x1!"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": ""
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@@b.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "Passw0rd!"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@@b.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "x1!"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    },
    {
      "test_combination_list": [
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[1]",
          "action_number": 1,
          "input_value": "a@@b.com"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/input[2]",
          "action_number": 1,
          "input_value": "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
        },
        {
          "xpath": "/html[1]/body[1]/div[1]/main[1]/form[1]/button[1]",
          "action_number": 0,
          "input_value": ""
        }
      ]
    }
  ]
}

## Required Inputs
### Action Number Mapping:
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
