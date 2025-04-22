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
            return "這是action_number對欄位名稱的對照表\n" + \
                   "-1: changeFocus, 0: click, 1: input\n" + \
                   "針對以下表單的每個欄位內容、各自列舉出可能的回答的特性，數量愈少愈好且不要重複。\n" + \
                   "這是表單的XPATH路徑: {form_xpath}\n" + \
                   "根據特性來切分input space partition。\n" + \
                   "以整張表單為單位，一次性的根據所有欄位的input space partition，產生符合each choice criteria、最少數量的測試組合。\n" + \
                   "產生的每個測試組合中，有各欄位的input_value、及各欄位的action_number，key是各欄位的xpath絕對路徑，要能有效填入表單。最外層使用Array列舉所有測試組合。\n" + \
                   """結果用json格式呈現，並用```json
```框起來。\n""" + \
                   "讓我們一步步思考:\n" +  \
                   "{dom}"
        elif selector == "update_input_values":
            # TODO: 根據特性來產生新的輸入值
            return "這是action_number對欄位名稱的對照表\n" + \
                   "-1: changeFocus, 0: click, 1: input\n" + \
                   "針對以下因AJAX而被更新的表單中的每個欄位內容，更新舊的測試組合，確保覆蓋所有新的表單欄位，尤其是{lacked_field_xpath}\n" + \
                   "這是表單的XPATH路徑: {form_xpath}\n" + \
                   "這是現有的測試組合: {input_values}\n" + \
                   "產生的測試組合中，有各欄位的input_value、各欄位的action_number、及各欄位的xpath(絕對路徑)，要能有效填入表單。最外層使用Array列舉此測試組合。\n" + \
                   """結果用json格式呈現，並用```json
```框起來。\n""" + \
                   "讓我們一步步思考:\n" +  \
                   "{dom}"
        raise ValueError(f"Invalid selector: {selector}")
