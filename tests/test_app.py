
def test_verifica_a_pagina_detalhe_curso(client):
    with client.test_client() as test_client:

        response = test_client.get('curso/detalhe/<curso_id>')
        assert response.status_code == 200
