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
                   "-1: button, 0: first name, 1: last name, 2: email, 3: gender, 4: string, 5: user name, 6: full name, 7: postal code, 8: store name, 9: phone number, 10: street address, 11: city, 12: state, 13: province, 14: region, 15: number, 16: country, 17: display name, 18: address, 19: suburb, 20: company name, 21: card number, 22: expiration date, 23: CVV, 24: date, 25: password\n" + \
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
                   "-1: button, 0: first name, 1: last name, 2: email, 3: gender, 4: string, 5: user name, 6: full name, 7: postal code, 8: store name, 9: phone number, 10: street address, 11: city, 12: state, 13: province, 14: region, 15: number, 16: country, 17: display name, 18: address, 19: suburb, 20: company name, 21: card number, 22: expiration date, 23: CVV, 24: date, 25: password\n" + \
                   "針對以下因AJAX而被更新的表單中的每個欄位內容，更新現有的測試組合。\n" + \
                   "這是表單的XPATH路徑: {form_xpath}\n" + \
                   "這是現有的測試組合: {input_values}\n" + \
                   "產生的測試組合中，有各欄位的input_value、及各欄位的action_number，key是各欄位的xpath絕對路徑，要能有效填入表單。最外層使用Array列舉此測試組合。\n" + \
                   """結果用json格式呈現，並用```json
```框起來。\n""" + \
                   "讓我們一步步思考:\n" +  \
                   "{dom}"
        raise ValueError(f"Invalid selector: {selector}")
