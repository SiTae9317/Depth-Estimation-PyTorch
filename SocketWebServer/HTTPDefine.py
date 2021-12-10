GET = 'Get'
POST = 'Post'
DELETE = 'Delete'

HEADER_VERSION10 = "HTTP/1.0";
HEADER_VERSION11 = "HTTP/1.1";
HEADER_VERSION20 = "HTTP/2.0";

HEADER_HOST = "Host";
HEADER_USER_AGENT = "User-Agent";
HEADER_ACCEPT = "Accept";
HEADER_ACCEPT_ENCODING = "Accept-Encoding";
HEADER_CONTENT_TYPE = "Content-Type";
HEADER_CONTENT_LENGTH = "Content-Length";
HEADER_CONNECTION = "Connection";

CUSTOM_SERVER = "CustomServer";

ACCEPT_ACC = "*/*";
ACCEPT_TEXT_HTML = "text/html";
ACCEPT_IMAGE = "image/*";

ACCEPT_ENCODING_BR = "br";
ACCEPT_ENCODING_IDENTITY = "identity";
ACCEPT_ENCODING_GZIP = "gzip";
ACCEPT_ENCODING_COMPRESS = "compress";
ACCEPT_ENCODING_DEFLATE = "deflate";

CONNECTION_KEEP_ALIVE = "keep-alive";
CONNECTION_CLOSE = "close";

CONTENT_TYPE_OCTETSTREAM = "application/octet-stream";
CONTENT_TYPE_TEXT_HTML = "text/html";
CONTENT_TYPE_MULTIPART = "multipart/form-data";

EQUAL = "=";
SEMICOLON = ";";
UTF8 = "utf-8";
LINEEND = "\r\n";

BOUNDARY = "boundary";
CHARSET = "charset";

statusCode = {}
statusCode["100"] = "100 Continue"
statusCode["101"] = "101 Switching Protocols"

statusCode["200"] = "200 OK"
statusCode["201"] = "201 Created"
statusCode["202"] = "202 Accepted"
statusCode["203"] = "203 Non-Authoritative Information"
statusCode["204"] = "204 No Content"
statusCode["205"] = "205 Reset Content"
statusCode["206"] = "206 Partial Content"

statusCode["300"] = "300 Multiple Choices"
statusCode["301"] = "301 Moved Permanently"
statusCode["302"] = "302 Found"
statusCode["303"] = "303 See Other"
statusCode["304"] = "304 Not Modified"
statusCode["305"] = "305 Use Proxy"
statusCode["307"] = "307 Temporary Redirect"

statusCode["400"] = "400 Bad Request"
statusCode["401"] = "401 Unauthorized"
statusCode["402"] = "402 Payment Required"
statusCode["403"] = "403 Forbidden"
statusCode["404"] = "404 Not Found"
statusCode["405"] = "405 Method Not Allowed"
statusCode["406"] = "406 Not Acceptable"
statusCode["407"] = "407 Proxy Authentication Required"
statusCode["408"] = "408 Request Time-out"
statusCode["409"] = "409 Conflict"
statusCode["410"] = "410 Gone"
statusCode["411"] = "411 Length Required"
statusCode["412"] = "412 Precondition Failed"
statusCode["413"] = "413 Request Entity Too Large"
statusCode["414"] = "414 Request-URI Too Large"
statusCode["415"] = "415 Unsupported Media Type"
statusCode["416"] = "416 Requested range not satisfiable"
statusCode["417"] = "417 Expectation Failed"

statusCode["500"] = "500 Internal Server Error"
statusCode["501"] = "501 Not Implemented"
statusCode["502"] = "502 Bad Gateway"
statusCode["503"] = "503 Service Unavailable"
statusCode["504"] = "504 Gateway Time-out"
statusCode["505"] = "505 HTTP Version not supported"