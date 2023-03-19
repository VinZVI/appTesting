

class DBSaveException(Exception):
    pass


class DataBaseSaveError(Exception):
    """Ошибка при сохранении в базу данных"""

    def __init__(self, additional_message, *args, **kwargs):
        self.additional_message = additional_message
        message = f"Ошибка при сохранении в базу данных, обратитесь к разработчику. " \
                  f"Ошибка: {self.additional_message}"
        self.message = message
        super().__init__(self.message)