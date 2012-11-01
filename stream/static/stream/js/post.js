Noodle.Tag = (function() {
    var template =
        '{{#each tags}}' +
        '<div class="tag">{{ name }}</div>' +
        '{{/each}}';

    var testJson = {
        tags: [{
            name: "tag1"
        },{
            name: "tag2"
        },{
            name: "tag3"
        }]
    };

    var render = function(data) {
        var tmpl = Handlebars.compile(template);
        var html = tmpl(data);
        return new Handlebars.SafeString(html);
    };

    return {
        json: testJson,
        render: render
    }
})();

Noodle.LiveTag = (function() {

    var template =
        '{{#each tags}}' +
        '<div class="livetag_box">' +
        '{{#if myvote}}' +
        '<b>{{ name }}</b>-{{ votes }}' +
        '{{else}}' +
        '<a href="#" class="livetag_vote" data-id="{{ id }}">{{ name }}</a>-{{ votes }}' +
        '{{/if}}' +
        '</div>' +
        '{{/each}}';
//        '<textarea class="new_tag"></textarea>' +
//        '<a href="#" class="tag_post">add tag</a>';

    var testJson = {
        tags: [{
            "myvote": true,
            "votes": 10,
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
            "name": "test"}]
    };

    var render = function(data) {
        var tmpl = Handlebars.compile(template);
        var html = tmpl(data);
        return new Handlebars.SafeString(html);
    };

    return {
        json: testJson,
        render: render
    }
})();

Noodle.Push = (function() {
    var template = '{{#each pushes}}' +
        '<div class="push">' +
        '{{ body }}@{{ user }}' +
        '<div class="postLiveTag">' +
        '{{#if myvote}}' +
        '<b>{{ name }}</b>-{{ votes }}' +
        '{{else}}' +
        '<a href="#" class="voteTag" data-id="{{ id }}">{{ name }}</a>-{{ votes }}{{/if}}</div></div><br>{{/each}}';

    var render = function(data) {
        var tmpl = Handlebars.compile(template);
        var html = tmpl(data);
        return new Handlebars.SafeString(html);
    };

    return {
        render: render
    }
})();


Noodle.Post = (function() {
    var template = '<div class="post" id="po{{ id }}" data-id="{{ id }}" data-time="{{ time }}">' +
        '<div class="postHeader">' +
        '{{ time }}@{{ user }}<br />' +
        '{{ id }}-{{ title }}<br />' +
        '</div><br>' +
        '<div class="postBody">' +
        '<p>{{ body }}</p>' +
        '</div><br>' +
        '<div class="postFooter">' +
        '<div class="postActions">' +
        '<a href="#" class="post-reply" data-postid="{{ id }}">reply</a></div></div><br>' +
        '<div class="postExpand">' +
        '<div class="livetag_box">{{ livetagHtml }}</div><br>' +
        '<div class="push_box">{{ pushHtml }}</div>' +
        '<div class="pushForm">' +
        'push: <textarea class="pushText"></textarea></div>' +
        '<div class="postReplyForm"></div></div></div>' +
        '<p>==========================================</p>';

    var testJson = [{
        "body": "this is a test post's body",
        "title": "this is a test post's title",
        "pushes": [{
            "body": "this is a push body",
            "user": "uuu2",
            "tag": {
                "name": "like",
                "votes": 10
            }
        }],
        "tags": [{
            "myvote": true,
            "votes": 10,
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
    }];


    var getPosts = function(tags, newestPostTime, oldestPostTime) {

    };

    /* public functions */
//    var loadPosts = function(args) {
//        args = {
//            tags: args.tags || "",
//            type: args.type || ""
//        };
//        switch(args.type) {
//            /* load a new post stream  with given tags*/
//            case 'reload':
//                break;
//            /* load more older posts, pagination */
//            case 'old':
//                break;
//            /* insert new posts */
//            case 'new':
//                break;
//        }
//    };

    var loadPosts = function(event) {
        console.log("lp" + Noodle.Dom.Post.FORM_BODY);
        if (event != null)
            event.preventDefault();
        $.ajax({
            url: '/api/post/get/',
            type: 'GET',
            data: {
                't': getUrlParam('t'),
                'd': getOldestPostTime()
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    if (posts.length == 0)
                        $(".loadPosts").hide();

                    renderPosts(data.posts);
                }
            }
        });
    };

    var autotagPost = function(event) {
        console.log('autotag');
        event.preventDefault();
        $.ajax({
            url: 'api/post/autotag/',
            type: 'POST',
            data: {
                'title': $(Noodle.Dom.Post.FORM_TITLE).val(),
                'body': $(Noodle.Dom.Post.FORM_BODY).val()
//                'tags': $(Noodle.Dom.Post.FORM_TAG).val()
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    _renderFormTagBox(data);
                }
            }
        });
    };

    var newPost = function(event) {
        event.preventDefault();
        $.ajax({
            url: 'api/post/new/',
            type: 'POST',
            data: {
                'title': $(Noodle.Dom.Post.FORM_TITLE).val(),
                'body': $(Noodle.Dom.Post.FORM_BODY).val(),
                'tags': $(Noodle.Dom.Post.FORM_TAG).val()
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                Noodle.Alert.render(data.alert);
            }
        });
    };

    var replyPost = function(event) {
        event.preventDefault();
        console.log($(event.target).data('id'));
        console.log(getLatestPostTime());
    };

    var pushPost = function(event) {
        // if enter key is pressed
        if (event.which == 13) {
            var $target = $(event.target);
            console.log($target.val());
            $.ajax({
                url: 'api/post/pu/',
                type: 'POST',
                data: {
                    'id': $target.parents('div.post').data('id'),   // post id
                    'body': $target.val() // push body
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data);
                    noodle.render.renderAlert(data.msg);
                    noodle.render.renderPushes(data.pushes);
                }
            });
            $target.val("");
            return false;
        }
    };

    var tagPost = function(event) {
        event.preventDefault();
        var $target = $(event.target);
        $.ajax({
            url: 'api/post/tag/',
            type: 'GET',
            data: {
                'id': $target.parents('div.post').data('id'),   // post id
                'tag': $target.prev('textarea.tagText').val()   // tag name
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                noodle.render.renderAlert(data.msg);
                noodle.render.renderTags(data.tags);
            }
        });
    };

    var voteTag = function(event) {
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
                    noodle.render.renderAlert("fail to vote the tag");
                } else {
                    noodle.render.renderAlert("votes = " + data.votes);
                }
            }
        });
    };

    var _renderFormTagBox = function(data) {
        var $box = $(Noodle.Dom.Post.FORM_TAG_BOX);
        var html = Noodle.Tag.render(data);
        console.log(html);
        $box.append(String(html));
    };

    var renderPosts = function(posts) {
        var $box = $(Noodle.Dom.Post.BOX);
        for (var i = 0; i < posts.length; i++) {
            posts[i].livetagHtml = Noodle.LiveTag.render(posts[i]);
            posts[i].pushHtml = Noodle.Push.render(posts[i]);
            var tmpl = Handlebars.compile(template);
            var html = tmpl(posts[i]);
            console.log("test");
            console.log(html);
            $box.append(html);
        }
    };

    return {
        json: testJson,
        load: loadPosts,
        render: renderPosts,
        new: newPost,
        reply: replyPost,
        push: pushPost,
        tag: tagPost,
        autotag: autotagPost
    }
})();
