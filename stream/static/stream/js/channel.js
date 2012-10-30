Noodle.Channel = (function() {

    /* private variables and functions */
    var testJsonData = [
        {
            cid: 1,
            tags: ["tag1", "tag2", "tag3"]
        },
        {
            cid: 2,
            tags: ["tag1", "tag2", "tag3"]
        }
    ];

    var template =
        '<div class="channel">' +
        '<a class="channel-btn" href="#" data-tags="{{ tags }}">channel id: {{ cid }}</a>' +
        '<textarea class="channel-new-tag-txt">new tag</textarea>' +
        '<a class="channel-new-tag-btn" href="#" data-cid="1">add a tag</a>' +
        '</div>';

    var getChannels = function(event) {

    };

    /* public functions */
    var clickChannel = function(event) {
        event.preventDefault();

        /* ajax: load posts of the channel's tags*/
        var $target = $(event.target);
        $target.data('tags');


        /* Set url as the channel's tag*/
        setUrlParam('t', "中文+t2+t3+t4");
        console.log("get:" + getUrlParam('t'));
    };

    var loadChannels = function(event) {
        /* get channels */
        $.ajax({
            url: '/api/cha/get/',
            type: 'GET',
            data: {
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert == null) {
                    // render channels
                    renderChannels(channels);
                } else {
                    // render alert
                    Noodle.Alert.render(alert);
                }
            }
        });
        renderChannels(testJsonData);
    };

    var addChannel = function(event) {
        // create a new channel
        // if success, render channels
    };

    var tagChannel = function(event) {
        // Get tags from text area
        // Ajax to add a tag, if successes, render the channel
    };

    var renderChannels = function(channels) {
        var $box = $("div.channel-box");
        $box.empty();
        var tmpl = Handlebars.compile(template);

        for (var i = 0; i < channels.length; i++) {
            var html = tmpl(channels[i]);
            $box.append(html);
            console.log("html" + html);
        }
    };

    return {
        click: clickChannel,
        load: loadChannels,
        render: renderChannels,
        tag: tagChannel,
        add: addChannel
    }
})();
