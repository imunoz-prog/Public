# Puedes agregar fixtures aquí si necesitas setup/teardown global para los tests
import pytest

@pytest.fixture(autouse=True)
def reset_state():
    # Aquí podrías resetear el estado global si fuera necesario
    pass
