def generate_alert(message, logger=None):
    """Generate an alert (print + optional log)."""
    print(f"[ALERT] {message}")
    if logger:
        logger.warning(message)

