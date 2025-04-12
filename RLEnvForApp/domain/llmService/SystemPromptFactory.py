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
                   "-1: button, 0: first name, 1: last name, 2: email, 3: username, 4: phone, 5: company name, 6: gender, 7: card number, 8: expiration date, 9: CVV, 10: address, 11: postal code, 12: store name, 13: year, 14: day, 15: search, 16: full name, 17: street address, 18: city, 19: state, 20: province, 21: region, 22: country, 23: claim code, 24: UPC, 25: brand, 26: product name, 27: type, 28: connectivity, 29: color, 30: wireless technology, 31: feature, 32: form factor, 33: microphone type, 34: MPN, 35: number, 36: user type, 37: description, 38: display name, 39: community name, 40: suburb, 41: date, 42: landline, 43: password\n" + \
                   "針對以下表單的每個欄位內容、各自列舉出可能的回答的特性，數量愈少愈好且不要重複。\n" + \
                   "根據特性來切分input space partition。\n" + \
                   "以整張表單為單位，一次性的根據所有欄位的input space partition，產生符合each choice criteria、最少數量的測試組合。\n" + \
                   "產生的每個測試組合中，有各欄位的input_value、及各欄位的action_number，key是各欄位的xpath絕對路徑，要能有效填入表單。最外層使用Array列舉所有測試組合。\n" + \
                   """結果用json格式呈現，並用```json
```框起來。\n""" + \
                   "讓我們一步步思考:\n" +  \
                   "{dom}"
        elif selector == "update_input_values":
            # TODO: update 特定form的其中一組輸入值
            return ""
        raise ValueError(f"Invalid selector: {selector}")
