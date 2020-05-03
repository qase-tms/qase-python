def test_init(qs_plugin):
    plugin = qs_plugin()
    assert plugin
    assert plugin.client
    assert plugin.client.api_token


def test_plugin_init(qs_plugin, testdir):
    print(dir(testdir))
    testdir.plugins = [qs_plugin()]
    testdir.makepyfile(
        """
    def test_func():
        pass
    def test_other_func():
        pass
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)
