/* Init page */
$( function() {
    noodle.ajax.loadPosts();
    noodle.ajax.getChannels();
    registEvents();
});

/* register elements with specific ajax actions */
var registEvents = function() {
    /* channel */
    $(document).on("click", "a.channel-btn", noodle.channel.clickChannel);
    $(document).on("click", "a.viewThread", noodle.channel.newChannel);
    $(document).on("click", "a.viewThread", noodle.channel.tagChannel);
    $(document).on("click", "a.channel-btn", noodle.channel.getChannels);

    /* stream */
    $(document).on("click", "a.loadPosts", noodle.ajax.loadPosts);
    $(document).on("click", "a.newPost", noodle.ajax.newPost);
    $(document).on("click", "a.replyPost", noodle.ajax.replyPost);
    $(document).on("keypress", "textarea.pushText", noodle.ajax.pushPost);
    $(document).on("click", "a.tagPost", noodle.ajax.tagPost);
    $(document).on("click", "a.voteTag", noodle.ajax.voteTag);

    /* kaleido */
    $(document).on("click", "a.viewThread", noodle.ajax.loadThread); // not implemented
};

function Noodle() {
    this.tmpl = new Templates();
    this.ajax = new Ajax();
    this.render = new Render();
    this.channel = new Channel();
}

function Templates() {
    this.streamPost = '<div class="streamPost" data-id="{{ id }}" data-time="{{ time }}"> ' +
        '<div class="streamPostHeader"> {{ time }}@{{ user }}<br /> {{ id }}:{{ title }}<br /> </div> <br /> ' +
        '<div class="streamPostBody"> <p>{{ body }}</p> </div> <br /> ' +
        '<div class="streamPostFooter"> actions: <ul class="streamPostActions"> <li><a href="#" class="reply" data-postid="{{ id }}">reply</a></li> <li><a href="#" class="thread" data-postid="{{ id }}">thread</a></li> </ul> </div> <br/> ' +
        '<div class="streamPostExpand"> <div class="liveTags"> tags: <ul> {{#each tags}} <li> <div class="liveTag"> {{#if myvote}} <b>{{ name }}</b>-{{ votes }} {{else}} <a href="#" class="voteTag" data-id="{{ id }}">{{ name }}</a>-{{ votes }} {{/if}} </div> </li> {{/each}} <li><textarea class="tagText"></textarea><a href="#" class="addTag">add tag</a></li> </ul> </div> <br /> <div class="streamPostPush"> <ul> {{#each pushes}} <li> {{ body }} @{{ user }} </li> {{/each}} </ul> </div> <textarea class="streamPushTextbox"></textarea> <a href="#">push</a> </div> </div> <br /> <div>====================================================</div> <br />';
    this.push = '';
}

function Ajax() {

    /*** Methods related to post ***/
    this.loadPosts = function(event) {
        if (event != null)
            event.preventDefault();
        $.ajax({
            url: '/api/post/get/', //'{% url stream.views.api_get_posts %}',
            type: 'GET',
            data: {
                't': getUrlParam('t'),
                'd': getOldestPostTime()
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                noodle.render.renderAlert(data.msg);
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
                noodle.render.renderAlert(data.msg);
            }
        });
    };

    this.replyPost = function(event) {
        event.preventDefault();
        console.log($(event.target).data('id'));
        console.log(getLatestPostTime());
    };

    this.pushPost = function(event) {
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

    this.tagPost = function(event) {
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
                    noodle.render.renderAlert("fail to vote the tag");
                } else {
                    noodle.render.renderAlert("votes = " + data.votes);
                }
            }
        });
    };

    this.loadPush = function(event) {

    };

    this.loadThread = function(event) {
        var $target = $(event.target);
        // alert("load thread. id:" + $target.attr("postid"));
        alert("load thread. postid:" + event.target.title);
    };

}

function Post() {

}

function Channel() {
    this.clickChannel = function(event) {
        if (event != null) event.preventDefault();

        /* Set url as the channel's tag*/
        var $target = $(event.target);
        console.log($target.data('tags'));
    };

    this.getChannels = function(event) {
        var $target = $(event.target);
        $.ajax({
            url: '/api/cha/get/',
            type: 'GET',
            data: {
                'i': $target.data('id')
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert == null) {
                    // render channels
                } else {
                    // render alert
                }
            }
        });
    };

    this.newChannel = function(event) {

    };

    this.tagChannel = function(event) {
        // Get tags from text area
        // Ajax to add a tag, if successes, render the channel
        //
    };

    this.renderChannels = function(channels) {
    };
}

function Render() {

    this.renderAlert = function(alert) {
        $("#msg").text("[msg] " + alert);
    };

    this.renderPosts = function(posts) {
        if (posts.length == 0) {
            $(".loadPosts").hide();
        }

        var $streamBody = $("#streamBody");
        for (var i = 0; i < posts.length; i++) {
            var tmpl = Handlebars.compile(noodle.tmpl.streamPost);
            var html = tmpl(posts[i]);
            $streamBody.append(html);
        }
    };

    this.renderTags = function(tags, postID) {
        var $div = $("#po"+postID).children("div.liveTags");
        for (var i = 0; i < tags.length; i++) {
            var tmpl = Handlebars.compile(noodle.tmpl);
            var html = tmpl(tags[i]);
            $div.append(html);
        }
    };

    this.renderPushes = function(pushes, postID) {
        var $div = $("#po"+postID).children("div.pushes");
        for (var i = 0; i < pushes.length; i++) {
            var tmpl = Handlebars.compile(noodle.tmpl);
            var html = tmpl(pushes[i]);
            $div.append(html);
        }
    };

}
var noodle = new Noodle();

var user = {
    channels: {}
};
var c1 = {
    id: 1,
    tags: ["tag1", "tag2", "tag3"]
};
var c2 = {
    id: 2,
    tags: ["tag1", "tag2", "tag3"]
};
user.channels[c1.id] = c1.tags;
user.channels[c2.id] = c2.tags;
