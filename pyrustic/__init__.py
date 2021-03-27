from pyrustic.version import __version__
try:
    import importlib.metadata as dist_info
except ImportError:
    import importlib_metadata as dist_info


def dist(name, target=None):  # TODO: implement target=None or path to blah blah...
    """
    DESCRIPTION:
        Use this function to get some info about a distribution package
    PARAM:
        name: the distribution name, example: "wheel"
    RETURN:
        A dict with these keys:
            name, author, author_email, description, home_page,
            maintainer, maintainer_email, version
        All values are strings.
    """
    metadata_cache = None
    try:
        metadata_cache = dist_info.metadata(name)
    except Exception:
        pass
    keys = (("author", "Author"),
            ("author_email", "Author-email"),
            ("description", "Summary"),
            ("home_page", "Home-page"),
            ("maintainer", "Maintainer"),
            ("maintainer_email", "Maintainer-email"),
            ("version", "Version"))
    data = None
    if metadata_cache:
        data = {"name": name}
        for item in keys:
            if item[1] in metadata_cache:
                data[item[0]] = metadata_cache[item[1]]
    return data
