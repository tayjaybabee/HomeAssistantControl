class EntityDataPresentError(Exception):
    """
    Raised when an attempt is made to change the entity_data after it has been set.

    Usage example:
    >>> try:
    >>>     entity.entity_data = new_data  # Assuming entity is an instance of Entity class
    >>> except EntityDataPresentError as e:
    >>>     print(f'Error: {e}')
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EntityIDMismatchError(Exception):
    """
    Raised when there is a mismatch between the entity_id provided and the entity_id in the entity_data.

    Usage example:
    >>> try:
    >>>     entity.entity_id = 'new_entity_id'  # Assuming entity is an instance of Entity class
    >>> except EntityIDMismatchError as e:
    >>>     print(f'Error: {e}')
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
