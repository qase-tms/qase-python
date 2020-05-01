def test_imports():
    import qaseio
    from qaseio import client

    assert getattr(qaseio, "__version__")
    assert qaseio.QaseApi == client.Client
