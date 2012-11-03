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

function setUrlParam(name,value){
    var search;
    if (getUrlParam(name)){
        search =location.search.replace(new RegExp('([?|&]'+name + '=)' + '(.+?)(&|$)'),"$1"+encodeURIComponent(value)+"$3");
    }else if(location.search.length){
        search = location.search +'&'+name + '=' +encodeURIComponent(value);
    }else{
        search = '?'+name + '=' +encodeURIComponent(value);
    }
    //console.log("search:" + decodeURIComponent(search));
//    document.location.href += search;
    document.location.search = search;
}