def normalize_phone(phone):
    if not phone:
        return None
    return phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')