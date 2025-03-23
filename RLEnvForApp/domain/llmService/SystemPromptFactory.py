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
            return "針對以下表單的每個欄位內容、各自列舉出可能的回答的特性，數量愈少愈好且不要重複。\n" + \
                   "根據特性來切分input space partition。\n" + \
                   "以整張表單為單位，一次性的根據所有欄位的input space partition，產生符合each choice criteria、最少數量的測試組合。\n" + \
                   "產生的測試組合中的輸入值，要能有效填入表單。\n" + \
                   """結果用csv格式呈現，並用```csv
```框起來，標題為各欄位的xpath絕對路徑。\n""" + \
                   "讓我們一步步思考: " +  \
                   "{dom}"
        elif selector == "update_input_values":
            # TODO: update 特定form的其中一組輸入值
            return ""
        raise ValueError(f"Invalid selector: {selector}")
