def send_custom_notification(context, *, message):
    print(f"{message}")
    print(f'ti={context["ti"]}')
    print(f'current_state={context["ti"].current_state()}')
