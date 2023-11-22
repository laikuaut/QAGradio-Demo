import app


class TestMain:
    def test__copy_1(self):
        """テストケース１"""
        text = "aaa"
        actual = app.copy(text)
        assert text == actual

    def test__trim_1(self):
        """テストケース２"""
        text = 'a"aa'
        expected = "aaa"
        actual = app.trim(text)
        assert expected == actual
