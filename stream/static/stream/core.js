/**
 * General library
 * @return {*}
 */
function getLatestPostTime() {
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

function getURLParameter(name) {
    return decodeURIComponent(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,""])[1]
    );
}

/**
 * App functions
 */
function app() {
    this.tmpl = new tmpl();
    this.ajax = new ajax();
    this.render = new render();
}

function tmpl() {
    this.streamPost = ' <div class="streamPost" data-id="{{ id }}" data-time="{{ time }}"> <div class="streamPostHeader"> {{ time }}@{{ user }}<br /> {{ id }}:{{ title }}<br /> </div> <br /> <div class="streamPostBody"> <p>{{ body }}</p> </div> <br /> <div class="streamPostFooter"> actions: <ul class="streamPostActions"> <li><a href="#" class="reply" data-postid="{{ id }}">reply</a></li> <li><a href="#" class="thread" data-postid="{{ id }}">thread</a></li> </ul> </div> <br/> <div class="streamPostExpand"> <div class="liveTags"> tags: <ul> {{#each tags}} <li> <div class="liveTag"> {{#if myvote}} <b>{{ name }}</b>-{{ votes }} {{else}} <a href="#" class="voteTag" data-id="{{ id }}">{{ name }}</a>-{{ votes }} {{/if}} </div> </li> {{/each}} <li><textarea class="tagText"></textarea><a href="#" class="addTag">add tag</a></li> </ul> </div> <br /> <div class="streamPostPush"> <ul> {{#each pushes}} <li> {{ body }} @{{ user }} </li> {{/each}} </ul> </div> <textarea class="streamPushTextbox"></textarea> <a href="#">push</a> </div> </div> <br /> <div>====================================================</div> <br />';
    this.push = '';
}

function ajax() {

    this.loadPosts = function(event) {
        if (event != null)
            event.preventDefault();
        $.ajax({
            url: '/api/post/get/', //'{% url stream.views.api_get_posts %}',
            type: 'GET',
            data: {
                't': getURLParameter('t'),
                'd': getLatestPostTime()
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                noodle.render.renderMsg(data.msg);
                noodle.render.renderPosts(data.posts);
            }
        });
    };

    this.newPost = function(event) {
        console.log($('textarea.newPostTitle').val());
        event.preventDefault();
        $.ajax({
            url: 'api/post/new/', //'{% url stream.views.api_new_post %}',
            type: 'POST',
            data: {
                'title': $('textarea.newPostTitle').val(),
                'body': $('textarea.newPostBody').val(),
                'tags': $('textarea.newPostTags').val()
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                noodle.render.renderMsg(data.msg);
            }
        });
    };

    this.replyPost = function(event) {
        event.preventDefault();
        console.log($(event.target).data('postid'));
        console.log(getLatestPostTime());
    };

    this.pushPost = function(event) {
    };

    this.tagPost = function(event) {
        event.preventDefault();
        var $target = $(event.target);
        console.log($target.prev('textarea.tagText').val());
    };

    this.voteTag = function(event) {
        event.preventDefault();
        var $target = $(event.target);
        $.ajax({
            url: '/api/tag/vote/',//'{% url stream.views.api_vote_live_tag %}',
            type: 'GET',
            data: {
                'i': $target.data('id')
            },
            dataType: 'json',
            success: function(data) {
                if (data.votes == null) {
                    noodle.render.renderMsg("fail to vote the tag");
                } else {
                    noodle.render.renderMsg("votes = " + data.votes);
                }
            }
        });
    };

    this.loadThread = function(event) {
        var $target = $(event.target);
        // alert("load thread. id:" + $target.attr("postid"));
        alert("load thread. postid:" + event.target.title);
    };

    this.loadChannels = function(event) {
    };

    this.newChannel = function(event) {

    };

    this.tagChannel = function(event) {
    };
}

function render() {

    this.renderMsg = function(msg) {
        //console.log("[msg] " + msg);
        $("#msg").text("[msg] " + msg);
    };

    this.renderPosts= function(posts) {
        if (posts.length == 0) {
            $(".loadPosts").hide();
        }
        for (var i = 0; i < posts.length; i++) {
            var tmpl = Handlebars.compile(noodle.tmpl.streamPost);
            var html = tmpl(posts[i]);
            $("#streamBody").append(html);
        }
    };
}

var noodle = new app();

/**
 * Posts data, used for json test
 * @type {Object}
 */
var jpost = {
    "body": "",
    "title": "",
    "tags": [{
        "myvote": false,
        "votes": 0,
        "type": "FN",
        "id": 1,
        "name": "like"}, {
        "myvote": false,
        "votes": 0,
        "type": "FN",
        "id": 2,
        "name": "pin"}, {
        "myvote": false,
        "votes": 0,
        "type": "NN",
        "id": 3,
        "name": "test"}],
    "user": "uuu1",
    "time": "2012-09-27 04:46:38.494626+00:00",
    "id": 1
};

var post1 = {
    "id": 1,
    "threadId": 10,
    "user": "user1",
    "time": "time data",
    "title": "post1 test",
    "body": "this is a post1 test...\n 2nd line test. New line is still a bug",
    "pushes": [
        {
            "id": 1,
            "user": "user5",
            "time": "time data",
            "body": "this is a push body 1"
        },
        {
            "id": 2,
            "user": "user6",
            "time": "time data",
            "body": "this is a push body 2"
        }
    ],
    "tags": ["tag1", "tag2"],
    "likeNum": 8
};
var posts = [post1, post1, post1];
var testData = {
    "msg": "ok",
    "posts": posts
};