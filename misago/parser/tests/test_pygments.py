from ..pygments import get_pygments_options


def test_get_pygments_options_returns_languages_from_list():
    languages, choices, names = get_pygments_options(["php", "python"])

    assert "php" in languages
    assert "python" in languages
    assert "actionscript" not in languages
    assert "html" not in languages

    assert choices == (("php", "PHP"), ("python", "Python"))
    assert names["php"] == "PHP"
    assert names["python"] == "Python"


def test_get_pygments_options_returns_all_languages_from_list():
    languages, choices, names = get_pygments_options(True)
    assert len(languages) > 50
    assert len(choices) > 50
    assert len(names) > 50
