import hashlib
from sha3 import keccak_256


support_heads = ['content-sha256', 'transaction-hash', 'object-id', 'redundancy-index', 'resource',
                 'date', 'range', 'piece-index', 'content-type', 'content-md5', 'unsigned-msg', 'user-address']


def get_host_info(req):
    host = req.headers.get("host")
    if host != "":
        return host
    if req.host != "":
        return req.host
    return req.url.host


def get_canonical_headers(req, support_headers):
    content = []
    contain_host_header = False
    sort_headers = get_sorted_headers(req, support_headers)
    header_map = {key.lower(): data for key, data in req.headers.items()}

    for header in sort_headers:
        content.append(header.lower() + ':')

        if header != 'host':
            for i, v in enumerate(header_map[header]):
                if i > 0:
                    content.append(',')
                trim_val = ' '.join(v.split())
                content.append(trim_val)
            content.append('\n')
        else:
            contain_host_header = True
            content.append(get_host_info(req))
            content.append('\n')

    if not contain_host_header:
        content.append(get_host_info(req))
        content.append('\n')
    return ''.join(content)


def get_sorted_headers(req, support_map):
    sign_headers = []
    for k in req.headers:
        if k.lower() in support_map:
            sign_headers.append(k.lower())
    sign_headers.sort()
    return sign_headers


def get_signed_headers(req, support_headers):
    return ';'.join(get_sorted_headers(req, support_headers))


def get_canonical_request(req, support_headers):
    req.url = req.url._replace(query = req.url.query.replace('+', '%20'))
    canonical_request = '\n'.join([
        req.method,
        encode_path(req.url.path),
        req.url.query,
        get_canonical_headers(req, support_headers),
        get_signed_headers(req, support_headers),
    ])
    return canonical_request

def get_msg_to_sign(req):
    headers = init_support_headers()
    sign_bytes = hashlib.sha256(get_canonical_request(req, headers).encode('utf-8')).digest()
    return keccak_256(sign_bytes).digest()

def init_support_headers():
    support_map = {}
    for header in support_heads:
        support_map[header] = {}
    return support_map