Noodle.Tag = (function() {
    var template =
        '{{#each tags}}' +
        '<div class="tag">{{ name }}</div>' +
        '{{/each}}';

    var render = function(data) {
        var tmpl = Handlebars.compile(template);
        var html = tmpl(data);
        return new Handlebars.SafeString(html);
    };

    return {
        render: render
    }
})();

Noodle.LiveTag = (function() {

    var template =
        '{{#each tags}}' +
        '<div class="livetag">' +
        '{{#if myvote}}' +
        '<b><a href="#" class="livetag_unvote" data-tag="{{ id }}">{{ name }}</a>-{{ votes }}</b>' +
        '{{else}}' +
        '<a href="#" class="livetag_vote" data-tag="{{ id }}">{{ name }}</a>-{{ votes }}' +
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

    var renderHtml = function(data) {
        var tmpl = Handlebars.compile(template);
        var html = tmpl(data);
        return new Handlebars.SafeString(html);
    };

    var renderLiveTagBox = function(data, $box) {
        var html = renderHtml(data);
        $box.empty();
        $box.append(String(html));
    };

    var voteLiveTag = function(event) {
        event.preventDefault();
        var $target = $(event.target);
        $.ajax({
            url: '/api/tag/vote/',
            type: 'GET',
            data: {
                't': $target.data('tag')
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    renderLiveTagBox(data, $target.parents(Noodle.Dom.LiveTag.BOX));
                }
            }
        });
    };

    var unvoteLiveTag = function(event) {
        event.preventDefault();
        var $target = $(event.target);
        $.ajax({
            url: '/api/tag/unvote/',
            type: 'GET',
            data: {
                't': $target.data('tag')
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    renderLiveTagBox(data, $target.parents(Noodle.Dom.LiveTag.BOX));
                }
            }
        });
    };

    return {
        json: testJson,
        renderHtml: renderHtml,
        renderBox: renderLiveTagBox,
        vote: voteLiveTag,
        unvote: unvoteLiveTag
    }
})();

Noodle.Push = (function() {
    var template =
        '<div class="push">' +
            '{{ body }} @{{ user }}' +
            '<div class="livetag_box">{{ livetagHtml }}</div>' +
        '</div>';

    var renderBox = function($box, pushes) {
        $box.empty();
        $box.append(renderHtml(pushes));
    };

    var renderHtml = function(pushes) {
        var html = "";
        for (var i = 0; i < pushes.length; i++) {
            pushes[i].livetagHtml = Noodle.LiveTag.renderHtml(pushes[i]);
            var tmpl = Handlebars.compile(template);
            html += tmpl(pushes[i]);
        }
        return html;
    };

    return {
        renderHtml: renderHtml,
        renderBox: renderBox
    }
})();


Noodle.Post = (function() {
    var template =
        '<div class="post" id="po{{ id }}" data-id="{{ id }}" data-time="{{ time }}">' +
        '<p>{{ time }}@{{ user }}</p>' +
        '<p>{{ id }}-{{ title }}</p>' +
        '<p>{{ body }}</p>' +

        '<div class="livetag_box">{{ livetagHtml }}</div>' +

        '<div class="livetag_form">' +
        'tag: <textarea class="livetag_input" data-post={{ id }}></textarea></div>' +

        '<div class="push_box">{{ pushHtml }}</div>' +

        '<div class="push_form">' +
        'push: <textarea class="push_input" data-post={{ id }}></textarea></div>' +

        '<div class="post_reply_form" data-reid="{{ id }}">' +
        '<p class="post_reply_form_title">RE:{{ title }}</p>' +
        'body:<textarea class="post_form_body_input"></textarea>' +
        '<div class="post_form_tag_box"></div>' +
        '<a href="#" class="post_form_autotag_btn">autotag</a> ' +
        '<a href="#" class="post_reply_form_btn">reply</a></div>' +

        '<p>==========================================</p></div>';

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


    var _processAjaxData = function(successFunction) {
        if (data.alert)
            Noodle.Alert.render(data.alert);
        else {
            successFunction();
        }
    };

    var _getPosts = function(tags, oldestPostTime, successFunction) {
        $.ajax({
            url: '/api/post/get/',
            type: 'GET',
            data: {
                't': tags,
                'd': oldestPostTime()
            },
            dataType: 'json',
            success: successFunction
        });
    };

    var _getTags = function($box) {
        var tags = [];
        $box.children(Noodle.Dom.Tag.TAG).each( function(i) {
            tags.push($(this).text());
        });
        return tags;
    };

    var _getPostForm = function(event) {
        var $form = $(event.target).parent('div');
        var title, body, tags, repost;
        if (Noodle.Dom.Post.FORM.indexOf($form.attr('class')) != -1) {
            // new post form
            title = $form.children(Noodle.Dom.Post.FORM_TITLE).val();
            body = $form.children(Noodle.Dom.Post.FORM_BODY).val();
            tags = _getTags($form.children(Noodle.Dom.Post.FORM_TAG_BOX));
            repost = null;
        } else if (Noodle.Dom.Post.REPLY_FORM.indexOf($form.attr('class')) != -1) {
            // reply post form
            title = $form.children(Noodle.Dom.Post.REPLY_FORM_TITLE).text();
            body = $form.children(Noodle.Dom.Post.FORM_BODY).val();
            tags = _getTags($form.children(Noodle.Dom.Post.FORM_TAG_BOX));
            repost = $form.data('reid');
        }
        return {
            title: title,
            body: body,
            tags: tags,
            repost: repost
        };
    };

    var loadPosts = function(event) {
        if (event != null) event.preventDefault();

        var tagstr = getUrlParam('t');
        if (tagstr) {
            // load posts with given tags
        } else {
            // load all posts
        }
        $.ajax({
            url: '/api/post/get/',
            type: 'GET',
            data: {
                't': tagstr,
                'd': getOldestPostTime()
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    if (data.posts.length == 0)
                        $(".loadPosts").hide();
                    renderPosts(data.posts);
                }
            }
        });
    };

    var autotagPost = function(event) {
        event.preventDefault();
        var form = _getPostForm(event);
        $.ajax({
            url: 'api/post/autotag/',
            type: 'POST',
            data: form,
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    _renderTagBox(data, $(event.target).siblings(Noodle.Dom.Post.FORM_TAG_BOX));
                }
            }
        });
    };

    var createPost = function(event) {
        event.preventDefault();
        var form = _getPostForm(event);
        $.ajax({
            url: 'api/post/new/',
            type: 'POST',
            data: form,
            dataType: 'json',
            success: function(data) {
                console.log(data);
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    location.reload(); // refresh the page
                }
            }
        });
    };

    var pushPost = function(event) {
        // if enter key is pressed
        if (event.which == 13) {
            event.preventDefault();
            var $input = $(event.target);
            $.ajax({
                url: 'api/post/push/',
                type: 'POST',
                data: {
                    'post': $input.data('post'),   // post id
                    'body': $input.val() // push body
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data);
                    if (data.alert) {
                        Noodle.Alert.render(data.alert);
                    } else {
                        $input.val("");
                        Noodle.Push.renderBox($input.parent().siblings(Noodle.Dom.Push.BOX), data.pushes);
//                        location.reload(); // refresh the page
                    }
                }
            });
        }
    };

    var tagPost = function(event) {
        // if enter key is pressed
        if (event.which == 13) {
            event.preventDefault();
            var $input = $(event.target);
            console.log($input.val());
            $.ajax({
                url: 'api/post/tag/',
                type: 'POST',
                data: {
                    'post': $input.data('post'),  // post id
                    'tag': $input.val() // tag name
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data);
                    if (data.alert) {
                        console.log("alert");
                        Noodle.Alert.render(data.alert);
                    } else {
                        $input.val("");
                        Noodle.LiveTag.renderBox(
                            data, $input.parent('div').siblings(Noodle.Dom.LiveTag.BOX));
                    }
                }
            });
        }
    };


    var renderPosts = function(posts) {
        var $box = $(Noodle.Dom.Post.BOX);
        for (var i = 0; i < posts.length; i++) {
            posts[i].livetagHtml = Noodle.LiveTag.renderHtml(posts[i]);
            posts[i].pushHtml = new Handlebars.SafeString(
                Noodle.Push.renderHtml(posts[i].pushes));
            var tmpl = Handlebars.compile(template);
            var html = tmpl(posts[i]);
            $box.append(html);
        }
    };

    var _renderTagBox = function(data, $box) {
        var html = Noodle.Tag.render(data);
        $box.empty();
        $box.append(String(html));
    };

    return {
        load: loadPosts,
        create: createPost,
        autotag: autotagPost,
        push: pushPost,
        tag: tagPost
    }
})();
