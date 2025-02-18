from django.db.migrations import RunPython


class CreateSetting(RunPython):
    def __init__(
        self,
        *,
        setting: str,
        python_type: str = "string",
        dry_value: str | int | None = None,
        is_public: bool = False,
    ):
        operation = create_setting(setting, python_type, dry_value, is_public)
        reverse_operation = delete_setting(setting)
        super().__init__(operation, reverse_operation, atomic=False)


class DeleteSetting(RunPython):
    def __init__(self, *, setting: str):
        operation = delete_setting(setting)
        super().__init__(operation, atomic=False)


def create_setting(
    setting: str, python_type: str, dry_value: str | int | None, is_public: bool
):
    def migration_operation(apps, _):
        Setting = apps.get_model("misago_conf", "Setting")
        Setting.objects.create(
            setting=setting,
            python_type=python_type,
            dry_value=dry_value,
            is_public=is_public,
        )

    return migration_operation


def delete_setting(setting: str):
    def migration_operation(apps, _):
        Setting = apps.get_model("misago_conf", "Setting")
        Setting.objects.filter(setting=setting).delete()

    return migration_operation
