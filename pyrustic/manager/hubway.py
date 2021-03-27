from pyrustic.gurl import dict_to_json_body
from pyrustic.manager.misc import funcs
import urllib.parse


class Catapult:
    def __init__(self, gurl, owner, repo):
        self._gurl = gurl
        self._owner = owner
        self._repo = repo

    def publish(self, name, tag_name,
                target_commitish, description,
                prerelease, draft,
                asset_path, asset_name, asset_label):
        """
        Return {"meta_code":, "status_code", "status_text", "data"}
        meta code:
            0- success
            1- failed to create release (check 'status_code', 'status_text')
            2- failed to upload asset (check 'status_code', 'status_text')
        """
        publishing_result = {"meta_code": None, "status_code": None,
                            "status_text": None, "data": None}
        # == create release
        response = self._create_release(self._owner, self._repo, name, tag_name,
                                        target_commitish, description,
                                        prerelease, draft)
        code = response.code
        if code != 201:
            publishing_result["meta_code"] = 1
            publishing_result["status_code"] = code
            publishing_result["status_text"] = response.status[1]
            return publishing_result
        # == upload asset
        upload_url = response.json["upload_url"]
        response = self._upload_asset(upload_url, asset_path,
                                      asset_name, asset_label)
        code = response.code
        if code != 201:
            publishing_result["meta_code"] = 2
            publishing_result["status_code"] = code
            publishing_result["status_text"] = response.status[1]
            return publishing_result
        publishing_result["meta_code"] = 0
        return publishing_result

    def _create_release(self, owner, repo, name, tag_name, target_commitish,
                        description, prerelease, draft):
        res = "/repos/{}/{}/releases".format(owner, repo)
        body = {"tag_name": tag_name, "target_commitish": target_commitish,
                "name": name, "body": description, "draft": draft,
                "prerelease": prerelease}
        body = dict_to_json_body(body)
        response = self._gurl.request(funcs.get_hub_url(res),
                                      body=body, method="POST")
        return response

    def _upload_asset(self, upload_url, path, name, label):
        url = upload_url.replace("{?name,label}", "?{}")
        parameters = urllib.parse.urlencode({"label": label, "name": name})
        url = url.format(parameters)
        with open(path, "rb") as file:
            data = file.read()
        header = {"Content-Type": "application/zip"}
        response = self._gurl.request(url, body=data, method="POST",
                                      headers=header)
        return response


def repo_description(gurl, owner, repo):
    """
    Returns: (status_code, status_text, data)
    data = {"created_at": date, "description": str,
            "stargazers_count": int, "subscribers_count": int}
    """
    res = "/repos/{}/{}".format(owner, repo)
    response = gurl.request(funcs.get_hub_url(res))
    code = response.code
    json = response.json
    data = {}
    if code == 304:
        json = response.cached_response.json
    if (code in (200, 304)) and json:
        data["description"] = json["description"]
        date = json["created_at"]
        data["created_at"] = _badass_iso_8601_date_parser(date)
        data["stargazers_count"] = json["stargazers_count"]
        data["subscribers_count"] = json["subscribers_count"]
    return *response.status, data


def latest_release(gurl, owner, repo):
    """
    Returns: (status_code, status_text, data}
    data = {"tag_name": str, "published_at": date,
            "downloads_count": int}
    """
    res = "/repos/{}/{}/releases/latest".format(owner, repo)
    response = gurl.request(funcs.get_hub_url(res))
    code = response.code
    json = response.json
    data = {}
    if code == 304:
        json = response.cached_response.json
    if (code in (200, 304)) and json:
        data["tag_name"] = json["tag_name"]
        date = json["published_at"]
        data["published_at"] = _badass_iso_8601_date_parser(date)
        data["downloads_count"] = _downloads_counter(json)
    return *response.status, data


def latest_releases_downloads(gurl, owner, repo, maxi=10):
    """
    Returns: (status_code, status_text, data}
    data = int, downloads count
    """
    res = "/repos/{}/{}/releases?per_page={}".format(owner, repo, maxi)
    response = gurl.request(funcs.get_hub_url(res))
    code = response.code
    json = response.json
    data = 0
    if code == 304:
        json = response.cached_response.json
    if (code in (200, 304)) and json:
        for release in json:
            data += _downloads_counter(release)
    return *response.status, data


def _downloads_counter(json):
    count = 0
    for asset in json["assets"]:
        count += asset["download_count"]
    return count


def _badass_iso_8601_date_parser(date):
    # YYYY-MM-DDTHH:MM:SSZ
    date = date.rstrip("Z")
    date_part, time_part = date.split("T")
    months = ("Jan", "Feb", "March", "April", "May", "June", "July",
             "Aug", "Sept", "Oct", "Nov", "Dec")
    year, month, day = date_part.split("-")
    text = "{} {} {} at {}".format(day, months[int(month) - 1], year, time_part)
    return text
