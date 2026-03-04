def filter_by_expiry(expiry):
    data_store.selected_expiry = expiry
    # Rebuild UI with only this expiry's options