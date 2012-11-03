var Noodle = Noodle || {};

/* Init page */
$( function() {
    /* testing */
//    console.log(Noodle.LiveTag.json);
//    console.log(Noodle.LiveTag.render(Noodle.LiveTag.json));

    Noodle.Channel.load();
    Noodle.Post.load();
    registEvents();
});

/* register elements with specific ajax actions */
var registEvents = function() {
    /* channel */
    $(document).on("click", Noodle.Dom.Channel.CHANNEL_BTN, Noodle.Channel.click);
    $(document).on("click", Noodle.Dom.Channel.ADD_BTN, Noodle.Channel.addChannel);
    $(document).on("click", Noodle.Dom.Channel.REMOVE_BTN, Noodle.Channel.removeChannel);
    $(document).on("keypress", Noodle.Dom.Channel.TAG_INPUT, Noodle.Channel.addTag);
    $(document).on("click", Noodle.Dom.Channel.TAG_REMOVE_BTN, Noodle.Channel.removeTag);

    /* stream */
//    $(document).on("click", "a.loadPosts", Noodle.Post.load);
    $(document).on("click", Noodle.Dom.Post.FORM_NEW_POST_BTN, Noodle.Post.create);
    $(document).on("click", Noodle.Dom.Post.FORM_AUTOTAG_BTN, Noodle.Post.autotag);
    $(document).on("click", Noodle.Dom.Post.REPLY_FORM_BTN, Noodle.Post.create);
    $(document).on("keypress", Noodle.Dom.Post.PUSH_INPUT, Noodle.Post.push);
    $(document).on("keypress", Noodle.Dom.LiveTag.INPUT, Noodle.Post.tag);
    $(document).on("click", Noodle.Dom.LiveTag.VOTE, Noodle.LiveTag.vote);
    $(document).on("click", Noodle.Dom.LiveTag.UNVOTE, Noodle.LiveTag.unvote);

    /* kaleido */
    /*
    $(document).on("click", "a.viewThread", noodle.ajax.loadThread); // not implemented
    */
};