Noodle.Channel = (function() {

    var template =
        '<div class="channel" data-tags="{{ tags }}" data-channel="{{ id }}">' +
        '<a class="channel_btn" href="#">channel {{ id }}</a><br>' +
        '{{#each tags}}' +
        '<a class="channel_tag_remove_btn" href="#">{{.}}</a><br>' +
        '{{/each}}' +
        '<textarea class="channel_tag_input" data-channel="{{ id }}"></textarea><br>' +
        '<a class="channel_remove_btn" href="#" data-channel="{{ id }}">remove this channel</a><br>' +
        '<p>**************</p></div>';

    var _getChannels = function(event) {
        var tags = $(event.target).parent(Noodle.Dom.Channel.CHANNEL).data('tags');
        return tags.split(',');
    };


    var _clickChannel = function($target) {
        var tags = $target.parent(Noodle.Dom.Channel.CHANNEL).data('tags');
        tags = tags.split(',').join('+');
        setUrlParam('t', tags);
    };

    var clickChannel = function(event) {
        event.preventDefault();
        _clickChannel($(event.target));
    };

    var loadChannels = function(event) {
        $.ajax({
            url: '/api/channel/get/',
            type: 'GET',
            data: null,
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    renderChannelBox(data.channels);
                }
            }
        });
    };

    var addChannel = function(event) {
        $.ajax({
            url: '/api/channel/add/',
            type: 'POST',
            data: null,
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    renderChannelBox(data.channels);
                }
            }
        });
    };

    var removeChannel = function(event) {
        $.ajax({
            url: '/api/channel/remove/',
            type: 'POST',
            data: {
                'channel': $(event.target).data('channel')
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    renderChannelBox(data.channels);
                }
            }
        });
    };

    var addTag = function(event) {
        var $input = $(event.target);
        if (event.which == 13) {
            event.preventDefault();
            $.ajax({
                url: '/api/channel/tag/add/',
                type: 'POST',
                data: {
                    'channel': $input.data('channel'),
                    'tag': $input.val()
                },
                dataType: 'json',
                success: function(data) {
                    if (data.alert)
                        Noodle.Alert.render(data.alert);
                    else {
                        renderChannelBox(data.channels);
//                        _clickChannel($input.siblings(Noodle.Dom.Channel.CHANNEL_BTN))
                    }
                }
            });
        }
    };

    var removeTag = function(event) {
        event.preventDefault();
        var $target= $(event.target);

        console.log($target.parent(Noodle.Dom.Channel.CHANNEL).data('channel'));
        $.ajax({
            url: '/api/channel/tag/remove/',
            type: 'POST',
            data: {
                'channel': $target.parent(Noodle.Dom.Channel.CHANNEL).data('channel'),
                'tag': $target.text()
            },
            dataType: 'json',
            success: function(data) {
                if (data.alert)
                    Noodle.Alert.render(data.alert);
                else {
                    renderChannelBox(data.channels);
//                    _clickChannel($target.siblings(Noodle.Dom.Channel.CHANNEL_BTN))
                }
            }
        });
    };

    var renderChannelBox = function(channels) {
        var $box = $(Noodle.Dom.Channel.BOX);
        $box.empty();
        var tmpl = Handlebars.compile(template);
        for (var i = 0; i < channels.length; i++) {
            var html = tmpl(channels[i]);
            $box.append(html);
        }
    };

    return {
        click: clickChannel,
        load: loadChannels,
        renderBox: renderChannelBox,
        addChannel: addChannel,
        removeChannel: removeChannel,
        addTag: addTag,
        removeTag: removeTag
    }
})();
