export const sendRequest = (url, 
    body, 
    method, 
    isAsync, 
    fOnLoad, 
    fLoadStart, 
    fLoadEnd, 
    header, 
    value, 
    responseType) => 
{
    let httpRequest = new XMLHttpRequest();

    try {
        httpRequest.onloadstart = fLoadStart;
        httpRequest.onloadend = fLoadEnd;
    }
    catch { }

    httpRequest.onload = fOnLoad;

    httpRequest.onerror = () => {
        alert("Не предвиденная ошибка, попробуйте позже.")
    };

    httpRequest.open(method, url);
    if (responseType) httpRequest.responseType = responseType;
    if (header) httpRequest.setRequestHeader(header, value);
    httpRequest.send(body);
}