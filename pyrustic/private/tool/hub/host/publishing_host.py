from pyrustic.gurl import dict_to_json_body
from pyrustic.private.tool.common.funcs import get_hub_url
import urllib.parse


class PublishingHost:
    def __init__(self, gurl, owner, repo):
        self._gurl = gurl
        self._owner = owner
        self._repo = repo

    def publishing(self, name, tag_name,
                   target_commitish, description,
                   prerelease, draft,
                   asset_path, asset_name, asset_label):
        """
        Return {"meta_code":, "status_code", "status_text", "data"}
        meta code:
            0- success
            1- failed to create release (check 'status_code', 'status_text')
            2- failed to upload zip (check 'status_code', 'status_text')
        """
        publishing_result = {"meta_code": None, "status_code": None,
                            "status_text": None, "data": None}
        # == create release
        response = self._create_release(self._owner, self._repo, name, tag_name,
                                        target_commitish, description,
                                        prerelease, draft)
        code = response.code
        if code != 201:
            publishing_result["meta_code"] = 5
            publishing_result["status_code"] = code
            publishing_result["status_text"] = response.status[1]
            return publishing_result
        # == upload asset
        upload_url = response.json["upload_url"]
        response = self._upload_asset(upload_url, asset_path,
                                      asset_name, asset_label)
        code = response.code
        if code != 201:
            publishing_result["meta_code"] = 6
            publishing_result["status_code"] = code
            publishing_result["status_text"] = response.status[1]
            return publishing_result
        publishing_result["meta_code"] = 0
        return publishing_result

    def _publishing(self, name, tag_name,
                 target_commitish, description, prerelease,
                 asset_path, asset_name, asset_label):
        # create release
        response = self._create_release(self._owner, self._repo, name, tag_name,
                                        target_commitish, description,
                                        prerelease)
        code = response.code
        if code == 201:
            # upload asset
            upload_url = response.json["upload_url"]
            response = self._upload_asset(upload_url, asset_path,
                                          asset_name, asset_label)
        return response.status

    def _create_release(self, owner, repo, name, tag_name, target_commitish,
                        description, prerelease, draft):
        res = "/repos/{}/{}/releases".format(owner, repo)
        body = {"tag_name": tag_name, "target_commitish": target_commitish,
                "name": name, "body": description, "draft": draft,
                "prerelease": prerelease}
        body = dict_to_json_body(body)
        response = self._gurl.request(get_hub_url(res), body=body, method="POST")
        return response

    def _upload_asset(self, upload_url, path, name, label):
        url = upload_url.replace("{?name,label}", "?{}")
        parameters = urllib.parse.urlencode({"label": label, "name": name})
        url = url.format(parameters)
        with open(path, "rb") as file:
            data = file.read()
        header = ("Content-Type", "application/zip")
        response = self._gurl.request(url, body=data, method="POST",
                                      headers=(header, ))
        return response
