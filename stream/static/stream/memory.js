var app = {
    'templates': {
        'push': null,
        'streamPost': null
    }
};
app.templates.streamPost = ' <div class="streamPost" data-postid="{{ id }}"> <div class="streamPostHeader"> <p>{{ title }} @{{ user }}</p> </div> <div class="streamPostBody"> <p>{{ body }}</p> </div> <div class="streamPostFooter"> <ul class="streamPostActions"> <li><a href="#" class="reply" data-postid="{{ id }}">reply</a></li> <li><a href="#" class="like" data-postid="{{ id }}">like</a></li> <li><a href="#" class="thread" data-postid="{{ id }}">thread</a></li> </ul> <ul class="streamPostTags"> {{#each tags}} <li><a href="#" class="postTag" data-postid="{{ id }}">{{ this }}</a></li> {{/each}} </ul> </div> <div class="streamPostExpand"> <div class="streamPostPush"> <ul> {{#each pushes}} <li> {{ body }} @{{ user }} </li> {{/each}} </ul> </div> <textarea class="streamPushTextbox"></textarea> <a href="#">push</a> </div> </div> <div>====================================================</div>';
app.templates.push = '';

/**
 * Posts data, used for json test
 * @type {Object}
 */
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
var posts = [
    post1,
    post1,
    post1,
];
var testData = {
    "msg": "ok",
    "posts": posts
};