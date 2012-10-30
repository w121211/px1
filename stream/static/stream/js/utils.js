/** General functions **/

function getOldestPostTime() {
    var $posts = $("div.streamPost");
    if ($posts.length == 0)
        return null;
    var min = Date.now();
    $posts.each( function() {
        t = Date.parse($(this).data('time'));
        if (t < min)
            min = t;
    });
    return new Date(min).toISOString();
}

function getNewestPostTime() {

}

function getUrlParam(name) {
    return decodeURIComponent(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,""])[1]
    );
}

function setURLParam(name, value) {
    name = encodeURI(name);
    value = encodeURI(value);

    var kvp = document.location.search.substr(1).split('&');
    if (kvp == '') {
        document.location.search = '?' + name + '=' + value;
    } else {
        var i = kvp.length; var x; while (i--) {
            x = kvp[i].split('=');
            if (x[0] == name) {
                x[1] = value;
                kvp[i] = x.join('=');
                break;
            }
        }
        if (i < 0) { kvp[kvp.length] = [name, value].join('='); }
    }
    //this will reload the page, it's likely better to store this until finished
    // document.location.search = kvp.join('&');
}
