from pathlib import Path
from loguru import logger
from .base import ParaTranzAPI
from pooch import retrieve, HTTPDownloader, Unzip


class Artifacts(ParaTranzAPI):
    """
    ParaTranz Artifacts API 類別
    ParaTranz Artifacts API class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_artifacts_info(self, project_id: str) -> dict:
        """獲取 Artifacts 建構資訊 | Get Artifacts build information

        Args:
            project_id (str):
                專案 ID | Project ID

        Returns:
            dict:
                Artifacts 建構資訊 | Artifacts build information
        """
        artifacts_url = f"{self._projects_url}/{project_id}/artifacts"
        return self._request("GET", artifacts_url)

    def trigger_artifacts_build(self, project_id: str) -> dict:
        """觸發 Artifacts 建構 | Trigger Artifacts build

        Args:
            project_id (str):
                專案 ID | Project ID

        Returns:
            dict:
                Artifacts 建構資訊 | Artifacts build information
        """
        artifacts_url = f"{self._projects_url}/{project_id}/artifacts"
        return self._request("POST", artifacts_url)

    def download_artifacts(
        self, project_id: str,
        path: Path = None,
        artifact_name: str = "artifact.zip",
        extract_path: Path = None
    ):
        """獲取 Artifacts 下載連結 | Get Artifacts download URL

        Args:
            project_id (str):
                專案 ID | Project ID
            path (Path):
                儲存檔案的路徑 (若為 None 的話，將會儲存於 pooch 的快取中) | Path to save the file (if None, it will be saved in the pooch cache) # noqa
            artifact_name (str):
                Artifacts 檔案名稱 | Artifacts file name (default: "artifact.zip")
            extract_path (Path):
                解壓縮路徑 | Extract path
        """
        artifacts_url = f"{self._projects_url}/{project_id}/artifacts/download"

        if extract_path is not None:
            extract_path = Path(extract_path)
            extract_dir_path = Unzip(extract_dir=extract_path.absolute())
        else:
            extract_dir_path = None

        try:
            retrieve(
                url=artifacts_url,
                path=path,
                fname=artifact_name,
                known_hash=None,
                processor=extract_dir_path,
                downloader=HTTPDownloader(headers=self._api_headers)
            )
        except Exception as e:
            logger.error(f"Download Failed! Error: {str(e)}")
