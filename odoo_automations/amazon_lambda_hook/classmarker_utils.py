def parse_classmarker_result(json_dict):
    if not "result" in json_dict:
        return None, None, None,"json does not contain result tag"

    if not "questions" in json_dict:
        return None, None, None, "json does not contain question data"

    name = json_dict["result"]["first"]
    surname = json_dict["result"]["last"]
    email = json_dict["result"]["email"]
    id = int(json_dict["result"]["cm_user_id"])
    result = int(json_dict["result"]["points_scored"])

    print(name)

    incorrect_answers = 0
    for question in json_dict["questions"]:
        if question["result"] == "incorrect":
            incorrect_answers = incorrect_answers + 1

    return id, result, incorrect_answers, ""