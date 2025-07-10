import re


def format_phone(phone):
    phone = re.sub(r"[^0-9]", "", phone)

    if len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"

    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"

    return phone
