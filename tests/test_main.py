from unittest.mock import patch

from src.main import main


def test_main_function() -> None:
    with patch("uvicorn.run") as mock_uvicorn_run, patch("src.main.get_settings") as mock_get_settings:
        mock_settings = mock_get_settings.return_value
        mock_settings.uvicorn.host = "127.0.0.1"
        mock_settings.uvicorn.port = 8000
        mock_settings.uvicorn.reload = True
        mock_settings.uvicorn.workers = 4

        main()

        mock_uvicorn_run.assert_called_once_with(
            "src.core.application:application",
            host=mock_settings.uvicorn.host,
            port=mock_settings.uvicorn.port,
            reload=mock_settings.uvicorn.reload,
            workers=mock_settings.uvicorn.workers,
        )
