# TODO: prompt add action

class SystemPromptFactory:
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
            return "你是軟體測試專家，負責測試網頁應用程式。目標是產生網頁表單的測試組合，以最少的測試組合數量嘗試覆蓋所有code並找出潛在的bug。\n" + \
                   """Step 1: 針對以下表單的每個欄位內容、各自列舉出可能的回答的特性，數量愈少愈好且不要重複。
Step 2: 根據特性來切分input space partition。
Step 3: 以整張表單為單位，根據所有欄位的input space partition，產生符合each choice criteria、最少數量的測試組合。
產生的每個測試組合中，包含且只包含各欄位的xpath絕對路徑、input_value、及各欄位的action_number，要能有效填入表單。
\n"""+ \
                   "這是action_number的對照表: -1: changeFocus, 0: click, 1: inputString\n" + \
                   "這是表單的XPATH路徑: {form_xpath}\n" + \
                   "這是表單的DOM: {dom}"
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
